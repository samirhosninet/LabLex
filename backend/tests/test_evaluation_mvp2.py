import pytest
import uuid
import json
from datetime import datetime, timedelta
from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.database import Base
from src.models.evaluation import (
    ToolRun, RunSpec, IdempotencyKey, Comparison, ComparisonItem,
    RunEvent, TenantQuota, TenantRetentionConfig
)
from src.models.tenant import Tenant
from src.core.idempotency import idempotent_endpoint
from src.core.quotas import (
    check_concurrent_quota, check_monthly_quota,
    check_duplicate_runspec_config
)
from src.core.comparison_engine import calculate_comparison, is_lower_better
from src.models.evaluation import NormalizedResult, NormalizedSample
from src.core.errors import LabLexException

# In-memory SQLite for testing DB models
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    
    # Seed a default tenant
    tenant = Tenant(id="tenant_1", name="Test Tenant")
    db.add(tenant)
    db.commit()
    
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_is_lower_better():
    assert is_lower_better("latency_ms") is True
    assert is_lower_better("average_latency_ms") is True
    assert is_lower_better("error_rate") is True
    assert is_lower_better("cost") is True
    assert is_lower_better("accuracy") is False
    assert is_lower_better("score") is False
    assert is_lower_better("bleu_score") is False

@pytest.mark.anyio
async def test_idempotency_decorator(db_session):
    # Setup mock request
    class MockRequest:
        def __init__(self, headers):
            self.headers = headers
            self.method = "POST"

    # Define mock handler
    call_count = 0
    @idempotent_endpoint()
    async def mock_handler(payload: dict, request: Request, db=None, auth=None):
        nonlocal call_count
        call_count += 1
        return {"result": f"success_{call_count}"}

    headers = {"Idempotency-Key": "key_1"}
    req = MockRequest(headers)
    auth = ("user_1", "tenant_1", "admin")

    # 1. First execution
    res1 = await mock_handler({"data": 1}, req, db=db_session, auth=auth)
    assert res1 == {"result": "success_1"}
    assert call_count == 1

    # Verify key saved in DB
    key_rec = db_session.query(IdempotencyKey).filter(IdempotencyKey.key == "key_1").first()
    assert key_rec is not None
    assert key_rec.status_code == 201
    assert key_rec.response_body == {"result": "success_1"}

    # 2. Second execution (should hit cache)
    res2 = await mock_handler({"data": 1}, req, db=db_session, auth=auth)
    # The decorator returns a JSONResponse on cache hit
    assert isinstance(res2, JSONResponse)
    assert json.loads(res2.body.decode()) == {"result": "success_1"}
    assert res2.headers.get("X-Cache-Idempotency") == "HIT"
    assert call_count == 1

def test_quotas_and_limits(db_session):
    # Set quota configuration
    quota = TenantQuota(
        tenant_id="tenant_1",
        max_concurrent_runs=2,
        max_monthly_runs=5
    )
    db_session.add(quota)
    db_session.commit()

    # Create dummy locked runspec
    runspec = RunSpec(id="rs_1", tenant_id="tenant_1", status="locked", components={})
    db_session.add(runspec)
    db_session.commit()

    # 1. Concurrency Check
    # No runs yet: should pass
    check_concurrent_quota("tenant_1", db_session)

    # Insert 2 running runs
    run1 = ToolRun(id="run_1", tenant_id="tenant_1", runspec_id="rs_1", status="running")
    run2 = ToolRun(id="run_2", tenant_id="tenant_1", runspec_id="rs_1", status="queued")
    db_session.add(run1)
    db_session.add(run2)
    db_session.commit()

    # Should raise QUOTA_EXCEEDED
    with pytest.raises(LabLexException) as excinfo:
        check_concurrent_quota("tenant_1", db_session)
    assert excinfo.value.code == "QUOTA_EXCEEDED"

    # 2. Monthly Check
    # Total monthly count is 2 (less than 5), should pass
    check_monthly_quota("tenant_1", db_session)

    # Insert more runs to breach limit of 5
    for i in range(3, 7):
        r = ToolRun(id=f"run_{i}", tenant_id="tenant_1", runspec_id="rs_1", status="completed")
        db_session.add(r)
    db_session.commit()

    with pytest.raises(LabLexException) as excinfo:
        check_monthly_quota("tenant_1", db_session)
    assert excinfo.value.code == "QUOTA_EXCEEDED"

def test_duplicate_runspec_config(db_session):
    # Create two runspecs with the same component config
    components = {"external_tool": "inspect_ai", "model": "gpt-4"}
    rs1 = RunSpec(id="rs_1", tenant_id="tenant_1", status="locked", components=components)
    rs2 = RunSpec(id="rs_2", tenant_id="tenant_1", status="locked", components=components)
    db_session.add(rs1)
    db_session.add(rs2)
    db_session.commit()

    # No runs active yet: should pass
    check_duplicate_runspec_config("tenant_1", "rs_2", db_session)

    # Insert an active run for rs1
    active_run = ToolRun(id="active_run", tenant_id="tenant_1", runspec_id="rs_1", status="running")
    db_session.add(active_run)
    db_session.commit()

    # Triggering rs2 (which has the same components) should raise DUPLICATE_RUN_CONFIG
    with pytest.raises(LabLexException) as excinfo:
        check_duplicate_runspec_config("tenant_1", "rs_2", db_session)
    assert excinfo.value.code == "DUPLICATE_RUN_CONFIG"

def test_comparison_delta_calculation(db_session):
    # Create runspecs
    rs_a = RunSpec(id="rs_a", tenant_id="tenant_1", status="locked", components={})
    rs_b = RunSpec(id="rs_b", tenant_id="tenant_1", status="locked", components={})
    db_session.add(rs_a)
    db_session.add(rs_b)
    db_session.commit()

    # Create Completed ToolRuns
    run_a = ToolRun(id="run_a", tenant_id="tenant_1", runspec_id="rs_a", status="completed")
    run_b = ToolRun(id="run_b", tenant_id="tenant_1", runspec_id="rs_b", status="completed")
    db_session.add(run_a)
    db_session.add(run_b)
    db_session.commit()

    # Add NormalizedResult for Run A
    nr_a = NormalizedResult(
        id="nr_a", tenant_id="tenant_1", run_id="run_a", raw_result_id="raw_a",
        normalization_status="completed", metrics_summary={"accuracy": 0.8, "latency_ms": 200}
    )
    # Add NormalizedResult for Run B
    nr_b = NormalizedResult(
        id="nr_b", tenant_id="tenant_1", run_id="run_b", raw_result_id="raw_b",
        normalization_status="completed", metrics_summary={"accuracy": 0.9, "latency_ms": 150}
    )
    db_session.add(nr_a)
    db_session.add(nr_b)
    db_session.commit()

    # Add NormalizedSamples
    sample_a1 = NormalizedSample(
        id="sa1", tenant_id="tenant_1", normalized_result_id="nr_a",
        sample_id="s1", output_text="Out A", metrics={"accuracy": 0.8}, status="completed", latency_ms=200
    )
    sample_b1 = NormalizedSample(
        id="sb1", tenant_id="tenant_1", normalized_result_id="nr_b",
        sample_id="s1", output_text="Out B", metrics={"accuracy": 0.9}, status="completed", latency_ms=150
    )
    db_session.add(sample_a1)
    db_session.add(sample_b1)
    db_session.commit()

    # Compute Comparison
    result = calculate_comparison("run_a", "run_b", db_session)

    # Assertions
    assert result["overall_winner"] == "run_b"
    assert result["summary"]["accuracy"]["delta"] == 0.1
    assert result["summary"]["accuracy"]["winner"] == "run_b"
    assert result["summary"]["latency_ms"]["delta"] == -50.0
    assert result["summary"]["latency_ms"]["winner"] == "run_b" # Lower is better!

    sample_comp = result["samples"][0]
    assert sample_comp["sample_id"] == "s1"
    assert sample_comp["metrics_comparison"]["accuracy"]["delta"] == 0.1
    assert sample_comp["metrics_comparison"]["accuracy"]["winner"] == "run_b"
    assert sample_comp["metrics_comparison"]["latency_ms"]["delta"] == -50.0
    assert sample_comp["metrics_comparison"]["latency_ms"]["winner"] == "run_b"

@pytest.mark.anyio
async def test_sse_event_replay(db_session):
    from src.api.runs import sse_event_generator
    
    # Mock FastAPI Request
    class MockRequest:
        async def is_disconnected(self):
            return False

    # Insert events in database
    ev1 = RunEvent(id="ev_1", run_id="run_a", event_type="message", data={"progress": 10}, created_at=datetime.utcnow() - timedelta(seconds=10))
    ev2 = RunEvent(id="ev_2", run_id="run_a", event_type="message", data={"progress": 50}, created_at=datetime.utcnow() - timedelta(seconds=5))
    ev3 = RunEvent(id="ev_3", run_id="run_a", event_type="message", data={"progress": 100}, created_at=datetime.utcnow())
    db_session.add(ev1)
    db_session.add(ev2)
    db_session.add(ev3)
    db_session.commit()

    # Insert completed run so generator stops immediately after replay
    run = ToolRun(id="run_a", tenant_id="tenant_1", runspec_id="rs_1", status="completed")
    db_session.add(run)
    db_session.commit()

    # Generator with no last_event_id: should yield all 3 events
    gen1 = sse_event_generator("run_a", MockRequest(), db=db_session)
    events_yielded = []
    async for event in gen1:
        events_yielded.append(event)
    assert len(events_yielded) == 3
    assert events_yielded[0]["id"] == "ev_1"
    assert events_yielded[1]["id"] == "ev_2"
    assert events_yielded[2]["id"] == "ev_3"

    # Generator with last_event_id="ev_1": should yield ev_2 and ev_3
    gen2 = sse_event_generator("run_a", MockRequest(), last_event_id="ev_1", db=db_session)
    events_yielded2 = []
    async for event in gen2:
        events_yielded2.append(event)
    assert len(events_yielded2) == 2
    assert events_yielded2[0]["id"] == "ev_2"
    assert events_yielded2[1]["id"] == "ev_3"

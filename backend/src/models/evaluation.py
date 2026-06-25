import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, Integer, JSON, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from src.core.database import Base

class SecretRef(Base):
    __tablename__ = "secret_refs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    encrypted_value = Column(String, nullable=False)
    key_version = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("tenant_id", "name", name="uq_secret_refs_tenant_name"),
    )

class Manifest(Base):
    __tablename__ = "manifests"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    kind = Column(String(100), nullable=False)
    manifest_id = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    schema_version = Column(String(50), nullable=False)
    manifest_version = Column(String(50), nullable=False)
    deprecated = Column(Boolean, default=False, nullable=False)
    content = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("tenant_id", "kind", "manifest_id", name="uq_manifests_tenant_kind_id"),
    )

class RunSpec(Base):
    __tablename__ = "runspecs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(50), default="draft", nullable=False) # draft, validated, locked
    components = Column(JSON, nullable=False) # JSON object containing selected IDs (e.g. {"external_tool": "x", ...})
    snapshots = Column(JSON, nullable=True) # Frozen copy of manifests when locked
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    tool_runs = relationship("ToolRun", back_populates="runspec", cascade="all, delete-orphan")

class Batch(Base):
    __tablename__ = "batches"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(50), default="pending", nullable=False) # pending, running, completed, partial_failure, failed
    total_runs = Column(Integer, nullable=False, default=0)
    completed_runs = Column(Integer, nullable=False, default=0)
    failed_runs = Column(Integer, nullable=False, default=0)
    max_parallel = Column(Integer, nullable=False, default=3)
    idempotency_key = Column(String(255), nullable=True)
    created_by = Column(String, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    tool_runs = relationship("ToolRun", back_populates="batch")

class ToolRun(Base):
    __tablename__ = "tool_runs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    runspec_id = Column(String, ForeignKey("runspecs.id", ondelete="CASCADE"), nullable=False)
    batch_id = Column(String, ForeignKey("batches.id", ondelete="SET NULL"), nullable=True)
    status = Column(String(50), default="created", nullable=False) # created, queued, running, completed, failed, normalization_failed
    error_message = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_tool_runs_tenant_id_status", "tenant_id", "status"),
        Index("ix_tool_runs_tenant_id_created_at", "tenant_id", "created_at"),
    )

    runspec = relationship("RunSpec", back_populates="tool_runs")
    batch = relationship("Batch", back_populates="tool_runs")
    raw_results = relationship("RawResult", back_populates="tool_run", cascade="all, delete-orphan")
    normalized_results = relationship("NormalizedResult", back_populates="tool_run", cascade="all, delete-orphan")

class RawResult(Base):
    __tablename__ = "raw_results"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    run_id = Column(String, ForeignKey("tool_runs.id", ondelete="CASCADE"), nullable=False)
    storage_path = Column(String(500), nullable=False)
    storage_status = Column(String(50), default="active", nullable=False) # active, archived, deleted
    source_type = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("ix_raw_results_run_id", "run_id"),
        Index("ix_raw_results_tenant_id_storage_status", "tenant_id", "storage_status"),
    )

    tool_run = relationship("ToolRun", back_populates="raw_results")
    normalized_results = relationship("NormalizedResult", back_populates="raw_result", cascade="all, delete-orphan")

class NormalizedResult(Base):
    __tablename__ = "normalized_results"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    run_id = Column(String, ForeignKey("tool_runs.id", ondelete="CASCADE"), nullable=False)
    raw_result_id = Column(String, ForeignKey("raw_results.id", ondelete="CASCADE"), nullable=False)
    normalization_status = Column(String(50), nullable=False) # completed, failed, warnings
    warnings = Column(JSON, nullable=True)
    metrics_summary = Column(JSON, nullable=True) # e.g. {"average_score": 0.85, ...}
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_normalized_results_run_id", "run_id"),
        Index("ix_normalized_results_tenant_id_created_at", "tenant_id", "created_at"),
    )

    tool_run = relationship("ToolRun", back_populates="normalized_results")
    raw_result = relationship("RawResult", back_populates="normalized_results")
    samples = relationship("NormalizedSample", back_populates="normalized_result", cascade="all, delete-orphan")

class NormalizedSample(Base):
    __tablename__ = "normalized_samples"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    normalized_result_id = Column(String, ForeignKey("normalized_results.id", ondelete="CASCADE"), nullable=False)
    sample_id = Column(String(255), nullable=False)
    input_text = Column(String, nullable=True)
    expected_output = Column(String, nullable=True)
    output_text = Column(String, nullable=True)
    error_message = Column(String, nullable=True)
    raw_sample_ref = Column(String(500), nullable=True)
    metrics = Column(JSON, nullable=False) # key-value metrics payload e.g. {"score": 1.0}
    status = Column(String(50), nullable=False) # completed, failed
    latency_ms = Column(Integer, nullable=True)
    sample_metadata = Column("metadata", JSON, nullable=True)

    __table_args__ = (
        Index("ix_normalized_samples_normalized_result_id", "normalized_result_id"),
        Index("ix_normalized_samples_tenant_id_status", "tenant_id", "status"),
    )

    normalized_result = relationship("NormalizedResult", back_populates="samples")


class IdempotencyKey(Base):
    __tablename__ = "idempotency_keys"

    key = Column(String(255), primary_key=True)
    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), primary_key=True)
    response_body = Column(JSON, nullable=True)
    status_code = Column(Integer, nullable=True)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Comparison(Base):
    __tablename__ = "comparisons"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    metrics_delta = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("ix_comparisons_tenant_id_created_at", "tenant_id", "created_at"),
    )

    items = relationship("ComparisonItem", back_populates="comparison", cascade="all, delete-orphan")


class ComparisonItem(Base):
    __tablename__ = "comparison_items"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    comparison_id = Column(String, ForeignKey("comparisons.id", ondelete="CASCADE"), nullable=False)
    run_id = Column(String, ForeignKey("tool_runs.id", ondelete="CASCADE"), nullable=False)

    comparison = relationship("Comparison", back_populates="items")
    tool_run = relationship("ToolRun")


class AuditEvent(Base):
    __tablename__ = "audit_events"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    actor_id = Column(String(255), nullable=False)
    action = Column(String(100), nullable=False)
    resource_type = Column(String(50), nullable=False)
    resource_id = Column(String(255), nullable=False)
    details = Column(JSON, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("ix_audit_events_tenant_id_timestamp", "tenant_id", "timestamp"),
        Index("ix_audit_events_resource", "resource_type", "resource_id"),
        Index("ix_audit_events_actor_tenant", "actor_id", "tenant_id"),
    )


class TenantQuota(Base):
    __tablename__ = "tenant_quotas"

    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), primary_key=True)
    max_concurrent_runs = Column(Integer, nullable=False, default=5)
    max_monthly_runs = Column(Integer, nullable=False, default=100)
    rate_limit_per_minute = Column(Integer, nullable=False, default=60)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TenantRetentionConfig(Base):
    __tablename__ = "tenant_retention_configs"

    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), primary_key=True)
    raw_results_retention_days = Column(Integer, nullable=False, default=30)
    reports_retention_days = Column(Integer, nullable=False, default=365)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class RunEvent(Base):
    __tablename__ = "run_events"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    run_id = Column(String, ForeignKey("tool_runs.id", ondelete="CASCADE"), nullable=False)
    event_type = Column(String(50), nullable=False, default="message")
    data = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("ix_run_events_run_id_created_at", "run_id", "created_at"),
    )

    tool_run = relationship("ToolRun")


from sqlalchemy import event, inspect
from src.core.errors import LabLexException

@event.listens_for(RunSpec, 'before_update')
def enforce_runspec_immutability(mapper, connection, target):
    state = inspect(target)
    db_status = state.committed_state.get('status')
    if db_status in ('locked', 'archived'):
        raise LabLexException(
            code="RUNSPEC_IMMUTABLE",
            message="This RunSpec is locked or archived and cannot be modified.",
            status_code=409
        )


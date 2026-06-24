from sqlalchemy.orm import Session
from src.core.database import SessionLocal, Base, engine
from src.models.tenant import Tenant, Membership
from src.models.user import User
from src.core.security import get_password_hash

def seed_db():
    db = SessionLocal()
    try:
        # 1. Create tables if not exist (fallback for local sqlite/postgres without alembic)
        Base.metadata.create_all(bind=engine)

        # 2. Check if default tenant exists
        tenant = db.query(Tenant).filter(Tenant.name == "LabLex Default Tenant").first()
        if not tenant:
            tenant = Tenant(name="LabLex Default Tenant", encrypted_dek="mock-encrypted-dek-key")
            db.add(tenant)
            db.commit()
            db.refresh(tenant)
            print(f"Created default tenant: {tenant.id}")

        # 3. Check if default admin user exists
        user = db.query(User).filter(User.email == "admin@lablex.ai").first()
        if not user:
            user = User(
                email="admin@lablex.ai",
                hashed_password=get_password_hash("adminpassword"),
                name="System Admin"
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            print(f"Created default admin user: {user.id}")

        # 4. Check if membership exists
        membership = db.query(Membership).filter(
            Membership.user_id == user.id,
            Membership.tenant_id == tenant.id
        ).first()
        if not membership:
            membership = Membership(
                user_id=user.id,
                tenant_id=tenant.id,
                role="admin"
            )
            db.add(membership)
            db.commit()
            print("Seeded membership: admin@lablex.ai -> admin in default tenant")
            
        # 5. Seed Mock Manifests for Registry
        from src.models.evaluation import Manifest
        
        mock_manifests = [
            {
                "kind": "adapter",
                "id": "mock_adapter_v1",
                "name": "Mock Evaluation Adapter",
                "schema_version": "1.0",
                "manifest_version": "1.0.0",
                "type": "mock",
                "class_path": "src.adapters.mock_adapter.MockAdapter",
                "compatible_result_schemas": ["mock_result_schema_v1"]
            },
            {
                "kind": "result_schema",
                "id": "mock_result_schema_v1",
                "name": "Mock Result Schema",
                "schema_version": "1.0",
                "manifest_version": "1.0.0",
                "extraction_rules": {
                    "sample_path": "$.results",
                    "sample_id": "$.id",
                    "input_text": "$.input",
                    "expected_output": "$.expected",
                    "output_text": "$.actual",
                    "error_message": "$.error",
                    "latency_ms": "$.latency_ms",
                    "metrics": {
                        "score": "$.metrics.score",
                        "accuracy": "$.metrics.accuracy"
                    }
                }
            },
            {
                "kind": "external_tool",
                "id": "mock_tool_v1",
                "name": "Mock External Evaluation Tool",
                "schema_version": "1.0",
                "manifest_version": "1.0.0",
                "endpoint": "http://localhost:8080/eval",
                "compatible_adapters": ["mock_adapter_v1"],
                "supported_benchmarks": ["mock_benchmark_v1"]
            },
            {
                "kind": "benchmark",
                "id": "mock_benchmark_v1",
                "name": "Mock Evaluation Benchmark",
                "schema_version": "1.0",
                "manifest_version": "1.0.0",
                "dataset_uri": "s3://lablex-benchmarks/mock.json",
                "required_metrics": ["score", "accuracy"],
                "size": 5
            },
            {
                "kind": "target",
                "id": "mock_target_v1",
                "name": "Mock Deployment Target",
                "schema_version": "1.0",
                "manifest_version": "1.0.0",
                "provider_id": "openai",
                "endpoint": "https://api.openai.com/v1"
            },
            {
                "kind": "model",
                "id": "mock_model_v1",
                "name": "Mock GPT-4 Model",
                "schema_version": "1.0",
                "manifest_version": "1.0.0",
                "provider_id": "openai",
                "compatible_targets": ["mock_target_v1"]
            }
        ]

        for m_data in mock_manifests:
            existing_m = db.query(Manifest).filter(
                Manifest.tenant_id == tenant.id,
                Manifest.kind == m_data["kind"],
                Manifest.manifest_id == m_data["id"]
            ).first()
            if not existing_m:
                db_m = Manifest(
                    tenant_id=tenant.id,
                    kind=m_data["kind"],
                    manifest_id=m_data["id"],
                    name=m_data["name"],
                    schema_version=m_data["schema_version"],
                    manifest_version=m_data["manifest_version"],
                    content=m_data,
                    deprecated=False
                )
                db.add(db_m)
                print(f"Seeded registry manifest: {m_data['kind']} -> {m_data['id']}")
        db.commit()
            
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()

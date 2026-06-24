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
            
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()

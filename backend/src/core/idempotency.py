import functools
import json
from datetime import datetime, timedelta
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from src.models.evaluation import IdempotencyKey
from src.core.errors import LabLexException

def idempotent_endpoint():
    """
    Decorator for FastAPI endpoints to enforce request idempotency via Idempotency-Key.
    Requires the decorated function to receive a 'request' (Request), 'db' (Session),
    and optionally 'auth' (tuple of user_id, tenant_id, role).
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            request: Request = kwargs.get("request")
            db: Session = kwargs.get("db")
            auth = kwargs.get("auth")

            # Fallback check in positional arguments
            if not request:
                for arg in args:
                    if hasattr(arg, "headers") and hasattr(arg, "method"):
                        request = arg
                        break
            if not db:
                for arg in args:
                    if isinstance(arg, Session):
                        db = arg
                        break

            # If request/db is missing or header not provided, skip idempotency logic
            if not request or not db:
                return await func(*args, **kwargs)

            idempotency_key = request.headers.get("Idempotency-Key")
            if not idempotency_key:
                return await func(*args, **kwargs)

            tenant_id = None
            if auth and isinstance(auth, tuple) and len(auth) >= 2:
                tenant_id = auth[1]

            if not tenant_id:
                return await func(*args, **kwargs)

            # Check for existing idempotency key
            record = db.query(IdempotencyKey).filter(
                IdempotencyKey.key == idempotency_key,
                IdempotencyKey.tenant_id == tenant_id
            ).first()

            if record:
                if record.expires_at > datetime.utcnow():
                    if record.response_body is not None:
                        # Return cached response
                        return JSONResponse(
                            content=record.response_body,
                            status_code=record.status_code,
                            headers={"X-Cache-Idempotency": "HIT"}
                        )
                    else:
                        raise LabLexException(
                            code="IDEMPOTENCY_IN_PROGRESS",
                            message="A request with this idempotency key is already in progress.",
                            status_code=409
                        )
                else:
                    # Expired: delete record and proceed
                    db.delete(record)
                    db.commit()

            # Insert pending record
            new_record = IdempotencyKey(
                key=idempotency_key,
                tenant_id=tenant_id,
                response_body=None,
                status_code=None,
                expires_at=datetime.utcnow() + timedelta(hours=24)
            )
            db.add(new_record)
            db.commit()

            try:
                res = await func(*args, **kwargs)

                # Determine status code and response body to cache
                status_code = 200
                if hasattr(res, "status_code"):
                    status_code = res.status_code
                elif isinstance(res, dict) and "status_code" in res:
                    status_code = res["status_code"]
                elif request.method == "POST":
                    status_code = 201

                response_body = None
                if isinstance(res, Response):
                    try:
                        response_body = json.loads(res.body.decode())
                    except Exception:
                        response_body = str(res.body)
                else:
                    response_body = jsonable_encoder(res)

                # Save response to the database
                record = db.query(IdempotencyKey).filter(
                    IdempotencyKey.key == idempotency_key,
                    IdempotencyKey.tenant_id == tenant_id
                ).first()
                if record:
                    record.response_body = response_body
                    record.status_code = status_code
                    db.commit()

                return res

            except Exception as e:
                # Remove pending record on failure so client can retry
                record = db.query(IdempotencyKey).filter(
                    IdempotencyKey.key == idempotency_key,
                    IdempotencyKey.tenant_id == tenant_id
                ).first()
                if record:
                    db.delete(record)
                    db.commit()
                raise e

        return wrapper
    return decorator

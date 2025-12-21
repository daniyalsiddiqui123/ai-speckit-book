import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# backend/main.py
import os

import redis.asyncio as redis
from core.config import get_settings
from core.database import Base, engine
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_limiter import FastAPILimiter

from backend.api.routes import chat

settings = get_settings()

app = FastAPI()

# ------------------------
# CORS Configuration
# ------------------------
# Allow only the production Vercel domain
prod_origin = "https://ai-speckit-book-mjfm.vercel.app/"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ai-speckit-book-mjfm.vercel.app/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ------------------------
# Exception handler
# ------------------------
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


# ------------------------
# Startup: DB + Rate limiter
# ------------------------
@app.on_event("startup")
async def startup_event():
    # For development: recreate tables to ensure schema is correct
    # In production, use proper migrations with Alembic
    import os

    from sqlalchemy import text

    # Only recreate tables in development mode
    env = os.getenv("ENVIRONMENT", "")
    is_production = env.lower() in ["production", "prod"]

    if not is_production:
        with engine.connect() as conn:
            # Use autocommit for DDL statements
            with conn.begin():
                # Drop all tables
                Base.metadata.drop_all(bind=engine)
                # Create all tables with correct schema
                Base.metadata.create_all(bind=engine)
                # Explicitly alter the conversations table to allow NULL user_id
                try:
                    conn.execute(
                        text(
                            "ALTER TABLE conversations ALTER COLUMN user_id DROP NOT NULL;"
                        )
                    )
                except Exception:
                    # If the column is part of a foreign key constraint, we need to handle it differently
                    # This may fail if there's an existing foreign key constraint
                    pass
    else:
        # In production, just create tables if they don't exist
        Base.metadata.create_all(bind=engine)

    redis_instance = redis.from_url(
        os.getenv("REDIS_URL", "redis://localhost:6379"),
        encoding="utf-8",
        decode_responses=True,
    )
    await FastAPILimiter.init(redis_instance)


# ------------------------
# Routers
# ------------------------
app.include_router(chat.router, prefix="/api", tags=["chat"])


@app.get("/")
async def read_root():
    return {"message": "FastAPI backend is running!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
    )

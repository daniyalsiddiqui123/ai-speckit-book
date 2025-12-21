import os

import redis.asyncio as redis
from api.routes import chat  # ✅ FIXED
from core.config import get_settings
from core.database import Base, engine
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_limiter import FastAPILimiter

settings = get_settings()
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ai-speckit-book-mjfm.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})


# Startup
@app.on_event("startup")
async def startup_event():
    from sqlalchemy import text

    env = os.getenv("ENVIRONMENT", "")
    is_production = env.lower() in ["production", "prod"]

    if not is_production:
        # For development: drop and recreate tables with CASCADE for PostgreSQL
        with engine.connect() as conn:
            with conn.begin():
                # Drop tables in reverse order of creation to handle foreign key constraints
                for table in reversed(Base.metadata.sorted_tables):
                    conn.execute(text(f'DROP TABLE IF EXISTS "{table.name}" CASCADE'))
                Base.metadata.create_all(bind=engine)
                try:
                    conn.execute(
                        text(
                            "ALTER TABLE conversations ALTER COLUMN user_id DROP NOT NULL;"
                        )
                    )
                except Exception:
                    pass
    else:
        # For production: only create tables that don't exist, don't drop existing ones
        Base.metadata.create_all(bind=engine)

    # Initialize Redis for rate limiting with error handling
    redis_url = os.getenv("REDIS_URL")
    if redis_url:
        try:
            redis_instance = redis.from_url(
                redis_url,
                encoding="utf-8",
                decode_responses=True,
            )
            await FastAPILimiter.init(redis_instance)
        except Exception as e:
            print(f"Redis connection failed: {e}. Rate limiting may not work.")
            # Continue without Redis - rate limiting will be disabled
    else:
        print("REDIS_URL not set. Rate limiting will be disabled.")
        # Optionally initialize with in-memory store for development
        # You can implement an in-memory fallback if needed


# Routers
app.include_router(chat.router, prefix="/api", tags=["chat"])


@app.get("/")
async def read_root():
    return {"message": "FastAPI backend is running!"}


# Entrypoint
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))

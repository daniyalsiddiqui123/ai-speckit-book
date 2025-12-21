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
        with engine.connect() as conn:
            with conn.begin():
                Base.metadata.drop_all(bind=engine)
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
        Base.metadata.create_all(bind=engine)

    redis_instance = redis.from_url(
        os.getenv("REDIS_URL", "redis://localhost:6379"),
        encoding="utf-8",
        decode_responses=True,
    )
    await FastAPILimiter.init(redis_instance)


# Routers
app.include_router(chat.router, prefix="/api", tags=["chat"])


@app.get("/")
async def read_root():
    return {"message": "FastAPI backend is running!"}


# Entrypoint
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))

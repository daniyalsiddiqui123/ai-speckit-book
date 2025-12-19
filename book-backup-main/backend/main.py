from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from core.config import get_settings
from core.database import engine, Base
# Import all models to ensure they are registered with SQLAlchemy Base
from models import user, conversation, message
from api.routes import auth, chat

from fastapi_limiter import FastAPILimiter
import redis.asyncio as redis # Use redis.asyncio for async FastAPI

settings = get_settings()

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.CLIENT_ORIGIN_URL],  # Allows only the frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Exception handler for HTTPException
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

# Function to create all tables in the database
@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)
    # Initialize FastAPI-Limiter
    # For a real project, ensure Redis is properly configured and accessible
    redis_instance = redis.from_url("redis://localhost:6379", encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis_instance)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(chat.router, prefix="/api", tags=["chat"]) # Prefix can be adjusted

@app.get("/")
async def read_root():
    return {"message": "FastAPI backend is running!"}


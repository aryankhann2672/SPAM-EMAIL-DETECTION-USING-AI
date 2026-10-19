"""FastAPI application entry point and lifespan configuration."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator, Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.database.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Initialize database tables and resources on application startup."""
    init_db()
    yield


app = FastAPI(
    title='AI Spam Email Detection & Threat Analysis API',
    version='1.0.0',
    description='Intelligent NLP-based spam detection with heuristic cybersecurity explainability.',
    lifespan=lifespan,
)

# Configure Cross-Origin Resource Sharing (CORS) for development & production
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        'http://localhost:5173',
        'http://127.0.0.1:5173',
        'http://localhost:5174',
        'http://127.0.0.1:5174',
        'http://localhost:3000',
        'http://127.0.0.1:3000',
    ],
    allow_origin_regex=r'^https?://(localhost|127\.0\.0\.1)(:\d+)?$',
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Root status route for browser verification
@app.get('/')
def root() -> Dict[str, str]:
    """Root health check returning server status and documentation link."""
    return {
        'status': 'online',
        'service': 'AI Spam Email Detection API',
        'docs': '/docs',
        'frontend_url': 'http://localhost:5173',
    }


# Mount API endpoints
app.include_router(router)

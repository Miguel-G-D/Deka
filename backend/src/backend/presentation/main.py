"""FastAPI application entrypoint."""

from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.presentation.dashboard import router as dashboard_router
from backend.presentation.deps import get_connection
from backend.presentation.health import router as health_router
from backend.presentation.meta_webhook import router as meta_webhook_router


@asynccontextmanager
async def lifespan(_application: FastAPI):
    get_connection()
    yield


def create_app() -> FastAPI:
    application = FastAPI(title="Deka API", version="0.1.0", lifespan=lifespan)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://127.0.0.1:3000",
            "http://localhost:3000",
            "http://127.0.0.1:3100",
            "http://localhost:3100",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.include_router(health_router)
    application.include_router(dashboard_router)
    application.include_router(meta_webhook_router)
    return application


app = create_app()


def run() -> None:
    uvicorn.run(
        "backend.presentation.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )

"""FastAPI application."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from stacks_core.models import DockerParams
from stacks_core.registry import registry
from stacks_core.stacks import WebAppDocker

from .routes import router

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle events."""
    # Startup: Registrar stacks
    registry.register("web-app-docker", WebAppDocker, DockerParams)

    yield

    # Shutdown
    pass


app = FastAPI(
    title="Stacks Platform API",
    description="Multi-interface IaC platform",
    version="0.1.0",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


def run():
    """Run the API server."""
    import uvicorn

    uvicorn.run("stacks_api.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    run()

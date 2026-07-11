from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()

    application = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.app_debug,
    )

    @application.get("/", tags=["meta"], summary="Service metadata")
    def root() -> dict[str, str]:
        return {
            "name": settings.app_name,
            "version": settings.app_version,
            "environment": settings.app_environment,
        }

    application.include_router(api_router, prefix=settings.app_api_v1_prefix)
    return application


app = create_app()

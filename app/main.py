from fastapi import FastAPI
from routers.health import router as health_router
from routers.catalog import router as catalog_router
from routers.matches import router as matches_router

app = FastAPI()

app.include_router(health_router)
app.include_router(catalog_router)
app.include_router(matches_router)
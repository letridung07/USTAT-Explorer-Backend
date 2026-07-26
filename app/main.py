from fastapi import FastAPI

from app.api.overview import router as overview_router

app = FastAPI(
    title="USTAT Explorer Backend",
    version="1.0.0"
)

app.include_router(overview_router)
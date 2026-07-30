from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.overview import router as overview_router

app = FastAPI(
    title="USTAT Explorer Backend",
    version="1.0.0"
)

# Frontend addresses allowed to call the backend
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,         # This tells FastAPI which type of middleware you are adding
    allow_origins=origins,  # Allow requests from the frontend addresses stored in the origins list
    allow_methods=["*"],    # Allow all HTTP methods (GET, POST, PUT, PATCH, DELETE)
    allow_headers=["*"],    # Allow the frontend to send any request headers
)

app.include_router(overview_router)
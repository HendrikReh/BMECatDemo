"""FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes.search import router as search_router

app = FastAPI(
    title="Product Search API",
    description="API for searching BMECat product catalog",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(search_router)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}

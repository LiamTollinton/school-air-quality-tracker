from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.cases import router as cases_router
from routes.ai import router as ai_router
from routes.upload import router as upload_router
from routes.air_quality import router as air_quality_router
from routes.school_air_quality import router as school_air_quality_router
from seed_data import seed


@asynccontextmanager
async def lifespan(app: FastAPI):
    seed()
    yield


app = FastAPI(
    title="School Air Quality Tracker",
    description="Prototype for Challenge 3 — supporting casework decisions",
    version="0.2.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cases_router)
app.include_router(ai_router)
app.include_router(upload_router)
app.include_router(air_quality_router)
app.include_router(school_air_quality_router)


@app.get("/")
def root():
    import os
    return {
        "service": "School Air Quality Tracker",
        "status": "running",
        "docs": "/docs",
        "ai_mode": "live" if os.getenv("ANTHROPIC_API_KEY") else "mocked",
    }


@app.get("/health")
def health():
    return {"status": "ok"}

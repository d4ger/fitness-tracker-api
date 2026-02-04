from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import engine, Base
from app.routers import auth, workouts, exercises, stats

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Fitness Tracker API",
    description="Backend API for the Fitness Tracker mobile app",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(workouts.router, prefix="/api")
app.include_router(exercises.router, prefix="/api")
app.include_router(stats.router, prefix="/api")


@app.get("/")
def root():
    return {
        "name": "Fitness Tracker API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}

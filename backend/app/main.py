from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from sqladmin import Admin, ModelView
import logging
import os
from app.database import Base, engine
from app.routers import users, pakaian, laundry, admin
from app import models, minio_client
from prometheus_fastapi_instrumentator import Instrumentator

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Laundry Tracker API",
    description="API  for managing laundry tracking system",
    version="1.0.0"
    )

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

origins = [
    "http://localhost:3000",    # React default
    "http://localhost:5173",    # Vite default
    "http://localhost:8080",    # Vue CLI default
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8080",
    # Add production URLs when deploy
    # "https://yourdomain.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Trusted Host Middleware (optional, for production)
# app.add_middleware(
#     TrustedHostMiddleware, 
#     allowed_hosts=["localhost", "127.0.0.1", "*.yourdomain.com"]
# )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

Instrumentator().instrument(app).expose(app)

# Mounting folder statis
app.mount("/static", StaticFiles(directory="static"), name="static")

admin = Admin(app, engine)

class UserAdmin(ModelView, model=models.User):
    column_list = [models.User.id, models.User.email, models.User.username, models.User.is_admin, models.User.created_at]
    column_searchable_list = [models.User.email, models.User.username]
    column_sortable_list = [models.User.id]

class PakaianAdmin(ModelView, model=models.Pakaian):
    column_list = [models.Pakaian.id, models.Pakaian.nama_pakaian, models.Pakaian.kategori, models.Pakaian.pemilik]
    column_labels = {models.Pakaian.pemilik: "Pemilik"}

class SesiLaundryAdmin(ModelView, model=models.SesiLaundry):
    column_list = [models.SesiLaundry.id, models.SesiLaundry.status, models.SesiLaundry.tanggal_masuk, models.SesiLaundry.pemilik_id]

admin.add_view(UserAdmin)
admin.add_view(PakaianAdmin)
admin.add_view(SesiLaundryAdmin)

app.include_router(users.router)
app.include_router(pakaian.router)
app.include_router(laundry.router)
app.include_router(admin.admin.router)

@app.get("/")
def read_root():
    """
    Root endpoint to check if the API is running.
    """
    logger.info("Root endpoint accessed")
    return {
        "message": "Welcome to the Laundry Tracker API! 🧺",
        "status": "running",
        "version": "1.0.0"
        }

@app.get("/health")
def health_check():
    """
    Health check endpoint for monitoring
    """
    return {
        "status": "healthy",
        "message": "API is running properly"
    }

@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Laundry Tracker API started successfully!")
    logger.info("📝 API Documentation available at: http://localhost:8000/docs")
    logger.info("🔧 Admin Panel available at: http://localhost:8000/admin")

    try:
        minio_client.ensure_bucket_exists(minio_client.env.MINIO_BUCKET)
    except Exception as e:
        logger.error(f"Failed to ensure MinIO bucket exists on startup: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("🛑 Laundry Tracker API shutting down...")
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqladmin import Admin, ModelView
from app.database import Base, engine
from app.routers import users, pakaian, laundry, admin
from app import models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Laundry Tracker API")

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
    return {"message": "Welcome to the Laundry Tracker API! 🧺"}

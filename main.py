# main.py
from fastapi import FastAPI
import app.api.users as users_module
import app.api.tasks as tasks_module
from fastapi.middleware.cors import CORSMiddleware
import app.api.data_read as data_module

app = FastAPI(
    title="IA Proyecto Backend",
    description="API para tu proyecto de IA – endpoints agrupados en un solo router",
    version="0.1.0",
)
origins = [
    "http://localhost:3001",
    # si luego usas otra URL (por ejemplo deploy), agrégala aquí
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # los orígenes que autorizas
    allow_credentials=True,           # si manejas cookies/autenticación
    allow_methods=["*"],              # GET, POST, PUT, DELETE…
    allow_headers=["*"],              # Content-Type, Authorization…
)

app
# Fíjate que ahora es users_module.router, no users_module
app.include_router(users_module.router, prefix="/api/users", tags=["users"])
app.include_router(data_module.router, prefix="/api/data", tags=["data"])
app.include_router(tasks_module.router, prefix="/api/tasks", tags=["tasks"])

# main.py
from fastapi import FastAPI
import app.api.users as users_module

app = FastAPI(
    title="IA Proyecto Backend",
    description="API para tu proyecto de IA – endpoints agrupados en un solo router",
    version="0.1.0",
)

# Fíjate que ahora es users_module.router, no users_module
app.include_router(users_module.router, prefix="/api/users", tags=["users"])

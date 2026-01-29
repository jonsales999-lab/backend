from fastapi import FastAPI
import os
import sys
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

# Configuração de CORS
# Adicionando localhost para testes e a URL do seu frontend na Hostinger
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ecoplaybrasil.com",
        "http://localhost:3000",
        "http://localhost:5173",
        "https://www.ecoplaybrasil.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Importação das rotas (agora na mesma pasta)
from auth_routes import auth_router
from catalog_routes import catalog_router
from equipes import equipes_router
from tarefas_routes import tarefas_router

# Inclui os routers
app.include_router(auth_router)
app.include_router(catalog_router)
app.include_router(equipes_router)
app.include_router(tarefas_router)

@app.get("/")
async def root():
    return {"message": "EcoPlay Backend API is running", "status": "online"}

from fastapi import FastAPI
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

load_dotenv()  # Carrega variáveis de ambiente do arquivo .env

SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ecoplaybrasil.com/"],          # List of allowed origins
    allow_credentials=True,         # Allow cookies to be sent with requests
    allow_methods=["*"],            # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],            # Allow all headers
)



# Serve frontend static files placed in project `frontend/` directory
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.isdir(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

    @app.get("/")
    async def _root_index():
        index_path = os.path.join(FRONTEND_DIR, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        return {"ok": True}


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")

# Permite executar tanto via "uvicorn api.main:app" quanto via "uvicorn main:app" dentro da pasta.
try:
    from .auth_routes import auth_router  # type: ignore
    from .catalog_routes import catalog_router  # type: ignore
    from .equipes import equipes_router  # type: ignore
    from .tarefas_routes import tarefas_router  # type: ignore
except ImportError:  # pragma: no cover - fallback para execução direta
    from api.auth_routes import auth_router
    from api.catalog_routes import catalog_router
    from api.equipes import equipes_router
    from api.tarefas_routes import tarefas_router

# Inclui os routers
app.include_router(auth_router)
app.include_router(catalog_router)
app.include_router(equipes_router)
app.include_router(tarefas_router)
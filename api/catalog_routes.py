from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List, Optional

from .models import Escola, Usuario
from .dependencies import pegar_sesssao

catalog_router = APIRouter(prefix="/catalog", tags=["catalogo"])

TEMPLATES_DIR = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@catalog_router.get("/escolas")
def listar_escolas(session: Session = Depends(pegar_sesssao)) -> List[dict]:
    escolas = session.query(Escola).all()
    return [
        {"id": escola.id, "nome": escola.nome}
        for escola in escolas
    ]


@catalog_router.get("/usuarios")
def listar_usuarios(
    escola_id: Optional[int] = None,
    somente_fiscais: bool = False,
    session: Session = Depends(pegar_sesssao),
) -> List[dict]:
    query = session.query(Usuario)
    if escola_id is not None:
        query = query.filter(Usuario.escola_id == escola_id)
    if somente_fiscais:
        query = query.filter(Usuario.funcao.ilike("%fiscal%"))

    usuarios = query.all()
    return [
        {
            "id": u.id,
            "nome_completo": u.nome_completo,
            "escola_id": u.escola_id,
            "funcao": u.funcao,
            "escola_nome": getattr(u.escola, "nome", None),
        }
        for u in usuarios
    ]


@catalog_router.get("/{page_name}.html", response_class=HTMLResponse)
def servir_pagina(page_name: str, request: Request):
    """Renderiza arquivos HTML localizados em api/templates."""
    filename = f"{page_name}.html"
    file_path = TEMPLATES_DIR / filename
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="Página não encontrada")
    return templates.TemplateResponse(filename, {"request": request})


@catalog_router.get("/{asset_name}.js")
def servir_script(asset_name: str):
    """Entrega arquivos JS do diretório de templates para páginas renderizadas."""
    filename = f"{asset_name}.js"
    file_path = TEMPLATES_DIR / filename
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")
    return FileResponse(file_path, media_type="application/javascript")

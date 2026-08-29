from fastapi.responses import HTMLResponse, FileResponse
from fastapi import APIRouter, Request
from pathlib import Path

router = APIRouter(tags=["pages"])
TEMPLATES_DIR = Path("templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return FileResponse(TEMPLATES_DIR / "index.html")


@router.get("/books_page", response_class=HTMLResponse)
async def books_page(request: Request):
    return FileResponse(TEMPLATES_DIR / "books.html")


@router.get("/files", response_class=HTMLResponse)
async def files_page(request: Request):
    return FileResponse(TEMPLATES_DIR / "files.html")


@router.get("/information", response_class=HTMLResponse)
async def information_page(request: Request):
    return FileResponse(TEMPLATES_DIR / "information.html")


@router.get("/desk", response_class=HTMLResponse)
async def desk_page(request: Request):
    return FileResponse(TEMPLATES_DIR / "desk.html")


@router.get("/info/{name}", response_class=HTMLResponse)
async def info_page(request: Request, name: str):
    return FileResponse(TEMPLATES_DIR / "info.html")
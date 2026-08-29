from fastapi.responses import HTMLResponse, FileResponse
from fastapi import APIRouter, Request
from pathlib import Path

router = APIRouter(tags=["pages"])

# Путь к templates
TEMPLATES_DIR = Path("templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Главная страница"""
    html_file = TEMPLATES_DIR / "index.html"
    return FileResponse(html_file)


@router.get("/books_page", response_class=HTMLResponse)
async def books_page(request: Request):
    """Страница библиотеки"""
    html_file = TEMPLATES_DIR / "books.html"
    return FileResponse(html_file)


@router.get("/files", response_class=HTMLResponse)
async def files_page(request: Request):
    """Страница файлов"""
    html_file = TEMPLATES_DIR / "files.html"
    return FileResponse(html_file)

@router.get("/desk", response_class=HTMLResponse)
async def get_desk(request: Request):
    html_file = TEMPLATES_DIR / "desk.html"
    return FileResponse(html_file)

@router.get("/information", response_class=HTMLResponse)
async def information_page(request: Request):
    """Страница информации"""
    html_file = TEMPLATES_DIR / "information.html"
    return FileResponse(html_file)
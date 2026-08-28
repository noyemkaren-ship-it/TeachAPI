from fastapi import APIRouter, HTTPException, UploadFile, File, status
from fastapi.responses import FileResponse
from typing import List
import os
import shutil
from pathlib import Path

router = APIRouter(tags=["files"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx", ".txt", ".md"}


@router.post("/files/upload")
async def upload_file(file: UploadFile = File(...)):
    """Загрузка файла на сервер"""
    try:
        file_extension = Path(file.filename).suffix.lower()

        if file_extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type {file_extension} not allowed"
            )

        file_path = UPLOAD_DIR / file.filename

        # Проверка на существование файла
        if file_path.exists():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"File {file.filename} already exists"
            )

        # Сохраняем файл
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {
            "filename": file.filename,
            "size": os.path.getsize(file_path),
            "status": "uploaded"
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Upload failed: {str(e)}"
        )


@router.get("/files/list")
async def list_files():
    """Получение списка всех файлов"""
    try:
        files = []
        for file_path in UPLOAD_DIR.iterdir():
            if file_path.is_file():
                files.append({
                    "name": file_path.name,
                    "size": os.path.getsize(file_path),
                    "type": file_path.suffix,
                    "modified": file_path.stat().st_mtime
                })
        return files
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list files: {str(e)}"
        )


@router.get("/files/download/{filename}")
async def download_file(filename: str):
    """Скачивание файла"""
    try:
        file_path = UPLOAD_DIR / filename

        if not file_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"File {filename} not found"
            )

        return FileResponse(
            path=file_path,
            filename=filename,
            media_type="application/octet-stream"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Download failed: {str(e)}"
        )


@router.delete("/files/{filename}")
async def delete_file(filename: str):
    """Удаление файла"""
    try:
        file_path = UPLOAD_DIR / filename

        if not file_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"File {filename} not found"
            )

        file_path.unlink()
        return {"message": f"File {filename} deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Delete failed: {str(e)}"
        )
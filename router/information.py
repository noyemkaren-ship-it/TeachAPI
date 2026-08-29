from fastapi import APIRouter, HTTPException, status
from repository import InformationRepository
from schemas.information import Information as InformationCreate
from models import Information

router = APIRouter(tags=["information"])
info_repo = InformationRepository()


@router.get("/api/informations")
async def get_informations():
    try:
        return info_repo.get_all()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/api/informations/subjects")
async def get_subjects():
    """Получение списка всех предметов"""
    try:
        return info_repo.get_all_subjects()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/api/informations/subject/{subject}")
async def get_information_by_subject(subject: str):
    """Получение информации по предмету"""
    try:
        info = info_repo.get_by_subject(subject)
        if info is None:
            raise HTTPException(status_code=404, detail="Information not found")
        return info
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/api/informations/name/{name}")
async def get_information_by_name(name: str):
    try:
        info = info_repo.get_by_name(name)
        if info is None:
            raise HTTPException(status_code=404, detail="Information not found")
        return info
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/api/informations")
async def post_informations(information: InformationCreate):
    """Создание новой информации"""
    try:
        new_info = Information(**information.model_dump())
        result = info_repo.create_information(new_info)

        if isinstance(result, dict) and "Message" in result:
            raise HTTPException(status_code=400, detail=result["Message"])

        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/api/informations/name/{name}")
async def delete_information_by_name(name: str):
    """Удаление информации по имени"""
    try:
        result = info_repo.delete_by_name(name)
        if "not found" in result["Message"].lower():
            raise HTTPException(status_code=404, detail=result["Message"])
        elif "not deleted" in result["Message"].lower():
            raise HTTPException(status_code=400, detail=result["Message"])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/api/informations/subject/{subject}")
async def delete_information_by_subject(subject: str):
    try:
        result = info_repo.delete_by_subject(subject)
        if "not found" in result["Message"].lower():
            raise HTTPException(status_code=404, detail=result["Message"])
        elif "not deleted" in result["Message"].lower():
            raise HTTPException(status_code=400, detail=result["Message"])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
from fastapi import APIRouter, HTTPException, status
from repository import InformationRepository
from schemas.information import Information as InformationCreate
from models import Information

router = APIRouter(tags=["information"])
info_repo = InformationRepository()


@router.get("/informations")
async def get_informations():
    try:
        return info_repo.get_all()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/informations/{subject}")
async def get_information(subject: str):
    try:
        info = info_repo.get_by_subject(subject)
        if info is None:
            raise HTTPException(status_code=404, detail="Information not found")
        return info
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/informations")
async def post_informations(information: InformationCreate):
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
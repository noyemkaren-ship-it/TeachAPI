from fastapi import APIRouter, HTTPException, status
from typing import List

from schemas import BookCreate, BookUpdate, BookResponse
from repository import BookRepository

router = APIRouter(tags=["book"])
book_repo = BookRepository()


@router.get("/books", response_model=List[BookResponse])
async def get_books():
    books = book_repo.get_all_books()
    return books


@router.get("/book/id/{book_id}", response_model=BookResponse)
async def get_book_by_id(book_id: int):
    book = book_repo.get_book_by_id(book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return book


@router.get("/book/{name}", response_model=BookResponse)
async def get_book(name: str):
    book = book_repo.get_book_by_name(name)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return book


@router.post("/book", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(book_data: BookCreate):
    result = book_repo.create_book(book_data)
    if isinstance(result, dict):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["Message"]
        )
    return result


@router.put("/book/{book_id}", response_model=BookResponse)
async def update_book(book_id: int, book_data: BookUpdate):
    result = book_repo.update_book(book_id, book_data)
    if isinstance(result, dict):
        if "not found" in result["Message"].lower():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=result["Message"]
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["Message"]
        )
    return result


@router.delete("/book/{name}")
async def delete_book(name: str):
    result = book_repo.delete_book_by_name(name)
    if isinstance(result, dict):
        if "not found" in result["Message"].lower():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=result["Message"]
            )
        elif "not deleted" in result["Message"].lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["Message"]
            )
    return result
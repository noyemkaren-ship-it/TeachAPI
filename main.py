from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from router import page_router, book_router, file_router
import uvicorn

app = FastAPI(
    title="TeachApp API",
    description="Enterprise Learning Management System",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(page_router)
app.include_router(book_router)
app.include_router(file_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
from .page import router as page_router
from .book import router as book_router
from .file import router as file_router
from .information import router as information_router

__all__ = ["page_router", "book_router", "file_router", "information_router"]
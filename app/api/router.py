from fastapi.routing import APIRouter

from .auth import router as auth_router
from .users import router as user_router
from .task import router as tasks_router
from .categories import router as category_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(user_router)
router.include_router(tasks_router)
router.include_router(category_router)

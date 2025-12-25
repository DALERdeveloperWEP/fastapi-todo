from typing import Annotated, List
import shutil
from uuid import uuid1

from sqlalchemy.orm import Session
from fastapi import Body, HTTPException, status, Depends, File, UploadFile, Form
from fastapi.routing import APIRouter

from ..core.dependencies import get_db
from ..schemas.categories import CategoryResponse
from ..models.user import User
from ..models.task import Category
from ..api.deps import get_admin, get_curent_user

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", response_model=CategoryResponse)
def create_categories(
    name: Annotated[str, Form()],
    color: Annotated[str, Form()],
    icon: Annotated[UploadFile, File()],
    db: Annotated[Session, Depends(get_db)],
    admin: Annotated[User, Depends(get_admin)]
):

    existing_category = db.query(Category).filter(Category.name == name).first()
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Category already exists."
        )

    img_types = {
        "image/jpeg": {"jpg"},
        "image/png": {"png"},
        "image/webp": {"webp"},
        "image/gif": {"gif"},
        "image/svg+xml": {"svg"},
    }

    file_type = None

    for img in img_types:
        if img == icon.content_type:
            file_type = list(img_types[img])[0]

    if not file_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="File type is not supported"
        )

    icon_path = f"media/icon/{str(uuid1())}.{file_type}"

    with open(icon_path, "wb") as buffer:
        shutil.copyfileobj(icon.file, buffer)

    new_category = Category(name=name, color=color, icon=icon_path)

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


@router.get("/", response_model=List[CategoryResponse])
def get_category_list(db: Annotated[Session, Depends(get_db)], user: Annotated[User, Depends(get_curent_user)]):
    return db.query(Category).all()


@router.get("/{pk}")
def get_one_category(pk: int):
    pass


@router.put("/{pk}")
def update_category():
    pass


@router.delete("/{pk}")
def delete_category():
    pass

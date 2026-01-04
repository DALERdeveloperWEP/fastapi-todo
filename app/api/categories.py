import os
from typing import Annotated, List
import shutil
from uuid import uuid1


from sqlalchemy.orm import Session
from storage3.exceptions import StorageApiError
from fastapi import HTTPException, status, Depends, File, UploadFile, Form
from fastapi.routing import APIRouter
from supabase import create_client

from ..core.dependencies import get_db
from ..schemas.categories import CategoryResponse
from ..models.user import User
from ..models.task import Category
from ..api.deps import get_admin, get_curent_user
from ..core.config import settings

router = APIRouter(prefix="/categories", tags=["Categories"])
supabase = create_client(supabase_key=settings.supabase_key, supabase_url=settings.supabase_url)

@router.post("/", response_model=CategoryResponse)
def create_categories(
    name: Annotated[str, Form()],
    color: Annotated[str, Form()],
    icon: Annotated[UploadFile, File()],
    db: Annotated[Session, Depends(get_db)],
    admin: Annotated[User, Depends(get_admin)],
) -> CategoryResponse:
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

    icon_path = f"icon/{str(uuid1())}.{file_type}"

    # Save file locally
    # with open(icon_path, "wb") as buffer:
    #     shutil.copyfileobj(icon.file, buffer)

    # Upload to Supabase Storage
    try:
        res = supabase.storage.from_("media").upload(
            icon_path,
            icon.file.read(),
            {"content-type": icon.content_type}
        )
    except StorageApiError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    new_category = Category(name=name, color=color, icon=icon_path)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return CategoryResponse(
        category_id=new_category.category_id,
        name=new_category.name,
        color=new_category.color,
        icon=f"https://ffqzvugwuogmwjtmyquj.supabase.co/storage/v1/object/public/media/{icon_path}"
    )


@router.get("/", response_model=List[CategoryResponse])
def get_category_list(
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_curent_user)],
) -> List[CategoryResponse]:
    categories = db.query(Category).all()
    result = []
    
    for category in categories:
        signed_url = supabase.storage.from_("media").get_public_url(category.icon)
        result.append(CategoryResponse(
            category_id=category.category_id,
            name=category.name,
            color=category.color,
            icon=signed_url
        ))
    return result


@router.get("/{pk}", status_code=status.HTTP_200_OK, response_model=CategoryResponse)
def get_one_category(
    pk: int,
    user: Annotated[User, Depends(get_curent_user)],
    db: Annotated[Session, Depends(get_db)],
) -> CategoryResponse:
    category = db.query(Category).get(pk)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found."
        )
    signed_url = supabase.storage.from_("media").get_public_url(category.icon)
    
    return CategoryResponse(
        category_id=category.category_id,
        name=category.name,
        color=category.color,
        icon=signed_url
    )


@router.put("/{pk}", status_code=status.HTTP_200_OK, response_model=CategoryResponse)
def update_category(
    pk: int,
    admin: Annotated[User, Depends(get_admin)],
    db: Annotated[Session, Depends(get_db)],
    name: Annotated[str | None, Form()] = None,
    color: Annotated[str, Form()] = None,
    icon: Annotated[UploadFile | None, File()] = None,
) -> CategoryResponse:
    category = db.query(Category).get(pk)

    if name is None and color is None and icon is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided for update.",
        )

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found."
        )

    update_name = name
    update_color = color
    update_icon = icon

    if update_name:
        category.name = name

    if update_color:
        category.color = color

    if update_icon:
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
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File type is not supported",
            )

        icon_path = f"icon/{str(uuid1())}.{file_type}"

        # Save file locally
        # with open(icon_path, "wb") as buffer:
        #     shutil.copyfileobj(icon.file, buffer)

        # Upload to Supabase Storage
        try:
            res = supabase.storage.from_("media").upload(
                icon_path,
                icon.file.read(),
                {"content-type": icon.content_type}
            )
        except StorageApiError as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )
        
        # Delete old icon file from local storage
        # os.remove(category.icon)
        
        supabase.storage.from_("media").remove([category.icon.split('/')[-1]])

        category.icon = icon_path

    db.commit()
    db.refresh(category)
    return CategoryResponse(
        category_id=category.category_id,
        name=category.name,
        color=category.color,
        icon=f"https://ffqzvugwuogmwjtmyquj.supabase.co/storage/v1/object/public/media/{category.icon}"
    )


@router.delete("/{pk}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    pk: int,
    admin: Annotated[User, Depends(get_admin)],
    db: Annotated[Session, Depends(get_db)],
):
    category = db.query(Category).get(pk)

    if not category:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found."
        )
    
    # Delete icon file from local storage
    # os.remove(category.icon)
    
    # Delete icon file from Supabase Storage
    supabase.storage.from_("media").remove([category.icon.split('https://ffqzvugwuogmwjtmyquj.supabase.co/storage/v1/object/public/media/')[-1]])
    
    db.delete(category)
    db.commit()
    return {"detail": "Category deleted successfully."}

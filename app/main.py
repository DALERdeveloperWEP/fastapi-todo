from fastapi import FastAPI
from .models import user, task
from app.core.database import engine, Base
from app.api.router import router

app = FastAPI(title="Todo List", version="1.0.0", description="FastAPI Todo List API")

app.include_router(router, prefix="/api")


@app.get("/")
def abwdbwd():
    return {}


# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

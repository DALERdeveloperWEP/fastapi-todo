from fastapi import FastAPI
from .models import user, task
from app.core.database import engine, Base 

app = FastAPI(title='Todo List', version='1.0.0', description='FastAPI Todo List API')

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
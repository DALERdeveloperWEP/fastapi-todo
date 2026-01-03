from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .models import user, task
from app.core.database import engine, Base
from app.api.router import router
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Todo List", version="1.0.0", description="FastAPI Todo List API")
app.include_router(router, prefix="/api")
# app.mount("/media", StaticFiles(directory="media"), name="media")

origins = [
    "http://localhost:5501",
    "http://localhost:5500",
    "http://127.0.0.1:5501",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5500",
    "http://localhost:3000"
    "http://192.168.1.8:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],   # ruxsat berilgan frontend URL
    allow_credentials=True,
    allow_methods=["*"],     # GET, POST, PUT, DELETE ...
    allow_headers=["*"],     # Content-Type, Authorization ...
)


@app.get("/")
def abwdbwd():
    return {}

@app.middleware("http")
async def csp_middleware(request, call_next):
    response = await call_next(request)
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "connect-src 'self' http://localhost:8000 http://127.0.0.1:8000;"
    )
    return response




# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

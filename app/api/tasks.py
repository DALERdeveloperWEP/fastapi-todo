from fastapi.routing import APIRouter

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/tasks")
def create_task():
    pass


@router.get("/tasks")
def get_task_list():
    pass


@router.get("/tasks/{pk}")
def get_one_task(pk: int):
    pass


@router.put("/tasks/{pk}")
def update_task():
    pass


@router.delete("/tasks/{pk}")
def delete_task():
    pass

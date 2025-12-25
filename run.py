from asyncio import CancelledError
import uvicorn
from time import sleep

if __name__ == "__main__":
    try:
        uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
    except CancelledError:
        pass
        # sleep(2)
        # uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

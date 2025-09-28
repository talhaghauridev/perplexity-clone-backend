from typing import Union
from fastapi import FastAPI
from src.routes import router

app = FastAPI()

# Include the API router
app.include_router(router=router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8000, host="localhost")

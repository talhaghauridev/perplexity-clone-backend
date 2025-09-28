from fastapi import FastAPI

app = FastAPI()


def main():
    print("Hello from backend!")


app.add_api_route("/", main, methods=["GET"])


@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
    )

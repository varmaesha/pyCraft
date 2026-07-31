from fastapi import FastAPI

app = FastAPI()


@app.get("/dummy")
async def read_dummy():
    return {
        "message": "hello from dummy endpoint",
        "data": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}],
    }


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"id": item_id, "name": f"item-{item_id}"}

from fastapi import FastAPI
from .schemas import Gift

app = FastAPI()


@app.post("/gift")
async def post_gift(gift: Gift):
    return gift

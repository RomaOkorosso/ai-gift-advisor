from fastapi import FastAPI

from app.api import gift_router

app = FastAPI(
    title="AI Gift Advisor",
)

app.include_router(gift_router)


@app.get("/")
async def root():
    return {"message": "AI Gift Advisor API"}


@app.get("/health")
async def health():
    return {"message": "OK"}

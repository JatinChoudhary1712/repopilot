from fastapi import FastAPI

from app.routers.github import router as github_router

app = FastAPI(
    title="RepoPilot",
    version="0.1.0",
)

app.include_router(github_router)


@app.get("/")
async def root():
    return {"status": "ok"}
from fastapi import FastAPI

app = FastAPI(
    title="RepoPilot",
    version="0.1.0",
)


@app.get("/")
async def root():
    return {"status": "ok"}
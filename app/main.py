from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def health_check():
    return "API Service is up and running"
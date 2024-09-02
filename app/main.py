from fastapi import FastAPI
from routers import auth, company


app = FastAPI()

app.include_router(auth.router)
app.include_router(company.router)

@app.get("/", tags=["Health Check"])
async def health_check():
    return "API Service is up and running!"
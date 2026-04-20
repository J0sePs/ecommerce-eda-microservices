from fastapi import FastAPI

app = FastAPI(title="inventory Service")

@app.get("/")
async def root():
    return {"message": "Hello from inventory"}


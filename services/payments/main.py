from fastapi import FastAPI

app = FastAPI(title="payments Service")

@app.get("/")
async def root():
    return {"message": "Hello from payments"}


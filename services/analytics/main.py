from fastapi import FastAPI

app = FastAPI(title="analytics Service")

@app.get("/")
async def root():
    return {"message": "Hello from analytics"}


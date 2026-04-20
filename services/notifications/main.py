from fastapi import FastAPI

app = FastAPI(title="notifications Service")

@app.get("/")
async def root():
    return {"message": "Hello from notifications"}


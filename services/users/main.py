from fastapi import FastAPI

app = FastAPI(title="users Service")

@app.get("/")
async def root():
    return {"message": "Hello from users"}


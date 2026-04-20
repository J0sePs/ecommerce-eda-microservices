from fastapi import FastAPI

app = FastAPI(title="products Service")

@app.get("/")
async def root():
    return {"message": "Hello from products"}


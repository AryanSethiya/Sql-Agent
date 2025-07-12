from fastapi import FastAPI

app = FastAPI(title="Test App")

@app.get("/")
async def root():
    return {"status": "ok", "message": "Test app is running"}

@app.get("/health")
async def health():
    return {"status": "healthy", "message": "Test app is healthy"} 
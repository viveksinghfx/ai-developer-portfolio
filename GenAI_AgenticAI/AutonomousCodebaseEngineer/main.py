from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints.engineer import router as engineer_router

app = FastAPI(
    title="Autonomous Codebase Engineer",
    description="Give it a GitHub repo URL + task — it reads the code and writes the implementation.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(engineer_router, prefix="/api/v1", tags=["engineer"])


@app.get("/health")
def health():
    return {"status": "healthy"}

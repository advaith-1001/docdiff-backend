from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import upload
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://doc-diff-ten.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/api")
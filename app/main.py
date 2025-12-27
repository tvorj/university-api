from fastapi import FastAPI
from app.routers.teacher import router as teacher_router

app = FastAPI()
app.include_router(teacher_router)

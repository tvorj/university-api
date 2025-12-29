from fastapi import FastAPI
from app.routers.teacher import router as teacher_router
from app.routers.subject import router as subject_router
from app.routers.lesson import router as lesson_router

app = FastAPI()
app.include_router(teacher_router)
app.include_router(subject_router)
app.include_router(lesson_router)

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Lesson, Teacher, Subject
from app.schemas import LessonCreate, LessonUpdate, LessonOut

router = APIRouter(prefix="/lessons", tags=["lessons"])


@router.post("", response_model=LessonOut)
def create_lesson(payload: LessonCreate, db: Session = Depends(get_db)):
    if not db.query(Teacher).filter(Teacher.id == payload.teacher_id).first():
        raise HTTPException(status_code=400, detail="teacher_id does not exist")
    if not db.query(Subject).filter(Subject.id == payload.subject_id).first():
        raise HTTPException(status_code=400, detail="subject_id does not exist")

    l = Lesson(**payload.dict())
    db.add(l)
    db.commit()
    db.refresh(l)
    return l


@router.get("", response_model=List[LessonOut])
def list_lessons(limit: int = 20, offset: int = 0, db: Session = Depends(get_db)):
    return db.query(Lesson).order_by(Lesson.id).offset(offset).limit(limit).all()


@router.get("/{lesson_id}", response_model=LessonOut)
def get_lesson(lesson_id: int, db: Session = Depends(get_db)):
    l = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not l:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return l


@router.patch("/{lesson_id}", response_model=LessonOut)
def update_lesson(lesson_id: int, payload: LessonUpdate, db: Session = Depends(get_db)):
    l = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not l:
        raise HTTPException(status_code=404, detail="Lesson not found")

    data = payload.dict(exclude_unset=True)
    if "teacher_id" in data and not db.query(Teacher).filter(Teacher.id == data["teacher_id"]).first():
        raise HTTPException(status_code=400, detail="teacher_id does not exist")
    if "subject_id" in data and not db.query(Subject).filter(Subject.id == data["subject_id"]).first():
        raise HTTPException(status_code=400, detail="subject_id does not exist")

    for k, v in data.items():
        setattr(l, k, v)

    db.commit()
    db.refresh(l)
    return l


@router.delete("/{lesson_id}")
def delete_lesson(lesson_id: int, db: Session = Depends(get_db)):
    l = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not l:
        raise HTTPException(status_code=404, detail="Lesson not found")

    db.delete(l)
    db.commit()
    return {"ok": True}

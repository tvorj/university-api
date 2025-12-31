from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.schemas import TeacherCreate, TeacherUpdate, TeacherOut, TeacherLessonsCountOut


from app.db import get_db
from app.models import Teacher

router = APIRouter(prefix="/teachers", tags=["teachers"])


@router.post("", response_model=TeacherOut)
def create_teacher(payload: TeacherCreate, db: Session = Depends(get_db)):
    t = Teacher(
        fio=payload.fio,
        kafedra=payload.kafedra,
        dolzhnost=payload.dolzhnost,
        uch_stepen=payload.uch_stepen,
    )
    db.add(t)
    db.commit()
    db.refresh(t)
    return t


@router.get("", response_model=List[TeacherOut])
def list_teachers(limit: int = 20, offset: int = 0, db: Session = Depends(get_db)):
    return db.query(Teacher).order_by(Teacher.id).offset(offset).limit(limit).all()

@router.get("/stats/lessons-count", response_model=List[TeacherLessonsCountOut])
def lessons_count_by_teacher(db: Session = Depends(get_db)):
    rows = (
        db.query(Teacher.id.label("teacher_id"), func.count().label("lessons_count"))
        .join(Teacher.lessons)
        .group_by(Teacher.id)
        .order_by(func.count().desc())
        .all()
    )
    return [{"teacher_id": r.teacher_id, "lessons_count": r.lessons_count} for r in rows]

@router.get("/search/regex", response_model=List[TeacherOut])
def search_teachers_regex(
    pattern: str,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    return (
        db.query(Teacher)
        .filter(Teacher.fio.op("~")(pattern))
        .order_by(Teacher.id)
        .offset(offset)
        .limit(limit)
        .all()
    )



@router.get("/{teacher_id}", response_model=TeacherOut)
def get_teacher(teacher_id: int, db: Session = Depends(get_db)):
    t = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return t


@router.patch("/{teacher_id}", response_model=TeacherOut)
def update_teacher(teacher_id: int, payload: TeacherUpdate, db: Session = Depends(get_db)):
    t = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Teacher not found")

    for k, v in payload.dict(exclude_unset=True).items():
        setattr(t, k, v)

    db.commit()
    db.refresh(t)
    return t


@router.delete("/{teacher_id}")
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    t = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Teacher not found")

    db.delete(t)
    db.commit()
    return {"ok": True}

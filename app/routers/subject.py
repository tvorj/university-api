from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Subject
from app.schemas import SubjectCreate, SubjectUpdate, SubjectOut

router = APIRouter(prefix="/subjects", tags=["subjects"])


@router.post("", response_model=SubjectOut)
def create_subject(payload: SubjectCreate, db: Session = Depends(get_db)):
    s = Subject(**payload.dict())
    db.add(s)
    db.commit()
    db.refresh(s)
    return s


@router.get("", response_model=List[SubjectOut])
def list_subjects(limit: int = 20, offset: int = 0, db: Session = Depends(get_db)):
    return db.query(Subject).order_by(Subject.id).offset(offset).limit(limit).all()

@router.patch("/bulk/mark-nonmandatory")
def mark_nonmandatory(min_hours: int = 32, db: Session = Depends(get_db)):
    updated = (
        db.query(Subject)
        .filter(Subject.chislo_chasov < min_hours)
        .update({Subject.obyazatelnost: False}, synchronize_session=False)
    )
    db.commit()
    return {"updated": updated}


@router.get("/{subject_id}", response_model=SubjectOut)
def get_subject(subject_id: int, db: Session = Depends(get_db)):
    s = db.query(Subject).filter(Subject.id == subject_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Subject not found")
    return s


@router.patch("/{subject_id}", response_model=SubjectOut)
def update_subject(subject_id: int, payload: SubjectUpdate, db: Session = Depends(get_db)):
    s = db.query(Subject).filter(Subject.id == subject_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Subject not found")

    for k, v in payload.dict(exclude_unset=True).items():
        setattr(s, k, v)

    db.commit()
    db.refresh(s)
    return s


@router.delete("/{subject_id}")
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    s = db.query(Subject).filter(Subject.id == subject_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Subject not found")

    db.delete(s)
    db.commit()
    return {"ok": True}
from typing import Optional
from pydantic import BaseModel
from datetime import date, time


class TeacherCreate(BaseModel):
    fio: str
    kafedra: str
    dolzhnost: str
    uch_stepen: Optional[str] = None


class TeacherUpdate(BaseModel):
    fio: Optional[str] = None
    kafedra: Optional[str] = None
    dolzhnost: Optional[str] = None
    uch_stepen: Optional[str] = None


class TeacherOut(BaseModel):
    id: int
    fio: str
    kafedra: str
    dolzhnost: str
    uch_stepen: Optional[str] = None

    class Config:
        orm_mode = True

class SubjectCreate(BaseModel):
    nazvanie: str
    chislo_chasov: int
    vid_proverki: str
    obyazatelnost: bool


class SubjectUpdate(BaseModel):
    nazvanie: Optional[str] = None
    chislo_chasov: Optional[int] = None
    vid_proverki: Optional[str] = None
    obyazatelnost: Optional[bool] = None


class SubjectOut(BaseModel):
    id: int
    nazvanie: str
    chislo_chasov: int
    vid_proverki: str
    obyazatelnost: bool

    class Config:
        orm_mode = True

class LessonCreate(BaseModel):
    teacher_id: int
    subject_id: int
    data: date
    vremya: time
    auditoriya: str
    vid_zanyatiya: str
    gruppa: str

class LessonUpdate(BaseModel):
    teacher_id: int = None
    subject_id: int = None
    data: date = None
    vremya: time = None
    auditoriya: str = None
    vid_zanyatiya: str = None
    gruppa: str = None

class LessonOut(BaseModel):
    id: int
    teacher_id: int
    subject_id: int
    data: date
    vremya: time
    auditoriya: str
    vid_zanyatiya: str
    gruppa: str

    class Config:
        orm_mode = True

from typing import Optional
from pydantic import BaseModel


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

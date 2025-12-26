from sqlalchemy import Column, BigInteger, Text, Integer, Boolean, Date, Time, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Teacher(Base):
    __tablename__ = "teacher"

    id = Column(BigInteger, primary_key=True)
    fio = Column(Text, nullable=False)
    kafedra = Column(Text, nullable=False)
    dolzhnost = Column(Text, nullable=False)
    uch_stepen = Column(Text, nullable=True)

    lessons = relationship("Lesson", back_populates="teacher")


class Subject(Base):
    __tablename__ = "subject"

    id = Column(BigInteger, primary_key=True)
    nazvanie = Column(Text, nullable=False, unique=True)
    chislo_chasov = Column(Integer, nullable=False)
    vid_proverki = Column(Text, nullable=False)
    obyazatelnost = Column(Boolean, nullable=False)

    lessons = relationship("Lesson", back_populates="subject")


class Lesson(Base):
    __tablename__ = "lesson"

    id = Column(BigInteger, primary_key=True)

    teacher_id = Column(BigInteger, ForeignKey("teacher.id"), nullable=False)
    subject_id = Column(BigInteger, ForeignKey("subject.id"), nullable=False)

    data = Column(Date, nullable=False)
    vremya = Column(Time, nullable=False)
    auditoriya = Column(Text, nullable=False)
    vid_zanyatiya = Column(Text, nullable=False)
    gruppa = Column(Text, nullable=False)

    teacher = relationship("Teacher", back_populates="lessons")
    subject = relationship("Subject", back_populates="lessons")

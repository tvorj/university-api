import random
import requests
from faker import Faker

fake = Faker("ru_RU")

BASE_URL = "http://127.0.0.1:8000"

NUM_TEACHERS = 30
NUM_SUBJECTS = 30
NUM_LESSONS = 10000

session = requests.Session()

teacher_ids = []
subject_ids = []

kafedras = ["Системное программирование", "Математическая кибернетика", "Общая физика и квантовые наноструктуры", "Математика и математическое моделирование", "Микроэлектронные схемы и системы", "Телекоммуникация"]
dolzhnosti = ["ассистент", "преподаватель", "старший преподаватель", "доцент", "профессор", "лектор"]
vidy_proverki = ["экзамен", "зачёт", "зачёт с оценкой"]
vidy_zanyatii = ["лекция", "практика", "лабораторная"]
uch_stepens = ["Bachelor", "Master", "PhD", None]



for _ in range(NUM_TEACHERS):
    data = {
        "fio": fake.name(),
        "kafedra": random.choice(kafedras),
        "dolzhnost": random.choice(dolzhnosti),
        "uch_stepen": random.choice(uch_stepens),
    }
    r = session.post(f"{BASE_URL}/teachers", json=data, timeout=10)
    if r.status_code in (200, 201):
        teacher_ids.append(r.json()["id"])
    else:
        print("Teacher error:", r.status_code, r.text)



for _ in range(NUM_SUBJECTS):
    data = {
        "nazvanie": f"{fake.word().capitalize()} {random.randint(1, 10000)}",
        "chislo_chasov": random.choice([16, 32, 48, 64, 72, 96]),
        "vid_proverki": random.choice(vidy_proverki),
        "obyazatelnost": random.choice([True, False]),
    }
    r = session.post(f"{BASE_URL}/subjects", json=data, timeout=10)
    if r.status_code in (200, 201):
        subject_ids.append(r.json()["id"])
    else:
        print("Subject error:", r.status_code, r.text)



for _ in range(NUM_LESSONS):
    if not teacher_ids or not subject_ids:
        break

    data = {
        "teacher_id": random.choice(teacher_ids),
        "subject_id": random.choice(subject_ids),
        "data": fake.date_between(start_date="-60d", end_date="+60d").isoformat(),
        "vremya": fake.time(pattern="%H:%M:%S"),
        "auditoriya": str(random.randint(100, 999)),
        "vid_zanyatiya": random.choice(vidy_zanyatii),
        "gruppa": f"{random.choice(['A','B','C'])}-{random.randint(100, 400):02d}",
    }
    r = session.post(f"{BASE_URL}/lessons", json=data, timeout=10)
    if r.status_code not in (200, 201):
        print("Lesson error:", r.status_code, r.text)

print("Database filled")
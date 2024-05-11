from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from faker import Faker
from models import Student, Group, Teacher, Subject, Grade
from datetime import datetime, timedelta
import random

engine = create_engine('postgresql+psycopg2://postgres:example@localhost:5432/students')
fake = Faker()


def create_students(n):
	for _ in range(n):
		student = Student(fullname=fake.name(), group_id=random.randint(1, 3))
		session.add(student)
	session.commit()


def create_groups():
	groups = ['Group 1', 'Group 2', 'Group 3']
	for group_name in groups:
		group = Group(name=group_name)
		session.add(group)
	session.commit()


def create_teachers(n):
	for _ in range(n):
		teacher = Teacher(fullname=fake.name())
		session.add(teacher)
	session.commit()


def create_subjects(n):
	for _ in range(n):
		subject = Subject(name=fake.word(), teacher_id=random.randint(1, 3))
		session.add(subject)
	session.commit()


def create_grades(n):
	students = session.query(Student).all()
	subjects = session.query(Subject).all()
	for _ in range(n):
		student = random.choice(students)
		subject = random.choice(subjects)
		grade = Grade(grade=random.randint(0, 100), grade_date=datetime.now() - timedelta(random.randint(0, 365)),
		              student_id=student.id, subject_id=subject.id)
		session.add(grade)
	session.commit()


with Session(engine) as session:
	create_groups()
	create_teachers(3)
	create_subjects(8)
	create_students(50)
	create_grades(200)


from sqlalchemy import func, create_engine
from sqlalchemy.orm import Session
from models import Student, Group, Teacher, Subject, Grade

engine = create_engine('postgresql+psycopg2://postgres:example@localhost:5432/students')


def select_1():
	result = session.query(
		Student.fullname.label('student_name'),
		func.round(func.avg(Grade.grade), 2).label('average_grade')
	) \
		.join(Grade, Student.id == Grade.student_id) \
		.group_by(Student.id) \
		.order_by(func.avg(Grade.grade).desc()) \
		.limit(5) \
		.all()
	return result


def select_2():
	result = session.query(
		Student.fullname.label('student_name'),
		func.round(func.avg(Grade.grade), 2).label('average_grade')
	) \
		.join(Grade, Student.id == Grade.student_id) \
		.filter(Grade.subject_id == 8) \
		.group_by(Student.fullname) \
		.order_by(func.avg(Grade.grade).desc()) \
		.first()
	return result


def select_3():
	result = session.query(
		Student.group_id.label('group_id'),
		Subject.name.label('subject_name'),
		func.round(func.avg(Grade.grade), 2).label('average_grade')
	) \
		.join(Grade, Student.id == Grade.student_id) \
		.join(Subject, Grade.subject_id == Subject.id) \
		.filter(Subject.id == 8) \
		.group_by(Student.group_id, Subject.name) \
		.order_by(Student.group_id) \
		.all()
	return result


def select_4():
	result = session.query(
		func.round(func.avg(Grade.grade), 2)).scalar()
	return result


def select_5():
	result = session.query(
		Teacher.fullname.label('teacher_name'),
		Subject.name.label('subject_name')
	) \
		.join(Subject, Teacher.id == Subject.teacher_id) \
		.filter(Teacher.id == 2) \
		.all()
	return result


def select_6():
	result = session.query(
		Student.fullname.label('student_name'),
	) \
		.join(Group, Group.id == Student.group_id) \
		.filter(Group.id == 2) \
		.all()
	return result


def select_7():
	result = session.query(
		Student.fullname.label('student_name'),
		Group.name.label('group_name'),
		Grade.grade.label('grade'),
		Subject.name.label('subject_name')
	) \
		.join(Grade, Student.id == Grade.student_id) \
		.join(Group, Student.group_id == Group.id) \
		.join(Subject, Grade.subject_id == Subject.id) \
		.filter(Group.id == 1) \
		.filter(Subject.id == 1) \
		.filter(Student.fullname == 'Dana Soto') \
		.all()
	return result


def select_8():
	result = session.query(
		Teacher.fullname.label('teacher_name'),
		func.round(func.avg(Grade.grade), 2).label('average_grade')
	) \
		.join(Subject, Teacher.id == Subject.teacher_id) \
		.join(Grade, Grade.subject_id == Subject.id) \
		.filter(Teacher.id == 2) \
		.group_by(Teacher.fullname) \
		.order_by(func.avg(Grade.grade)) \
		.all()
	return result


def select_9():
	result = session.query(
		Subject.name.label('subject_name')
	) \
		.join(Grade, Subject.id == Grade.subject_id) \
		.join(Student, Student.id == Grade.student_id) \
		.filter(Student.id == 1) \
		.group_by(Subject.name) \
		.all()
	return result


def select_10():
	result = session.query(
		Subject.name.label('subject_name')
	) \
		.join(Grade, Subject.id == Grade.subject_id) \
		.join(Student, Student.id == Grade.student_id) \
		.join(Teacher, Teacher.id == Subject.teacher_id) \
		.filter(Student.id == 1) \
		.filter(Teacher.id == 3) \
		.group_by(Subject.name) \
		.all()
	return result


def select_11():
	result = session.query(func.round(func.avg(Grade.grade), 2).label('average_grade')) \
		.join(Student, Grade.student_id == Student.id) \
		.join(Subject, Grade.subject_id == Subject.id) \
		.join(Teacher, Subject.teacher_id == Teacher.id) \
		.filter(Student.id == 6) \
		.filter(Teacher.id == 3) \
		.scalar()
	return result


def select_12():
	lesson_date = session.query(func.max(Grade.grade_date)) \
		.join(Student, Grade.student_id == Student.id) \
		.join(Group, Student.group_id == Group.id) \
		.filter(Group.id == 1) \
		.filter(Grade.subject_id == 1) \
		.scalar_subquery()

	result = session.query(
		Student.fullname.label('student_name'),
		Grade.grade,
		Grade.grade_date
	) \
		.join(Group, Student.group_id == Group.id) \
		.join(Grade, Student.id == Grade.student_id) \
		.filter(Group.id == 1) \
		.filter(Grade.subject_id == 1) \
		.filter(Grade.grade_date == lesson_date) \
		.all()
	return result


if __name__ == '__main__':
	print('''   Ласкаво просимо до бази даних успішності студентів!
	1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
	2. Знайти студента із найвищим середнім балом з певного предмета.
	3. Знайти середній бал у групах з певного предмета.
	4. Знайти середній бал на потоці (по всій таблиці оцінок).
	5. Знайти які курси читає певний викладач.
	6. Знайти список студентів у певній групі.
	7. Знайти оцінки студентів у окремій групі з певного предмета.
	8. Знайти середній бал, який ставить певний викладач зі своїх предметів.
	9. Знайти список курсів, які відвідує студент.
	10. Список курсів, які певному студенту читає певний викладач.
	11. Середній бал, який певний викладач ставить певному студентові.
	12. Оцінки студентів у певній групі з певного предмета на останньому занятті.''')
	print('Для того щоб продовжити виберіть цифрою номер запиту. Або введіть "Вихід"')
	with Session(engine) as session:
		while True:
			while True:
				user_input = input("Виберіть команду запиту: ")
				if user_input:
					break
				else:
					print("Ви нічого не ввели")
			command = user_input

			if command in ("Вихід"):
				print("Допобачення!")
				break
			elif command == '1':
				print(select_1())
			elif command == '2':
				print(select_2())
			elif command == '3':
				print(select_3())
			elif command == '4':
				print(select_4())
			elif command == '5':
				print(select_5())
			elif command == '6':
				print(select_6())
			elif command == '7':
				print(select_7())
			elif command == '8':
				print(select_8())
			elif command == '9':
				print(select_9())
			elif command == '10':
				print(select_10())
			elif command == '11':
				print(select_11())
			elif command == '12':
				print(select_12())
			else:
				print("Invalid command.")

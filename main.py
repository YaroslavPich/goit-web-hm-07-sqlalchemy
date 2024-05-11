from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Student, Group, Teacher, Subject, Grade
import argparse

engine = create_engine('postgresql+psycopg2://postgres:example@localhost:5432/students')
Session = sessionmaker(bind=engine)
session = Session()

parser = argparse.ArgumentParser()
parser.add_argument('-a', '--action', default='list')
parser.add_argument('-m', '--model')
parser.add_argument('-n', '--name')
parser.add_argument('--id', '--id', type=int)
parser.add_argument('-f', '--fullname')
parser.add_argument('-g', '--grade', type=int)
parser.add_argument('-d', '--grade_date')


def list_records(model):
	result = session.query(model).all()
	session.close()
	return result


def print_records(model):
	for record in list_records(model):
		print(record)


def get_model(model_name):
	if model_name == 'student':
		return Student
	if model_name == 'subject':
		return Subject
	if model_name == 'teacher':
		return Teacher
	if args.model == 'group':
		return Group
	if args.model == 'grade':
		return Grade


def get_field_to_update(model, args):
	if model in (Subject, Group):
		return {
			'name': args.name
		}
	if model in (Student, Teacher):
		return {
			'fullname': args.fullname
		}
	if model is Grade:
		return {
			'grade': args.grade
		}
	if model is Grade:
		return {
			'grade_date': args.grade_date
		}


def update_instance(model, instance_id, fields_to_update):
	instance = session.get(model, instance_id)
	if not instance:
		return
	for field_name, field_value in fields_to_update.items():
		if hasattr(instance, field_name):
			setattr(instance, field_name, field_value)
	session.add(instance)
	session.commit()


def create_instance(model, fields_to_update):
	instance = model()
	if not instance:
		return
	for field_name, field_value in fields_to_update.items():
		if hasattr(instance, field_name):
			setattr(instance, field_name, field_value)
	session.add(instance)
	session.commit()


def remove_instance(model, instance_id):
	instance = session.get(model, instance_id)
	if not instance:
		return
	session.delete(instance)
	session.commit()


if __name__ == '__main__':
	args = parser.parse_args()
	model_to_display = get_model(args.model)
	field_to_update = get_field_to_update(model_to_display, args)
	instance_id = args.id
	if args.action == 'list':
		print_records(model_to_display)
	if args.action == 'update':
		update_instance(model_to_display, instance_id, field_to_update)
	if args.action == 'create':
		create_instance(model_to_display, field_to_update)
	if args.action == 'remove':
		remove_instance(model_to_display, instance_id)

from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Student(Base):
	__tablename__ = 'students'
	id = Column(Integer, primary_key=True)
	fullname = Column(String(150), nullable=False)
	group_id = Column('group_id', ForeignKey('groups.id', ondelete='CASCADE'))
	group = relationship('Group', backref='students')

	def __repr__(self):
		return f'Student {self.id} {self.fullname}'


class Group(Base):
	__tablename__ = 'groups'
	id = Column(Integer, primary_key=True)
	name = Column(String(50), nullable=False)

	def __repr__(self):
		return f'Group {self.id} {self.name}'


class Teacher(Base):
	__tablename__ = 'teachers'
	id = Column(Integer, primary_key=True)
	fullname = Column(String(150), nullable=False)

	def __repr__(self):
		return f'Teacher {self.id} {self.fullname}'

class Subject(Base):
	__tablename__ = 'subjects'
	id = Column(Integer, primary_key=True)
	name = Column(String(175), nullable=False)
	teacher_id = Column('teacher_id', ForeignKey('teachers.id', ondelete='CASCADE'))
	teacher = relationship('Teacher', backref='subjects')

	def __repr__(self):
		return f'Subject {self.id} {self.name}'

class Grade(Base):
	__tablename__ = 'grades'
	id = Column(Integer, primary_key=True)
	grade = Column(Integer, nullable=False)
	grade_date = Column('grade_date', Date, nullable=True)
	student_id = Column('student_id', ForeignKey('students.id', ondelete='CASCADE'))
	subject_id = Column('subject_id', ForeignKey('subjects.id', ondelete='CASCADE'))
	student = relationship('Student', backref='grade')
	subject = relationship('Subject', backref='grade')

	def __repr__(self):
		return f'Student {self.id} {self.grade} {self.grade_date}'
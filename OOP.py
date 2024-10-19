import json
import re 
from typing import List


class Person:
    def __init__(self, name: str, age: int, email: str):
        self.name = name
        self.age = self.validate_age(age)
        self._email = self.validate_email(email)


    def introduce(self):
        print(f'Hello, i am  {self.name} i am {self.age} and my email is {self._email}.')


    @staticmethod
    def validate_email(email: str) -> str:
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if re.match(email_regex, email):
            return email
        else:
            raise ValueError(f"Invalid email format: {email}")


    @staticmethod
    def validate_age(age: int) -> int:
        if isinstance(age, int) and age >= 0:
            return age
        else:
            raise ValueError(f"Invalid age: {age} please enter a valid age.")


    @staticmethod
    def save_data(filename, data):
        with open(filename, 'w') as file:
            json.dump(data, file, default=lambda obj: obj.__dict__, indent=4)


    @staticmethod
    def load_data(filename):
        with open(filename, 'r') as file:
            return json.load(file)


class Instructor(Person):
    def __init__(self, name: str, age: int, email: str, instructor_id: str, assigned_courses: List['Course'] = None):
        super().__init__(name, age, email)
        self.instructor_id = instructor_id
        self.assigned_courses = assigned_courses if assigned_courses is not None else []


    def assign_course(self, course: 'Course'):
        self.assigned_courses.append(course)
        
class Course:
    def __init__(self, course_id: str, course_name: str, instructor: Instructor, enrolled_students: List['Student'] = None):
        self.course_id = course_id
        self.course_name = course_name
        self.instructor = instructor
        self.enrolled_students = enrolled_students if enrolled_students is not None else []


    def add_student(self, student: 'Student'):
        self.enrolled_students.append(student)
        
class Student(Person):
    def __init__(self, name: str, age: int, email: str, student_id: str, registered_courses: List[Course] = None):
        super().__init__(name, age, email)
        self.student_id = student_id
        self.registered_courses = registered_courses if registered_courses is not None else []


    def register_course(self, course: Course):
        self.registered_courses.append(course)
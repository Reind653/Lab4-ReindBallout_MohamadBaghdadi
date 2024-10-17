import sys
import csv
import re
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from OOP import *

class MainWindow(QMainWindow):
    """
    Main window for the School Management System.

    This class provides the main interface for managing students, instructors,
    courses, and school records. It includes functionality for adding, displaying,
    editing, and saving data.

    Attributes:
        available_courses (list): A list of available courses.
        instructors (list): A list of instructor objects.
        students (list): A list of student objects.
    """

    def __init__(self):

        """
        Initializes the main window and sets up the user interface (UI).
        """
        super().__init__()
        self.available_courses = []  
        self.instructors = []  
        self.students = []  
        self.initUI()

    def initUI(self):

        """
        Sets up the user interface of the application.

        This method creates the main layout of the window, including tabs for
        student, instructor, and course management. It also adds buttons for
        saving, loading, and exporting data.

        Tabs:
            - Student: Form to add student data.
            - Instructor: Form to add instructor data.
            - Course: Form to add course data.
            - Records: Displays school records.

        Buttons:
            - Save Data: Saves current data to a file.
            - Load Data: Loads data from a file.
            - Export to CSV: Exports current data to a CSV file.
        """

        self.setWindowTitle('School Management System')
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: lightblue;")
        self.available_courses = [
            {'course_id': 'CS101', 'course_name': 'Introduction to Computer Science'},
            {'course_id': 'MATH101', 'course_name': 'Calculus I'},
            {'course_id': 'PHYS101', 'course_name': 'Physics I'}
        ]
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        tabs = QTabWidget()
        layout.addWidget(tabs)

        tabs.addTab(self.createStudentForm(), 'Student')
        tabs.addTab(self.createInstructorForm(), 'Instructor')
        tabs.addTab(self.createCourseForm(), 'Course')
        tabs.addTab(self.createRecordDisplay(), 'Records')

        self.updateCourseDropdown()

        self.save_button = QPushButton("Save Data")
        self.load_button = QPushButton("Load Data")
        self.save_button.setStyleSheet("background-color: blue; color: white;")
        self.load_button.setStyleSheet("background-color: blue; color: white;")


        
        layout.addWidget(self.save_button)
        layout.addWidget(self.load_button)

        self.save_button.clicked.connect(self.saveData)
        self.load_button.clicked.connect(self.loadData)

        export_button = QPushButton("Export to CSV")
        export_button.clicked.connect(self.export_to_csv)
        export_button_layout = QHBoxLayout()
        export_button_layout.addWidget(export_button)
        layout.addLayout(export_button_layout)

    def createStudentForm(self):

        """
        Creates the form for adding student details.

        This method sets up the input fields for adding a new student, including
        fields for name, age, email, and student ID. A dropdown allows for selecting
        a course the student will be registered for.

        Returns:
            QWidget: The widget containing the student form layout.
        """

        form_widget = QWidget()
        layout = QFormLayout()
        
        self.student_name = QLineEdit()
        self.student_age = QLineEdit()
        self.student_email = QLineEdit()
        self.student_id = QLineEdit()
        
        layout.addRow(QLabel('Name:'), self.student_name)
        layout.addRow(QLabel('Age:'), self.student_age)
        layout.addRow(QLabel('Email:'), self.student_email)
        layout.addRow(QLabel('ID:'), self.student_id)
        
        self.course_dropdown = QComboBox()
        self.updateCourseDropdown()
        layout.addRow(QLabel('Register for Course:'), self.course_dropdown)
        
        submit_button = QPushButton('Add Student')
        submit_button.clicked.connect(self.addStudent)
        layout.addWidget(submit_button)
        
        form_widget.setLayout(layout)
        return form_widget

    def createInstructorForm(self):

        """
        Creates the form for adding instructor details.

        This method sets up the input fields for adding a new instructor, including
        fields for name, age, email, and instructor ID. A dropdown allows for assigning
        the instructor to a course.

        Returns:
            QWidget: The widget containing the instructor form layout.
        """

        form_widget = QWidget()
        layout = QFormLayout()

        self.instructor_name = QLineEdit()
        self.instructor_age = QLineEdit()
        self.instructor_email = QLineEdit()
        self.instructor_id = QLineEdit()
        
        layout.addRow(QLabel('Name:'), self.instructor_name)
        layout.addRow(QLabel('Age:'), self.instructor_age)
        layout.addRow(QLabel('Email:'), self.instructor_email)
        layout.addRow(QLabel('ID:'), self.instructor_id)
        
        self.instructor_course_dropdown = QComboBox()
        self.updateCourseDropdown()  # Populate dropdown with courses
        layout.addRow(QLabel('Assign Course:'), self.instructor_course_dropdown)

        submit_button = QPushButton('Add Instructor')
        submit_button.clicked.connect(self.addInstructor)
        layout.addWidget(submit_button)
        
        form_widget.setLayout(layout)
        return form_widget

    def createCourseForm(self):

        """
        Creates the form for adding course details.

        This method sets up the input fields for adding a new course, including
        fields for course ID, course name, instructor, and enrolled students.

        Returns:
            QWidget: The widget containing the course form layout.
        """

        form_widget = QWidget()
        layout = QFormLayout()
        
        self.course_id = QLineEdit()
        self.course_name = QLineEdit()
        self.course_instructor = QLineEdit()  
        self.course_enrolled_students = QLineEdit()  
        
        layout.addRow(QLabel('Course ID:'), self.course_id)
        layout.addRow(QLabel('Course Name:'), self.course_name)
        layout.addRow(QLabel('Instructor ID:'), self.course_instructor)
        layout.addRow(QLabel('Enrolled Students IDs:'), self.course_enrolled_students)
        
        submit_button = QPushButton('Add Course')
        submit_button.clicked.connect(self.addCourse)
        layout.addWidget(submit_button)
        
        form_widget.setLayout(layout)
        return form_widget

    def createRecordDisplay(self):

        """
        Creates and returns the layout for displaying and managing records.

        This method sets up the layout containing the search field, buttons to edit
        and delete records, and the table widget that displays the records.

        Returns:
            QWidget: The widget containing the record management interface.
        """

        form_widget = QWidget()
        layout = QVBoxLayout()
        
        search_layout = QHBoxLayout()
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText('Search by name, ID, or course')
        search_button = QPushButton('Search')
        search_button.clicked.connect(self.searchRecords)
        search_layout.addWidget(self.search_field)
        search_layout.addWidget(search_button)
        
        layout.addLayout(search_layout)

        button_layout = QHBoxLayout()
        self.edit_button = QPushButton('Edit Record')
        self.delete_button = QPushButton('Delete Record')
        self.edit_button.clicked.connect(self.editRecord)
        self.delete_button.clicked.connect(self.deleteRecord)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        
        layout.addLayout(button_layout)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(6)  
        self.table_widget.setHorizontalHeaderLabels(['Type', 'ID', 'Name', 'Age', 'Email', 'Assigned Courses'])
        layout.addWidget(self.table_widget)
        
        form_widget.setLayout(layout)
        self.updateRecordDisplay()  
        
        return form_widget

    def updateCourseDropdown(self):

        """
        Updates the dropdown menus for course selection in the student and instructor forms.

        This method clears the existing dropdown items and populates them with the current
        list of available courses. If the dropdowns already exist, it updates them.
        """

        if hasattr(self, 'course_dropdown'):
            self.course_dropdown.clear()
        
        if hasattr(self, 'instructor_course_dropdown'):
            self.instructor_course_dropdown.clear()
        
        for course in self.available_courses:
            if hasattr(self, 'course_dropdown'):
                self.course_dropdown.addItem(f"{course['course_id']} - {course['course_name']}", course['course_id'])
            if hasattr(self, 'instructor_course_dropdown'):
                self.instructor_course_dropdown.addItem(f"{course['course_id']} - {course['course_name']}", course['course_id'])


    def addStudent(self):

        """
        Adds a new student to the list based on the input from the form.

        This method retrieves the student's details from the input form (name, age, email, 
        student ID, and selected course) and adds the student to the `students` list. It 
        also displays a success message upon completion.

        Raises:
            ValueError: If any required field is missing or invalid.
        """

        selected_course_id = self.course_dropdown.currentData()
        student_name = self.student_name.text()
        student_age = self.student_age.text()
        student_email = self.student_email.text()
        student_id = self.student_id.text()
        
        student = Student(name=student_name, age=int(student_age), email=student_email, student_id=student_id)
        self.students.append(student)
        QMessageBox.information(self, 'Success', f'Student added successfully! Registered for course ID: {selected_course_id}')
        self.updateRecordDisplay()
        
    def addInstructor(self):

        """
        Adds a new instructor to the list based on the input from the form.

        This method retrieves the instructor's details from the input form (name, age, 
        email, instructor ID, and assigned course) and adds the instructor to the 
        `instructors` list. It also assigns the instructor to a course.

        Raises:
            ValueError: If any required field is missing or invalid.
        """

        selected_course_id = self.instructor_course_dropdown.currentData()
        
        instructor_name = self.instructor_name.text()
        instructor_age = self.instructor_age.text()
        instructor_email = self.instructor_email.text()
        instructor_id = self.instructor_id.text()
        
        instructor = Instructor(name=instructor_name, age=int(instructor_age), email=instructor_email, instructor_id=instructor_id)
        self.instructors.append(instructor)
        
        for course in self.available_courses:
            if course['course_id'] == selected_course_id:
                for inst in self.instructors:
                    if inst.instructor_id == instructor_id:
                        inst.assign_course(course)
                        break
                break
        
        QMessageBox.information(self, 'Success', f'Instructor added successfully! Assigned to course ID: {selected_course_id}')
        self.updateRecordDisplay()

    def addCourse(self):

        """
        Adds a new course to the available courses list based on the input from the form.

        This method retrieves the course details (course ID, course name, instructor, and 
        enrolled students) from the input form, creates the course, and assigns the students 
        to it.

        Raises:
            ValueError: If any required field is missing or invalid.
        """

        course_id = self.course_id.text()
        course_name = self.course_name.text()
        instructor_id = self.course_instructor.text()
        enrolled_students_ids = self.course_enrolled_students.text().split(',')

        instructor = None
        for inst in self.instructors:
            if inst.instructor_id == instructor_id:
                instructor = inst
                break

        if not instructor:
            QMessageBox.warning(self, 'Error', 'Instructor not found!')
            return

        enrolled_students = []
        for student_id in enrolled_students_ids:
            student = next((s for s in self.students if s.student_id == student_id.strip()), None)
            if student:
                enrolled_students.append(student)
                student.register_course(course_id)  

        course = Course(course_id=course_id, course_name=course_name, instructor=instructor, enrolled_students=enrolled_students)
        self.available_courses.append({
            'course_id': course_id,
            'course_name': course_name,
            'instructor_id': instructor_id,
            'enrolled_students_ids': enrolled_students_ids
        })

        QMessageBox.information(self, 'Success', 'Course added successfully!')
        self.updateRecordDisplay()

    def searchRecords(self):

        """
        Searches through the student, instructor, and course records based on the search term.

        This method filters the records to display only those that match the search term 
        (either by name, ID, or course). The matching records are displayed in the table widget.
        """

        search_term = self.search_field.text().lower()
        self.table_widget.clear()
        self.table_widget.setRowCount(0)
        self.table_widget.setColumnCount(6)
        self.table_widget.setHorizontalHeaderLabels(['Type', 'ID', 'Name', 'Age', 'Email', 'Assigned Courses'])

        for student in self.students:
            if (search_term in student.name.lower() or
                search_term in student.student_id.lower()):
                row_position = self.table_widget.rowCount()
                self.table_widget.insertRow(row_position)
                self.table_widget.setItem(row_position, 0, QTableWidgetItem('Student'))
                self.table_widget.setItem(row_position, 1, QTableWidgetItem(student.student_id))
                self.table_widget.setItem(row_position, 2, QTableWidgetItem(student.name))
                self.table_widget.setItem(row_position, 3, QTableWidgetItem(str(student.age)))
                self.table_widget.setItem(row_position, 4, QTableWidgetItem(student._email))
                self.table_widget.setItem(row_position, 5, QTableWidgetItem('N/A'))

        for instructor in self.instructors:
            if (search_term in instructor.name.lower() or
                search_term in instructor.instructor_id.lower()):
                row_position = self.table_widget.rowCount()
                self.table_widget.insertRow(row_position)
                self.table_widget.setItem(row_position, 0, QTableWidgetItem('Instructor'))
                self.table_widget.setItem(row_position, 1, QTableWidgetItem(instructor.instructor_id))
                self.table_widget.setItem(row_position, 2, QTableWidgetItem(instructor.name))
                self.table_widget.setItem(row_position, 3, QTableWidgetItem(str(instructor.age)))
                self.table_widget.setItem(row_position, 4, QTableWidgetItem(instructor._email))
                self.table_widget.setItem(row_position, 5, QTableWidgetItem(', '.join([c['course_name'] for c in self.available_courses if c['course_id'] in instructor.courses])))

        for course in self.available_courses:
            if (search_term in course['course_name'].lower() or
                search_term in course['course_id'].lower()):
                row_position = self.table_widget.rowCount()
                self.table_widget.insertRow(row_position)
                self.table_widget.setItem(row_position, 0, QTableWidgetItem('Course'))
                self.table_widget.setItem(row_position, 1, QTableWidgetItem(course['course_id']))
                self.table_widget.setItem(row_position, 2, QTableWidgetItem(course['course_name']))
                self.table_widget.setItem(row_position, 3, QTableWidgetItem('N/A'))  # Placeholder for course info
                self.table_widget.setItem(row_position, 4, QTableWidgetItem('N/A'))  # Placeholder for course info
                self.table_widget.setItem(row_position, 5, QTableWidgetItem('N/A'))  # Placeholder for enrolled students


    def updateRecordDisplay(self):
        
        """
        Updates the table widget to display the current student, instructor, and course records.

        This method clears the table widget and repopulates it with the latest records from
        the `students`, `instructors`, and `available_courses` lists.
        """

        self.table_widget.setRowCount(0)
            
        for student in self.students:
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            self.table_widget.setItem(row_position, 0, QTableWidgetItem('Student'))
            self.table_widget.setItem(row_position, 1, QTableWidgetItem(student.student_id))
            self.table_widget.setItem(row_position, 2, QTableWidgetItem(student.name))
            self.table_widget.setItem(row_position, 3, QTableWidgetItem(str(student.age)))
            self.table_widget.setItem(row_position, 4, QTableWidgetItem(student._email))

        for instructor in self.instructors:
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            self.table_widget.setItem(row_position, 0, QTableWidgetItem(instructor.instructor_id))
            self.table_widget.setItem(row_position, 1, QTableWidgetItem(instructor.name))
            self.table_widget.setItem(row_position, 2, QTableWidgetItem(str(instructor.age)))
            self.table_widget.setItem(row_position, 3, QTableWidgetItem(instructor._email))
            self.table_widget.setItem(row_position, 4, QTableWidgetItem('Instructor'))

        for course in self.available_courses:
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            self.table_widget.setItem(row_position, 0, QTableWidgetItem('Course'))
            self.table_widget.setItem(row_position, 1, QTableWidgetItem(course['course_id']))
            self.table_widget.setItem(row_position, 2, QTableWidgetItem(course['course_name']))
            self.table_widget.setItem(row_position, 3, QTableWidgetItem('N/A'))  # No direct age info for courses
            self.table_widget.setItem(row_position, 4, QTableWidgetItem('N/A'))  # No direct email info for courses

            instructor_id = course.get('instructor_id', 'N/A')
            enrolled_students_ids = course.get('enrolled_students_ids', [])
            additional_info = f"Instructor ID: {instructor_id}\nEnrolled Students: {', '.join(enrolled_students_ids)}"
            self.table_widget.setItem(row_position, 5, QTableWidgetItem(additional_info))

    def editRecord(self):

        """
        Allows the user to edit the selected student or instructor record.

        This method retrieves the selected record from the table, opens a dialog for the user
        to update the details (name, age, email), and updates the record upon confirmation.
        """

        selected_row = self.table_widget.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, 'Edit Record', 'No record selected!')
            return
        
        record_type = self.table_widget.item(selected_row, 4).text()
        record_id = self.table_widget.item(selected_row, 0).text()
        
        if record_type == 'Student':
            student = next((s for s in self.students if s.student_id == record_id), None)
            if student:
                # Open a dialog or new form to edit the student record
                new_name, ok = QInputDialog.getText(self, 'Edit Student', 'Enter new name:', text=student.name)
                if ok and new_name.strip():
                    student.name = new_name.strip()
                else:
                    QMessageBox.warning(self, 'Edit Student', 'Invalid name!')
                    return
                new_age, ok = QInputDialog.getText(self, 'Edit Student', 'Enter new age:', text=str(student.age))
                booll=new_age.isdigit() and int(new_age) > 0
                if ok and booll:
                    student.age = int(new_age)
                else:
                    QMessageBox.warning(self, 'Edit Student', 'Invalid age!')
                    return

            new_email, ok = QInputDialog.getText(self, 'Edit Student', 'Enter new email:', text=student._email)
            booll= re.match(r"[^@]+@[^@]+\.[^@]+", new_email) is not None
            if ok and booll:
                student._email = new_email
            else:
                QMessageBox.warning(self, 'Edit Student', 'Invalid email!')
                return
        elif record_type == 'Instructor':
            instructor = next((i for i in self.instructors if i.instructor_id == record_id), None)
            if instructor:
                # Open a dialog or new form to edit the instructor record
                new_name, ok = QInputDialog.getText(self, 'Edit Instructor', 'Enter new name:', text=instructor.name)
                if ok and new_name.strip():
                    instructor.name = new_name.strip()
                else:
                    QMessageBox.warning(self, 'Edit Instructor', 'Invalid name!')
                    return
                new_age, ok = QInputDialog.getText(self, 'Edit Instructor', 'Enter new age:', text=str(instructor.age))
                booll=new_age.isdigit() and int(new_age) > 0
            if ok and booll:
                instructor.age = int(new_age)
            else:
                QMessageBox.warning(self, 'Edit Instructor', 'Invalid age!')
                return

            new_email, ok = QInputDialog.getText(self, 'Edit Instructor', 'Enter new email:', text=instructor._email)
            booll= re.match(r"[^@]+@[^@]+\.[^@]+", new_email) is not None
            if ok and booll:
                instructor._email = new_email
            else:
                QMessageBox.warning(self, 'Edit Instructor', 'Invalid email!')
                return
        self.updateRecordDisplay()
    
    def deleteRecord(self):

        """
        Deletes the selected student or instructor record from the list.

        This method removes the selected record from either the `students` or `instructors` list 
        and updates the table widget to reflect the changes.
        """

        selected_row = self.table_widget.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, 'Delete Record', 'No record selected!')
            return
        
        record_type = self.table_widget.item(selected_row, 4).text()
        record_id = self.table_widget.item(selected_row, 0).text()
        
        if record_type == 'Student':
            self.students = [s for s in self.students if s.student_id != record_id]
        elif record_type == 'Instructor':
            self.instructors = [i for i in self.instructors if i.instructor_id != record_id]
        
        self.updateRecordDisplay()
        QMessageBox.information(self, 'Success', f'{record_type} record deleted successfully!')

    def saveData(self):

        """
        Saves the current data to a JSON file.

        This method collects the student, instructor, and course records from the application's
        lists and serializes them into a JSON file. It handles any file I/O exceptions that may occur
        and notifies the user upon success or failure.

        Raises:
            Exception: If an error occurs during the file save operation.
        """

        try:
            data = {
                'students': [],
                'instructors': [],
                'courses': []
            }

            for student in self.students:
                data['students'].append({
                    'student_id': student.student_id,
                    'name': student.name,
                    'age': student.age,
                    'email': student._email,
                    'registered_courses': [course.course_id for course in student.registered_courses]
                })

            for instructor in self.instructors:
                data['instructors'].append({
                    'instructor_id': instructor.instructor_id,
                    'name': instructor.name,
                    'assigned_courses': [course.course_id for course in instructor.assigned_courses]
                })

            for course in self.available_courses:
                data['courses'].append({
                    'course_id': course['course_id'],
                    'course_name': course['course_name'],
                    'instructor_id': course['instructor'].instructor_id if course.get('instructor') else None,
                    'enrolled_students': [student.student_id for student in course.get('enrolled_students', [])]
                })

            with open('school_data.json', 'w') as file:
                json.dump(data, file)

            QMessageBox.information(self, 'Success', 'Data saved successfully!')

        except Exception as e:
            QMessageBox.critical(self, 'Error', f"An error occurred while saving data: {str(e)}")

    def loadData(self):
        
        """
        Loads data from a JSON file.

        This method reads a JSON file selected by the user and populates the application's
        records with the loaded data. The data is applied to the student, instructor, and course lists,
        and the interface is updated to reflect the new state.

        Raises:
            Exception: If an error occurs during the file read operation.
        """

        file_name, _ = QFileDialog.getOpenFileName(self, "Open Data", "", "JSON Files (*.json)")
        if file_name:
                with open(file_name, 'r') as file:
                    data = json.load(file)

                self.students = []
                self.instructors = []
                self.available_courses = []

                for instructor_data in data.get('instructors', []):
                    instructor = Instructor(
                        instructor_id=instructor_data.get('instructor_id', ''),
                        name=instructor_data.get('name', ''),
                        age=instructor_data.get('age', None),  # Use None or a default value if 'age' is missing
                        _email=instructor_data.get('email', '')
                    )
                    self.instructors.append(instructor)

                for student_data in data.get('students', []):
                    student = Student(
                        student_id=student_data.get('student_id', ''),
                        name=student_data.get('name', ''),
                        age=student_data.get('age', None),  # Use None or a default value if 'age' is missing
                        _email=student_data.get('email', '')
                    )
                    self.students.append(student)

                for course_data in data.get('courses', []):
                    instructor = next((inst for inst in self.instructors if inst.instructor_id == course_data.get('instructor_id')), None)
                    
                    course = Course(
                        course_id=course_data.get('course_id', ''),
                        course_name=course_data.get('course_name', ''),
                        instructor=instructor,
                        enrolled_students=course_data.get('enrolled_students')
                    )
                    
                    for student_id in course_data.get('enrolled_students_ids', []):
                        student = next((stud for stud in self.students if stud.student_id == student_id), None)
                        if student:
                            course.add_student(student)
                            student.registered_courses.append(course)

                    self.available_courses.append(course)
                    if instructor:
                        instructor.assigned_courses.append(course)

                self.updateRecordDisplay()
                QMessageBox.information(self, "Success", "Data loaded successfully!")

    def export_to_csv(self):

        """
        Exports the current school data to a CSV file.

        This method allows the user to save the student, instructor, and course
        records into a CSV file, with each type of data written into a separate row.

        Raises:
            Exception: If an error occurs during the exporting process.
        """

        # Prompt user to select file location
        file_name, _ = QFileDialog.getSaveFileName(self, "Save CSV File", "", "CSV Files (*.csv)")
        if file_name:
            try:
                with open(file_name, 'w', newline='') as file:
                    writer = csv.writer(file)
                    # Write header
                    writer.writerow(["Type", "ID", "Name", "Age", "Email", "Instructor", "Course Name", "Students"])

                    # Write student records
                    for student in self.students:
                        writer.writerow([
                            "Student", 
                            student.student_id, 
                            student.name, 
                            student.age, 
                            student._email, 
                            '', 
                            '', 
                            ''
                        ])

                    # Write instructor records
                    for instructor in self.instructors:
                        writer.writerow([
                            "Instructor", 
                            instructor.instructor_id, 
                            instructor.name, 
                            instructor.age, 
                            instructor._email, 
                            '', 
                            '', 
                            ''
                        ])

                    # Write course records
                    for course in self.available_courses:
                        # Check if course is a dictionary or object
                        if isinstance(course, dict):
                            enrolled_students_list = ', '.join(
                                student['name'] for student in course.get('enrolled_students', [])
                            )
                            writer.writerow([
                                "Course", 
                                course.get('course_id', ''), 
                                course.get('course_name', ''), 
                                '', 
                                '', 
                                course.get('instructor', {}).get('name', ''), 
                                course.get('course_name', ''), 
                                enrolled_students_list
                            ])
                        else:
                            enrolled_students_list = ', '.join(
                                student.name for student in course.enrolled_students
                            )
                            writer.writerow([
                                "Course", 
                                course.course_id, 
                                course.course_name, 
                                '', 
                                '', 
                                course.instructor.name if course.instructor else '', 
                                course.course_name, 
                                enrolled_students_list
                            ])

                QMessageBox.information(self, "Success", "Data exported successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export data: {str(e)}")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

import re
import os
import sys
import csv
from PyQt5 import QtWidgets
from UI_design import Ui_MainBox
from UI_updateStudent import Ui_UpdateBox
from UI_updateProgram import Ui_UpdateProgram
from UI_updateCollege import Ui_UpdateCollege

#CSV FILES AS DATABASE
STUDENTS_CSV_FILE = "students.csv"
PROGRAMS_CSV_FILE = "programs.csv"
COLLEGES_CSV_FILE = "colleges.csv"

class MainApp(QtWidgets.QMainWindow, Ui_MainBox):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        #CONNECT BUTTONS TO FUNCTIONS
        self.clear_student_input()
        self.clear_program_input()
        self.searchStudents_combo.setCurrentIndex(-1)
        self.searchProgram_combo.setCurrentIndex(-1)
        self.searchCollege_combo.setCurrentIndex(-1)
        self.sortStudents_combo.setCurrentIndex(-1)
        self.sortProgram_combo.setCurrentIndex(-1)
        self.sortCollege_combo.setCurrentIndex(-1)
        self.refreshStudents_button.clicked.connect(self.refresh_student)
        self.refreshProgram_button.clicked.connect(self.refresh_program) 
        self.refreshCollege_button.clicked.connect(self.refresh_college)  
        self.sortStudents_combo.currentIndexChanged.connect(self.sort_student)
        self.sortProgram_combo.currentIndexChanged.connect(self.sort_program)
        self.sortCollege_combo.currentIndexChanged.connect(self.sort_college)
        self.tabWidget.currentChanged.connect(self.clear_all_selections)
        self.editProgram_button.clicked.connect(self.open_updateProgram_window)
        self.edit_button.clicked.connect(self.open_updateStudent_window)
        self.editCollege_button.clicked.connect(self.open_updateCollege_window)
        self.searchStudents_button.clicked.connect(self.search_student)
        self.searchProgram_button.clicked.connect(self.search_program)
        self.searchCollege_button.clicked.connect(self.search_college)
        self.addStudent_button.clicked.connect(self.add_student)
        self.delete_button.clicked.connect(self.delete_student_button)
        self.addProgram_button.clicked.connect(self.add_program)
        self.deleteProgram_button.clicked.connect(self.delete_program_button)
        self.addCollege_button.clicked.connect(self.add_college)
        self.deleteCollege_button.clicked.connect(self.delete_college_button)

        #INITIALIZE DATABASES
        self.students = []
        self.programs = []
        self.colleges = []

        #CHECK IF DATABASES EXIST
        if os.path.exists(STUDENTS_CSV_FILE):
            self.load_student()
        else:
            QtWidgets.QMessageBox.information(self, "File Error", "students.csv file not found")
        if os.path.exists(PROGRAMS_CSV_FILE):
            self.load_program()
            self.populate_program_code()
        else:
            QtWidgets.QMessageBox.information(self, "File Error", "programs.csv file not found")
        if os.path.exists(COLLEGES_CSV_FILE):
            self.load_college()
            self.populate_college_code()
        else:
            QtWidgets.QMessageBox.information(self, "File Error", "colleges.csv file not found")

#=======================================================================================================================================================================================================================

#=================================================================================================ADD STUDENTS========================================================================================================

    #SORT STUDENT TABLE
    def sort_student(self):
        sort_column = self.sortStudents_combo.currentIndex()
        if sort_column >= 0:
            self.studentTable_widget.sortItems(sort_column)

    #SEARCH STUDENTS
    def search_student(self):
        search_text = self.searchStudents_bar.text().strip().lower()
        search_column = self.searchStudents_combo.currentIndex()
        
        if not search_text:
            for row in range(self.studentTable_widget.rowCount()):
                self.studentTable_widget.setRowHidden(row, False)
            return
        
        matches_found = False
        matching_rows = []
        
        for row in range(self.studentTable_widget.rowCount()):
            item = self.studentTable_widget.item(row, search_column)
            if item and search_text in item.text().strip().lower():
                matches_found = True
                matching_rows.append(row)
        
        if matches_found:
            for row in range(self.studentTable_widget.rowCount()):
                self.studentTable_widget.setRowHidden(row, row not in matching_rows)
            self.search_succesful()
            self.searchStudents_bar.clear()
            self.searchStudents_combo.setCurrentIndex(-1)
        else:
            self.search_error()
            self.searchStudents_bar.clear()
            self.searchStudents_combo.setCurrentIndex(-1)

    #ADD STUDENT BUTTON
    def add_student(self):
        student_id = self.lineEdit_2.text().strip()
        student_first_name = self.lineEdit_3.text().strip().title()
        student_last_name = self.lineEdit_4.text().strip().title()
        student_gender = self.comboBox_2.currentText()
        student_year_level = self.comboBox.currentText()
        student_program_code = self.comboBox_5.currentText().upper()
        
        #VALIDATE IF INPUTS ARE VALID
        if not self.validate_student_id_format(student_id):
            self.add_error()
            return
        
        #ALLOW SPACE INPUT (DOUBLE NAME EX: JOHN DOE)
        if not all(char.isalpha() or char.isspace() for char in student_first_name):
            self.add_error()
            return
        
        if not (student_last_name.isalpha()):
            self.add_error()
            return
        
        #CHECK FOR EXISTING INPUTS
        if any(student[0] == student_id for student in self.students):
            self.input_exists()
            return

        if student_id and student_first_name and student_last_name and student_year_level and student_gender and student_program_code:
            student_data = [student_id, student_first_name, student_last_name, student_year_level, student_gender, student_program_code]

            self.students.append(student_data)
            self.save_students_csv()
            self.update_student_table()
            self.clear_student_input()
            self.add_succesful()
        else:
            self.add_error()

    #CLEAR STUDENT LINE BOXES EVERY AFTER SUCCESFUL ADD
    def clear_student_input(self):
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()
        self.comboBox_2.setCurrentIndex(-1)
        self.comboBox.setCurrentIndex(-1)
        self.comboBox_5.setCurrentIndex(-1)
        
    #DELETE STUDENT CONFIRMATION PROMPT
    def delete_student_confirmation(self):
        confirmation = QtWidgets.QMessageBox(self)
        confirmation.setWindowTitle("Confirm Deletion")
        confirmation.setText(f"Are you sure you want to delete this student?")
        confirmation.setIcon(QtWidgets.QMessageBox.Warning)
        confirmation.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        confirmation.setDefaultButton(QtWidgets.QMessageBox.No)
        confirmation.setStyleSheet("QLabel { color : white; }")
        confirmation.button(QtWidgets.QMessageBox.Yes).setStyleSheet("color: white;")
        confirmation.button(QtWidgets.QMessageBox.No).setStyleSheet("color: white;")
        
        result = confirmation.exec_()
        
        #IF DELETE == YES
        if result == QtWidgets.QMessageBox.Yes:
            self.delete_student()
    
    #OPEN UPDATE UI
    def open_updateStudent_window(self):
        selected_row = self.studentTable_widget.currentRow()
        if selected_row >= 0:
            student_data = self.students[selected_row]
            self.update_window = QtWidgets.QDialog(self)
            self.update_ui = Ui_UpdateBox()
            self.update_ui.setupUi(self.update_window)

            #POPULATE THE UPDATE WINDOW WITH SELECTED STUDENT'S DATA
            self.update_ui.updateStudentID_box.setText(student_data[0])
            self.update_ui.updateFirstNam_box.setText(student_data[1])
            self.update_ui.updateLastName_box.setText(student_data[2])
            self.update_ui.updateGender_combo.setCurrentText(student_data[4])
            self.update_ui.updateYearLevel_combo.setCurrentText(student_data[3])

            #POPULATE PROGRAM CODES COMBO BOX WITH THE PROGRAM CODES IN PROGRAMS CSV   
            self.update_ui.updateGender_combo_2.clear()
            with open(PROGRAMS_CSV_FILE, "r", newline='') as file:
                reader = csv.reader(file)
                next(reader, None)
                program_codes = sorted(set(row[0] for row in reader if len(row) > 0 and row[0].strip()))
                self.update_ui.updateGender_combo_2.addItems(program_codes)
            
            self.update_ui.updateGender_combo_2.setCurrentText(student_data[5])
            self.update_ui.update_button.clicked.connect(self.save_updated_student_button_clicked)
            self.update_window.exec_()
        else:
            self.selection_error()

    #SAVE UPDATED STUDENT
    def save_updated_student_button_clicked(self):
        selected_row = self.studentTable_widget.currentRow()
        self.save_updated_student(selected_row)

    def save_updated_student(self, row):
        student_id = self.update_ui.updateStudentID_box.text().strip()
        student_first_name = self.update_ui.updateFirstNam_box.text().strip().title()
        student_last_name = self.update_ui.updateLastName_box.text().strip().title()
        student_gender = self.update_ui.updateGender_combo.currentText()
        student_year_level = self.update_ui.updateYearLevel_combo.currentText()
        student_program_code = self.update_ui.updateGender_combo_2.currentText().upper()

        if not self.validate_student_id_format(student_id, edit_state=True):
            self.add_error()
            return

        if not all(char.isalpha() or char.isspace() for char in student_first_name):
            self.add_error()
            return

        if not student_last_name.isalpha():
            self.add_error()
            return

        # Check if the new student ID matches with any other student ID in the table
        if any(student[0] == student_id for i, student in enumerate(self.students) if i != row):
            self.input_exists()
            return

        if student_id and student_first_name and student_last_name and student_year_level and student_gender and student_program_code:
            self.students[row] = [student_id, student_first_name, student_last_name, student_year_level, student_gender, student_program_code]
            self.save_students_csv()
            self.save_programs_csv()
            self.save_colleges_csv()
            self.update_student_table()
            self.update_window.close()
            self.update_succesful()
        else:
            self.add_error()

    #VALIDATE IF STUDENT ID IS VALID (ONLY ACCEPTS YEAR STARTING FROM 2-XXX)
    def validate_student_id_format(self, student_id, edit_state=False):
        if not edit_state:
            valid_id_number = re.match(r'^2[0-9]{3}-[0-9]{4}$', student_id)
        else:
            valid_id_number = re.match(r'^2[0-9]{3}-[0-9]{4}$|^$', student_id)
        return True if valid_id_number else False
    
    #UPDATE STUDENT TABLE INFORMATION
    def update_student_table(self):
        self.studentTable_widget.setRowCount(len(self.students))
        for row, student in enumerate(self.students):
            for col, data in enumerate(student):
                self.studentTable_widget.setItem(row, col, QtWidgets.QTableWidgetItem(data))

    #DELETE STUDENT
    def delete_student(self):
        selected_student_row = self.studentTable_widget.currentRow()
        if selected_student_row >= 0:
            del self.students[selected_student_row]

            self.save_students_csv()
            self.update_student_table()
    
    #SAVE INPUT TO STUDENTS CSV   
    def save_students_csv(self):
        with open(STUDENTS_CSV_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Student ID", "First Name", "Last Name", "Year Level", "Gender", "Program Code"])
            writer.writerows(self.students)

    #LOAD STUDENTS DATABASE
    def load_student(self):
        with open(STUDENTS_CSV_FILE, mode="r") as file:
            reader = csv.reader(file)
            next(reader)
            self.students = [row for row in reader]
            self.update_student_table()

#======================================================================================================================================================================================================================

#=================================================================================================ADD PROGRAMS=========================================================================================================
    
    #SORT PROGRAM TABLE
    def sort_program(self):
        sort_column = self.sortProgram_combo.currentIndex()
        if sort_column >= 0:
            self.programTable_widget.sortItems(sort_column)

    #SEARCH PROGRAM
    def search_program(self):
        search_text = self.searchProgram_bar.text().strip().lower()
        search_column = self.searchProgram_combo.currentIndex()  # Get selected column index
        
        if not search_text:
            for row in range(self.programTable_widget.rowCount()):
                self.programTable_widget.setRowHidden(row, False)
            return
        
        matches_found = False
        matching_rows = []
        
        for row in range(self.programTable_widget.rowCount()):
            item = self.programTable_widget.item(row, search_column)
            if item and search_text in item.text().strip().lower():
                matching_rows.append(row)
                matches_found = True
        
        if matches_found:
            for row in range(self.programTable_widget.rowCount()):
                self.programTable_widget.setRowHidden(row, row not in matching_rows)
            self.search_succesful()
            self.searchProgram_bar.clear()
            self.searchProgram_combo.setCurrentIndex(-1)
        else:
            self.search_error()
    
    #UPDATE PROGRAM TABLE INFORMATION
    def update_program_table(self):
        self.programTable_widget.setRowCount(len(self.programs))
        for row, program in enumerate(self.programs):
            for col, data in enumerate(program):
                self.programTable_widget.setItem(row, col, QtWidgets.QTableWidgetItem(data))

    #POPULATE COMBOBOX_5 (STUDENTS' PROGRAM CODES FROM )
    def populate_program_code(self):
        with open(PROGRAMS_CSV_FILE, "r", newline='') as file:
            reader = csv.reader(file)
            next(reader, None)
            program_codes = sorted(set(row[0] for row in reader if len(row) > 0 and row[0].strip()))

            self.comboBox_5.clear()
            self.comboBox_5.addItem("")
            self.comboBox_5.addItems(program_codes)

    #ADD PROGRAM BUTTON
    def add_program(self):
        pr_program_code = self.lineEdit_6.text().strip().upper()
        pr_program_name = self.lineEdit.text().strip().title()
        program_college_code = self.comboBox_4.currentText().upper()

        #VALIDATE IF INPUTS ARE VALID
        if not (pr_program_code.isalpha()):
            self.add_error()
            return
        
        #ALLOW SPACE INPUT (BACHELOR OF ...)
        if not all(char.isalpha() or char.isspace() for char in pr_program_name):
            self.add_error()
            return

        if not pr_program_code or not pr_program_name or not program_college_code:
            self.add_error()
            return
        
        #CHECK IF THERE ARE EXISTING CODES
        existing_program_codes = set()
        if os.path.exists(PROGRAMS_CSV_FILE):
            with open(PROGRAMS_CSV_FILE, "r", newline='') as file:
                reader = csv.reader(file)
                existing_program_codes = {row[0] for row in reader if len(row) > 0}

        #CHECK IF THERE ARE EXISTING INPUTS
        if pr_program_code in existing_program_codes:
            self.add_error()
            return
        
        if pr_program_code and pr_program_name and program_college_code:
            program_data = [pr_program_code, pr_program_name, program_college_code]

            self.programs.append(program_data)
            self.save_programs_csv()
            self.update_program_table()
            self.populate_program_code()
            self.clear_program_input()
            self.add_succesful()
        else:
            self.add_error()

    #CLEAR PROGRAM LINE BOXES EVERY AFTER SUCCESFUL ADD
    def clear_program_input(self):
        self.lineEdit_6.clear()
        self.lineEdit.clear()
        self.comboBox_4.setCurrentIndex(-1)

    #OPEN UPDATE PROGRAM UI
    def open_updateProgram_window(self):
        selected_row = self.programTable_widget.currentRow()
        if selected_row >= 0:
            program_data = self.programs[selected_row]
            self.update_program_window = QtWidgets.QDialog(self)
            self.update_program_ui = Ui_UpdateProgram()
            self.update_program_ui.setupUi(self.update_program_window)

            #POPULATE THE UPDATE WINDOW WITH SELECTED PROGRAM'S DATA
            self.update_program_ui.updateProgramCode_box.setText(program_data[0])
            self.update_program_ui.updateProgramName_box.setText(program_data[1])
            self.update_program_ui.updateCollegeCode_box.setCurrentText(program_data[2])

            #POPULATE THE COLLEGE CODES COMBO BOX WITH THE COLLEGE CODES IN COLLEGES CSV
            self.update_program_ui.updateCollegeCode_box.clear()
            with open(COLLEGES_CSV_FILE, "r", newline='') as file:
                reader = csv.reader(file)
                next(reader, None)
                college_codes = sorted(set(row[0] for row in reader if len(row) > 0 and row[0].strip()))
                self.update_program_ui.updateCollegeCode_box.addItems(college_codes)
            
            self.update_program_ui.updateCollegeCode_box.setCurrentText(program_data[2])
            self.update_program_ui.updateProgram_button.clicked.connect(self.save_updated_program_button_clicked)
            self.update_program_window.exec_()
        else:
            self.selection_error()

    def save_updated_program_button_clicked(self):
        selected_row = self.programTable_widget.currentRow()
        self.save_updated_program(selected_row)

    #SAVE UPDATED PROGRAM
    def save_updated_program(self, row):
        program_code = self.update_program_ui.updateProgramCode_box.text().strip().upper()
        program_name = self.update_program_ui.updateProgramName_box.text().strip().title()
        college_code = self.update_program_ui.updateCollegeCode_box.currentText().upper()

        if not program_code.isalpha():
            self.add_error()
            return

        if not all(char.isalpha() or char.isspace() for char in program_name):
            self.add_error()
            return

        if program_code and program_name and college_code:
            old_program_code = self.programs[row][0]
            self.programs[row] = [program_code, program_name, college_code]

            #UPDATE STUDEMTS UNDER OLD PROGRAM CODE TO NEW PROGRAM CODE
            for student in self.students:
                if student[5] == old_program_code:
                    student[5] = program_code

            self.save_programs_csv()
            self.update_program_table()
            self.save_students_csv()
            self.save_colleges_csv()
            self.update_student_table()
            self.update_program_window.close()
            self.update_succesful()
        else:
            self.add_error()

    #DELETE PROGRAM CONFIRMATION PROMPT
    def delete_program_confirmation(self):
        confirmation = QtWidgets.QMessageBox(self)
        confirmation.setWindowTitle("Confirm Deletion")
        confirmation.setText(f"Are you sure you want to delete this program?")
        confirmation.setInformativeText("All affected students in this program will be marked as unenrolled")
        confirmation.setIcon(QtWidgets.QMessageBox.Warning)
        confirmation.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        confirmation.setDefaultButton(QtWidgets.QMessageBox.No)
        confirmation.setStyleSheet("QLabel { color : white; }")
        confirmation.button(QtWidgets.QMessageBox.Yes).setStyleSheet("color: white;")
        confirmation.button(QtWidgets.QMessageBox.No).setStyleSheet("color: white;")

        result = confirmation.exec_()
        
        #IF DELETE == YES
        if result == QtWidgets.QMessageBox.Yes:
            self.delete_program()

    #DELETE PROGRAM
    def delete_program(self):
        selected_program_row = self.programTable_widget.currentRow()
        if selected_program_row >= 0:
            deleted_program_code = self.programs[selected_program_row][0]
            del self.programs[selected_program_row]

            #SET AFFECTED STUDENTS UNDER DELETED PROGRAM CODE TO UNENROLLED
            for student in self.students:
                if student[5] == deleted_program_code:
                    student[5] = "UNENROLLED"

            #UPDATE CSV,TABLE,COMBOBOX
            self.save_students_csv()
            self.save_programs_csv()
            self.update_student_table()
            self.update_program_table()
            self.populate_program_code()

    #SAVE INPUT TO PROGRAM CSV
    def save_programs_csv(self):
        with open(PROGRAMS_CSV_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Program Code", "Program Name", "College Code"])
            writer.writerows(self.programs)

    #LOAD PROGRAM DATABASE
    def load_program(self):
        if os.path.exists(PROGRAMS_CSV_FILE):
            with open(PROGRAMS_CSV_FILE, mode="r") as file:
                reader = csv.reader(file)
                next(reader)
                self.programs = [row for row in reader]
                self.update_program_table()
                
#=======================================================================================================================================================================================================================

#=================================================================================================ADD COLLEGES==========================================================================================================

    #SORT COLLEGE TABLE
    def sort_college(self):
        sort_column = self.sortCollege_combo.currentIndex()
        if sort_column >= 0:
            self.collegeTable_widget.sortItems(sort_column)

    #SEARCH COLLEGE
    def search_college(self):
        search_text = self.searchCollege_bar.text().strip().lower()
        search_column = self.searchCollege_combo.currentIndex()
        
        if not search_text:
            for row in range(self.collegeTable_widget.rowCount()):
                self.collegeTable_widget.setRowHidden(row, False)
            return
        
        matches_found = False
        matching_rows = []
        
        for row in range(self.collegeTable_widget.rowCount()):
            item = self.collegeTable_widget.item(row, search_column)
            if item and search_text in item.text().strip().lower():
                matching_rows.append(row)
                matches_found = True
        
        if matches_found:
            for row in range(self.collegeTable_widget.rowCount()):
                self.collegeTable_widget.setRowHidden(row, row not in matching_rows)
            self.search_succesful()
            self.searchCollege_bar.clear()
            self.searchCollege_combo.setCurrentIndex(-1)
        else:
            self.search_error()

    #POPULATE COMBOBOX_4 (PROGRAMS' COLLEGE CODE)
    def populate_college_code(self):
        with open(COLLEGES_CSV_FILE, "r", newline='') as file:
            reader = csv.reader(file)
            next(reader, None)
            college_codes = sorted(set(row[0] for row in reader if len(row) > 0 and row[0].strip()))

        self.comboBox_4.clear()
        self.comboBox_4.addItem("")
        self.comboBox_4.addItems(college_codes)

    #ADD COLLEGE BUTTON
    def add_college(self):
        co_college_code = self.lineEdit_8.text().strip().upper()
        co_college_name = self.lineEdit_9.text().strip().title()

        #VALIDATE IF INPUTS ARE VALID
        if not co_college_code.isalpha():
            self.add_error()
            return
        
        if not all(char.isalpha() or char.isspace() for char in co_college_name):
            self.add_error()
            return
        
        #CHECK IF THERE ARE EXISTING CODES
        existing_college_codes = set()
        if os.path.exists(COLLEGES_CSV_FILE):
            with open(COLLEGES_CSV_FILE, "r", newline='') as file:
                reader = csv.reader(file)
                existing_college_codes = {row[0] for row in reader if len(row) > 0}

        if co_college_code in existing_college_codes:
            self.input_exists()
            return

        if co_college_code and co_college_name:
            college_data = [co_college_code, co_college_name]
            self.colleges.append(college_data)
            self.save_colleges_csv()
            self.update_college_table()
            self.populate_college_code()
            self.clear_college_inputs()
            self.add_succesful()
        else:
            self.add_error()

    #CLEAR COLLEGE LINE BOXES EVERY AFTER SUCCESFUL ADD
    def clear_college_inputs(self):
        self.lineEdit_8.clear()
        self.lineEdit_9.clear()

    #DELETE COLLEGE CONFIRMATION
    def delete_college_confirmation(self):
            confirmation = QtWidgets.QMessageBox(self)
            confirmation.setWindowTitle("Confirm Deletion")
            confirmation.setText(f"Are you sure you want to delete this college?")
            confirmation.setInformativeText("All affected affected programs in this college will be deleted and all affected students in this programs will be marked as unenrolled")
            confirmation.setIcon(QtWidgets.QMessageBox.Warning)
            confirmation.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            confirmation.setDefaultButton(QtWidgets.QMessageBox.No)
            confirmation.setStyleSheet("QLabel { color : white; }")
            confirmation.button(QtWidgets.QMessageBox.Yes).setStyleSheet("color: white;")
            confirmation.button(QtWidgets.QMessageBox.No).setStyleSheet("color: white;")
            
            result = confirmation.exec_()
            
            #IF DELETE == YES
            if result == QtWidgets.QMessageBox.Yes:
                self.delete_college()

    #DELETE COLLEGE
    def delete_college(self):
            selected_college_row = self.collegeTable_widget.currentRow()
            if selected_college_row >= 0:
                deleted_college_code = self.colleges[selected_college_row][0]
                
                #PROGRAMS AFFECTED UNDER DELETED COLLEGE
                program_in_college = [program[0] for program in self.programs if program[2] == deleted_college_code]
                
                #REMOVE MATCHING PROGRAMS IN COLLEGE CODE
                self.programs = [program for program in self.programs if program[2] != deleted_college_code]
                
                #SET AFFECTED STUDENTS UNDER PROGRAMS AFFECTED UNDER DELETED COLLEGE TO UNENROLLED
                for student in self.students:
                    if student[5] in program_in_college:
                        student[5] = "UNENROLLED"
                
                del self.colleges[selected_college_row]
                
                #UPDATE CSV,TABLE,COMBOBOX
                self.save_colleges_csv()
                self.save_programs_csv()
                self.save_students_csv()
                self.update_college_table()
                self.update_program_table()
                self.update_student_table()
                self.populate_college_code()
                self.populate_program_code()

    #OPEN UPDATE COLLEGE UI
    def open_updateCollege_window(self):
        selected_row = self.collegeTable_widget.currentRow()
        if selected_row >= 0:
            college_data = self.colleges[selected_row]
            self.update_college_window = QtWidgets.QDialog(self)
            self.update_college_ui = Ui_UpdateCollege()
            self.update_college_ui.setupUi(self.update_college_window)

            #POPULATE THE UPDATE WINDOW WITH THE SELECTED COLLEGE'S DATA
            self.update_college_ui.updateCollegeCode_box.setText(college_data[0])
            self.update_college_ui.updateCollegeName_box.setText(college_data[1])

            self.update_college_ui.updateCollege_button.clicked.connect(self.save_updated_college_button_clicked)
            self.update_college_window.exec_()
        else:
            self.selection_error()

    def save_updated_college_button_clicked(self):
        selected_row = self.collegeTable_widget.currentRow()
        self.save_updated_college(selected_row)

    #SAVE UPDATED COLLEGE
    def save_updated_college(self, row):
        college_code = self.update_college_ui.updateCollegeCode_box.text().strip().upper()
        college_name = self.update_college_ui.updateCollegeName_box.text().strip().title()

        if not college_code.isalpha():
            self.add_error()
            return

        if not all(char.isalpha() or char.isspace() for char in college_name):
            self.add_error()
            return

        if college_code and college_name:
            old_college_code = self.colleges[row][0]
            self.colleges[row] = [college_code, college_name]

            #UPDATE COLLEGE CODES IN PROGRAMS
            for program in self.programs:
                if program[2] == old_college_code:
                    program[2] = college_code

            self.save_colleges_csv()
            self.update_college_table()
            self.save_students_csv()
            self.save_programs_csv()
            self.update_program_table()
            self.update_college_window.close()
            self.update_succesful()
        else:
            self.add_error()

    #UPDATE COLLEGE TABLE INFORMATION
    def update_college_table(self):
        self.collegeTable_widget.setRowCount(len(self.colleges))
        for row, college in enumerate(self.colleges):
            for col, data in enumerate(college):
                self.collegeTable_widget.setItem(row, col, QtWidgets.QTableWidgetItem(data))

    #SAVE INPUT TO COLLEGES CSV
    def save_colleges_csv(self):
        with open(COLLEGES_CSV_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["College Code", "College Name"])
            writer.writerows(self.colleges)

    #LOAD PROGRAM DATABASE
    def load_college(self):
        if os.path.exists(COLLEGES_CSV_FILE):
            with open(COLLEGES_CSV_FILE, mode="r") as file:
                reader = csv.reader(file)
                next(reader)
                self.colleges = [row for row in reader]
                self.update_college_table()

#==============================================================================================CLEAR TABLE AND PROMPT FUNCTIONS==============================================================================================================
    #CLEAR SELECTION EVERY TIME SELECTION CHANGES
    def clear_all_selections(self):
      self.studentTable_widget.clearSelection()
      self.programTable_widget.clearSelection()
      self.collegeTable_widget.clearSelection()

      self.studentTable_widget.clearFocus()
      self.programTable_widget.clearFocus()
      self.collegeTable_widget.clearFocus()

      self.studentTable_widget.viewport().update()
      self.programTable_widget.viewport().update()
      self.collegeTable_widget.viewport().update()

    #IF SELECTED ROW IS DELETE
    def delete_student_button(self):
        if self.studentTable_widget.currentRow() >= 0:
            self.delete_student_confirmation()
        else:
            self.delete_error()
            
    def delete_program_button(self):
        if self.programTable_widget.currentRow() >= 0:
            self.delete_program_confirmation()
        else:
            self.delete_error()

    def delete_college_button(self):
        if self.collegeTable_widget.currentRow() >= 0:
            self.delete_college_confirmation()
        else:
            self.delete_error()

    def delete_error(self):
        message_box = QtWidgets.QMessageBox(self)
        message_box.setWindowTitle('Delete Error')
        message_box.setText('Please select a row to delete')
        message_box.setIcon(QtWidgets.QMessageBox.Warning)
        message_box.setStyleSheet("QLabel { color : white; } QPushButton { color: white; }")
        message_box.exec_()

    def add_succesful(self):
        message_box = QtWidgets.QMessageBox(self)
        message_box.setWindowTitle('Add Successful')
        message_box.setText('Input succesfully added')
        message_box.setIcon(QtWidgets.QMessageBox.Information)
        message_box.setStyleSheet("QLabel { color : white; } QPushButton { color: white; }")
        message_box.exec_()

    def add_error(self):
        message_box = QtWidgets.QMessageBox(self)
        message_box.setWindowTitle('Add Error')
        message_box.setText('Input not added')
        message_box.setIcon(QtWidgets.QMessageBox.Warning)
        message_box.setStyleSheet("QLabel { color : white; } QPushButton { color: white; }")
        message_box.exec_()

    def search_succesful(self):
        message_box = QtWidgets.QMessageBox(self)
        message_box.setWindowTitle('Search Successful')
        message_box.setText('An item is found')
        message_box.setIcon(QtWidgets.QMessageBox.Information)
        message_box.setStyleSheet("QLabel { color : white; } QPushButton { color: white; }")
        message_box.exec_()

    def search_error(self):
        message_box = QtWidgets.QMessageBox(self)
        message_box.setWindowTitle('Search Error')
        message_box.setText('No item is found')
        message_box.setIcon(QtWidgets.QMessageBox.Warning)
        message_box.setStyleSheet("QLabel { color : white; } QPushButton { color: white; }")
        message_box.exec_()

    def selection_error(self):
        message_box = QtWidgets.QMessageBox(self)
        message_box.setWindowTitle('Selection Error')
        message_box.setText('Please select a row to edit')
        message_box.setIcon(QtWidgets.QMessageBox.Warning)
        message_box.setStyleSheet("QLabel { color : white; } QPushButton { color: white; }")
        message_box.exec_()
    
    def update_succesful(self):
        message_box = QtWidgets.QMessageBox(self)
        message_box.setWindowTitle('Update Successful')
        message_box.setText('Input succesfully updated')
        message_box.setIcon(QtWidgets.QMessageBox.Information)
        message_box.setStyleSheet("QLabel { color : white; } QPushButton { color: white; }")
        message_box.exec_()

    def input_exists(self):
        message_box = QtWidgets.QMessageBox(self)
        message_box.setWindowTitle('Input Error')
        message_box.setText('Input already exists')
        message_box.setIcon(QtWidgets.QMessageBox.Warning)
        message_box.setStyleSheet("QLabel { color : white; } QPushButton { color: white; }")
        message_box.exec_()
    
    def refresh_student(self):
        for row in range(self.studentTable_widget.rowCount()):
            self.studentTable_widget.setRowHidden(row, False)
        self.load_student()
        self.clear_student_input()
        self.sortStudents_combo.setCurrentIndex(-1)
        self.searchStudents_combo.setCurrentIndex(-1)
    
    def refresh_program(self):
        for row in range(self.programTable_widget.rowCount()):
            self.programTable_widget.setRowHidden(row, False)
        self.load_program()
        self.clear_program_input()
        self.sortProgram_combo.setCurrentIndex(-1)
        self.searchProgram_combo.setCurrentIndex(-1)

    def refresh_college(self):
        for row in range(self.collegeTable_widget.rowCount()):
            self.collegeTable_widget.setRowHidden(row, False)
        self.load_college()
        self.clear_college_inputs()
        self.sortCollege_combo.setCurrentIndex(-1)
        self.searchCollege_combo.setCurrentIndex(-1)

#========================================================================================================================================================================================================================

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainApp()
    mainWindow.show()
    sys.exit(app.exec_())
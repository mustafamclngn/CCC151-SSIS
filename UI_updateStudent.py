# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'update_window_new.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_UpdateBox(object):
    def setupUi(self, UpdateBox):
        UpdateBox.setObjectName("UpdateBox")
        UpdateBox.resize(376, 299)
        UpdateBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        UpdateBox.setStyleSheet("background-color: rgba(31,31,47,255)")
        self.label = QtWidgets.QLabel(UpdateBox)
        self.label.setGeometry(QtCore.QRect(160, 10, 55, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label.setStyleSheet("color: white;")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(UpdateBox)
        self.label_2.setGeometry(QtCore.QRect(11, 51, 121, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: white;")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(UpdateBox)
        self.label_3.setGeometry(QtCore.QRect(11, 82, 111, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: white;")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(UpdateBox)
        self.label_4.setGeometry(QtCore.QRect(11, 113, 121, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: white;")
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(UpdateBox)
        self.label_5.setGeometry(QtCore.QRect(11, 144, 91, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color: white;")
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(UpdateBox)
        self.label_6.setGeometry(QtCore.QRect(11, 173, 121, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color: white;")
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(UpdateBox)
        self.label_7.setGeometry(QtCore.QRect(11, 202, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("color: white;")
        self.label_7.setObjectName("label_7")
        self.updateStudentID_box = QtWidgets.QLineEdit(UpdateBox)
        self.updateStudentID_box.setGeometry(QtCore.QRect(160, 50, 191, 24))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.updateStudentID_box.setFont(font)
        self.updateStudentID_box.setStyleSheet("border-radius: 10px;\n"
"background-color: rgba(44,44,45,255);\n"
"color:white;")
        self.updateStudentID_box.setText("")
        self.updateStudentID_box.setObjectName("updateStudentID_box")
        self.updateFirstNam_box = QtWidgets.QLineEdit(UpdateBox)
        self.updateFirstNam_box.setGeometry(QtCore.QRect(160, 80, 191, 24))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.updateFirstNam_box.setFont(font)
        self.updateFirstNam_box.setStyleSheet("border-radius: 10px;\n"
"background-color: rgba(44,44,45,255);\n"
"color:white;")
        self.updateFirstNam_box.setText("")
        self.updateFirstNam_box.setObjectName("updateFirstNam_box")
        self.updateLastName_box = QtWidgets.QLineEdit(UpdateBox)
        self.updateLastName_box.setGeometry(QtCore.QRect(160, 110, 191, 24))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.updateLastName_box.setFont(font)
        self.updateLastName_box.setStyleSheet("border-radius: 10px;\n"
"background-color: rgba(44,44,45,255);\n"
"color:white;")
        self.updateLastName_box.setObjectName("updateLastName_box")
        self.updateGender_combo = QtWidgets.QComboBox(UpdateBox)
        self.updateGender_combo.setGeometry(QtCore.QRect(160, 140, 101, 22))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.updateGender_combo.setFont(font)
        self.updateGender_combo.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.updateGender_combo.setStyleSheet("border-radius: 10px;\n"
"background-color: rgba(44,44,45,255);\n"
"color:white;")
        self.updateGender_combo.setObjectName("updateGender_combo")
        self.updateGender_combo.addItem("")
        self.updateGender_combo.addItem("")
        self.updateYearLevel_combo = QtWidgets.QComboBox(UpdateBox)
        self.updateYearLevel_combo.setGeometry(QtCore.QRect(160, 170, 41, 22))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.updateYearLevel_combo.setFont(font)
        self.updateYearLevel_combo.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.updateYearLevel_combo.setStyleSheet("border-radius: 10px;\n"
"background-color: rgba(44,44,45,255);\n"
"color:white;")
        self.updateYearLevel_combo.setObjectName("updateYearLevel_combo")
        self.updateYearLevel_combo.addItem("")
        self.updateYearLevel_combo.addItem("")
        self.updateYearLevel_combo.addItem("")
        self.updateYearLevel_combo.addItem("")
        self.update_button = QtWidgets.QPushButton(UpdateBox)
        self.update_button.setGeometry(QtCore.QRect(140, 250, 101, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.update_button.setFont(font)
        self.update_button.setStyleSheet("background-color: rgb(114,137,218);\n"
"color: white;\n"
"font-weight: bold;\n"
"border-radius: 13px;")
        self.update_button.setObjectName("update_button")
        self.updateGender_combo_2 = QtWidgets.QComboBox(UpdateBox)
        self.updateGender_combo_2.setGeometry(QtCore.QRect(160, 210, 101, 22))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.updateGender_combo_2.setFont(font)
        self.updateGender_combo_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.updateGender_combo_2.setStyleSheet("border-radius: 10px;\n"
"background-color: rgba(44,44,45,255);\n"
"color:white;")
        self.updateGender_combo_2.setObjectName("updateGender_combo_2")

        self.retranslateUi(UpdateBox)
        QtCore.QMetaObject.connectSlotsByName(UpdateBox)

    def retranslateUi(self, UpdateBox):
        _translate = QtCore.QCoreApplication.translate
        UpdateBox.setWindowTitle(_translate("UpdateBox", "Dialog"))
        self.label.setText(_translate("UpdateBox", "EDIT"))
        self.label_2.setText(_translate("UpdateBox", "Student ID:"))
        self.label_3.setText(_translate("UpdateBox", "First Name:"))
        self.label_4.setText(_translate("UpdateBox", "Last Name:"))
        self.label_5.setText(_translate("UpdateBox", "Gender:"))
        self.label_6.setText(_translate("UpdateBox", "Year Level:"))
        self.label_7.setText(_translate("UpdateBox", "Program Code:"))
        self.updateGender_combo.setItemText(0, _translate("UpdateBox", "Male"))
        self.updateGender_combo.setItemText(1, _translate("UpdateBox", "Female"))
        self.updateYearLevel_combo.setItemText(0, _translate("UpdateBox", "1"))
        self.updateYearLevel_combo.setItemText(1, _translate("UpdateBox", "2"))
        self.updateYearLevel_combo.setItemText(2, _translate("UpdateBox", "3"))
        self.updateYearLevel_combo.setItemText(3, _translate("UpdateBox", "4"))
        self.update_button.setText(_translate("UpdateBox", "Update"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    UpdateBox = QtWidgets.QDialog()
    ui = Ui_UpdateBox()
    ui.setupUi(UpdateBox)
    UpdateBox.show()
    sys.exit(app.exec_())

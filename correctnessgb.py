from PyQt5.QtWidgets import QGroupBox, QLabel, QLineEdit, QPushButton, QGridLayout, QMessageBox
from PyQt5.QtGui import QIntValidator

import os


class CorrectnessGroupBox(QGroupBox):
    def __init__(self, test_data_dir='', exe='', max_deduction=0):
        def getDir(entry, dir):
            dname = QFileDialog.getExistingDirectory(self)
            if not dname:
                return
            if not os.path.isdir(dname):
                return
            entry.setText(dname)
            dir = dname

        def getExe(entry, exe):
            ename, _ = QFileDialog.getOpenFileName(self)
            if not ename:
                return
            elif not os.access(ename, os.X_OK):
                err = QMessageBox(QMessageBox.Critical, 'Error', '%s is not an executable program' % ename, QMessageBox.Ok, self)
                err.show()
                return
            entry.setText(ename)
            exe = ename

        def onEditDeduction(entry, max_deduction):
            max_deduction = int(entry.text())

        def onEditDir(entry, member_dir):
            new_dir = entry.text()
            if not new_dir:
                return
            if not os.path.isdir(new_dir):
                err = QMessageBox(QMessageBox.Critical, 'Error', '%s is not a directory' % new_dir, QMessageBox.Ok, self)
                err.show()
                return
            member_dir = new_dir

        def onEditExe(new_exe, member_exe):
            new_exe = entry.text()
            if not new_exe:
                return
            elif not os.access(new_exe, os.X_OK):
                err = QMessageBox(QMessageBox.Critical, 'Error', '%s is not an executable program' % new_exe, QMessageBox.Ok, self)
                err.show()
                return
            member_exe = new_exe

        super().__init__()
        self.test_data_dir = test_data_dir
        self.exe = exe
        self.max_deduction = max_deduction

        test_data_label = QLabel('Test data directory')
        self.test_data_edit = QLineEdit() 
        self.test_data_edit.editingFinished.connect(lambda: onEditDir(self.test_data_edit, self.test_data_dir))
        test_data_btn = QPushButton('Browse', self) 
        test_data_btn.clicked.connect(lambda: getDir(self.test_data_edit, self.test_data_dir))

        exe_label = QLabel('Answer program')
        self.exe_edit = QLineEdit() 
        self.exe_edit.editingFinished.connect(lambda: onEditExe(self.exe_edit, self.exe))
        exe_btn = QPushButton('Browse', self) 
        exe_btn.clicked.connect(lambda: getExe(self.exe_edit, self.exe))

        point_label = QLabel('Maximum points deduction:')
        self.point_edit = QLineEdit()
        self.point_edit.setMaximumWidth(50)
        point_validator = QIntValidator()
        self.point_edit.setValidator(point_validator)
        self.point_edit.editingFinished.connect(lambda: onEditDeduction(self.point_edit, self.max_deduction))

        gb_grid = QGridLayout()

        gb_grid.addWidget(test_data_label, 0, 0, 1, 1)
        gb_grid.addWidget(self.test_data_edit, 0, 1, 1, 4)
        gb_grid.addWidget(test_data_btn, 0, 5, 1, 1)

        gb_grid.addWidget(exe_label, 1, 0, 1, 1)
        gb_grid.addWidget(self.exe_edit, 1, 1, 1, 4)
        gb_grid.addWidget(exe_btn, 1, 5, 1, 1)

        gb_grid.addWidget(point_label, 2, 0, 1, 1)
        gb_grid.addWidget(self.point_edit, 2, 1, 1, 1)

        self.setLayout(gb_grid)
        self.setTitle('Correctness')

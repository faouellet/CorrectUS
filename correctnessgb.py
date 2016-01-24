from PyQt5.QtWidgets import QGroupBox, QLabel, QLineEdit, QPushButton, QGridLayout, QMessageBox, QFileDialog
from PyQt5.QtGui import QIntValidator

import os


class CorrectnessGroupBox(QGroupBox):
    def __init__(self, test_data_dir='', exe='', max_deduction=0):
        def getDir(entry):
            dname = QFileDialog.getExistingDirectory(self)
            entry.setText(dname)

        def getExe(entry):
            ename, _ = QFileDialog.getOpenFileName(self)
            entry.setText(ename)

        def onEditDeduction(entry):
            try:
                self.max_deduction = int(entry.text())
            except ValueError:
                self.max_deduction = 0

        def onEditDir(entry):
            new_dir = entry.text()
            if not new_dir:
                return
            if not os.path.isdir(new_dir):
                err = QMessageBox(QMessageBox.Critical, 'Error', '%s is not a directory' % new_dir, QMessageBox.Ok, self)
                err.show()
                entry.setText('')
                return
            self.test_data_dir = new_dir

        def onEditExe(entry):
            new_exe = entry.text()
            if not new_exe:
                return
            elif not os.access(new_exe, os.X_OK):
                err = QMessageBox(QMessageBox.Critical, 'Error', '%s is not an executable program' % new_exe, QMessageBox.Ok, self)
                err.show()
                entry.setText('')
                return
            self.exe = new_exe

        super().__init__()
        self.test_data_dir = test_data_dir
        self.exe = exe
        self.max_deduction = max_deduction

        test_data_label = QLabel('Test data directory')
        self.test_data_edit = QLineEdit() 
        self.test_data_edit.textChanged.connect(lambda: onEditDir(self.test_data_edit))
        test_data_btn = QPushButton('Browse', self) 
        test_data_btn.clicked.connect(lambda: getDir(self.test_data_edit))

        exe_label = QLabel('Answer program')
        self.exe_edit = QLineEdit() 
        self.exe_edit.textChanged.connect(lambda: onEditExe(self.exe_edit))
        exe_btn = QPushButton('Browse', self) 
        exe_btn.clicked.connect(lambda: getExe(self.exe_edit))

        point_label = QLabel('Maximum points deduction:')
        self.point_edit = QLineEdit()
        self.point_edit.setMaximumWidth(50)
        point_validator = QIntValidator()
        self.point_edit.setValidator(point_validator)
        self.point_edit.textChanged.connect(lambda: onEditDeduction(self.point_edit))

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

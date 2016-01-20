from PyQt5.QtWidgets import QGroupBox, QLabel, QLineEdit, QPushButton, QGridLayout

import os


class CorrectnessGroupBox(QGroupBox):
    def __init__(self):
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

        super().__init__()
        self.test_data_dir = ""
        self.exe = ""

        test_data_label = QLabel('Test data directory')
        test_data_edit = QLineEdit() 
        test_data_btn = QPushButton('Browse', self) 
        test_data_btn.clicked.connect(lambda: getDir(test_data_edit, self.test_data_dir))

        exe_label = QLabel('Answer program')
        exe_edit = QLineEdit() 
        exe_btn = QPushButton('Browse', self) 
        exe_btn.clicked.connect(lambda: getExe(exe_edit, self.exe))

        point_label = QLabel('Maximum points deduction:')
        point_edit = QLineEdit()
        point_edit.setMaximumWidth(50)

        gb_grid = QGridLayout()

        gb_grid.addWidget(test_data_label, 0, 0, 1, 1)
        gb_grid.addWidget(test_data_edit, 0, 1, 1, 4)
        gb_grid.addWidget(test_data_btn, 0, 5, 1, 1)

        gb_grid.addWidget(exe_label, 1, 0, 1, 1)
        gb_grid.addWidget(exe_edit, 1, 1, 1, 4)
        gb_grid.addWidget(exe_btn, 1, 5, 1, 1)

        gb_grid.addWidget(point_label, 2, 0, 1, 1)
        gb_grid.addWidget(point_edit, 2, 1, 1, 1)

        self.setLayout(gb_grid)
        self.setTitle('Correctness')

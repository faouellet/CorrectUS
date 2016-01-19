from PyQt5.QtWidgets import *

import os


class GeneralInfoGroupBox(QGroupBox):
    def __init__(self):
        super().__init__()
        self.root_dir = ""
        self.res_dir = ""

        root_label = QLabel('Assignments directory')
        root_edit = QLineEdit() 
        root_btn = QPushButton('Browse', self) 
        root_btn.clicked.connect(lambda: self.getDir(root_edit, self.root_dir))

        res_label = QLabel('Results directory')
        res_edit = QLineEdit() 
        res_btn = QPushButton('Browse', self) 
        res_btn.clicked.connect(lambda: self.getDir(res_edit, self.res_dir))

        gb_grid = QGridLayout()

        gb_grid.addWidget(root_label, 0, 0, 1, 1)
        gb_grid.addWidget(root_edit, 0, 1, 1, 4)
        gb_grid.addWidget(root_btn, 0, 5, 1, 1)

        gb_grid.addWidget(res_label, 1, 0, 1, 1)
        gb_grid.addWidget(res_edit, 1, 1, 1, 4)
        gb_grid.addWidget(res_btn, 1, 5, 1, 1)

        self.setLayout(gb_grid)
        self.setTitle('General informations')


    def getDir(self, entry, dir):
            dname = QFileDialog.getExistingDirectory(self)
            if not dname:
                return
            if not os.isdir(dname):
                return
            entry.setText(dname)
            dir = dname
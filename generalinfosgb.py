from PyQt5.QtWidgets import QGroupBox, QLabel, QLineEdit, QPushButton, QGridLayout, QFileDialog

import os


class GeneralInfoGroupBox(QGroupBox):
    def __init__(self, root_dir='', res_dir=''):
        def checkDir(dname):
            if not dname:
                return False
            if not os.path.isdir(dname):
                err = QMessageBox(QMessageBox.Critical, 'Error', '%s is not a directory' % new_dir, QMessageBox.Ok, self)
                err.show()
                return False
            return True

        def getDir(entry):
            dname = QFileDialog.getExistingDirectory(self)
            entry.setText(dname)

        def onEditRootDir(entry):
            new_dir = entry.text()
            if checkDir(new_dir):
                self.root_dir = new_dir
            else:
                entry.setText('')

        def onEditResDir(entry):
            new_dir = entry.text()
            if checkDir(new_dir):
                self.res_dir = new_dir
            else:
                entry.setText('')
            
        super().__init__()
        self.root_dir = root_dir
        self.res_dir = res_dir

        root_label = QLabel('Assignments directory')
        self.root_edit = QLineEdit() 
        self.root_edit.textChanged.connect(lambda: onEditRootDir(self.root_edit))
        root_btn = QPushButton('Browse', self) 
        root_btn.clicked.connect(lambda: getDir(self.root_edit))

        res_label = QLabel('Results directory')
        self.res_edit = QLineEdit() 
        self.res_edit.textChanged.connect(lambda: onEditResDir(self.res_edit))
        res_btn = QPushButton('Browse', self) 
        res_btn.clicked.connect(lambda: getDir(self.res_edit))

        gb_grid = QGridLayout()

        gb_grid.addWidget(root_label, 0, 0, 1, 1)
        gb_grid.addWidget(self.root_edit, 0, 1, 1, 4)
        gb_grid.addWidget(root_btn, 0, 5, 1, 1)

        gb_grid.addWidget(res_label, 1, 0, 1, 1)
        gb_grid.addWidget(self.res_edit, 1, 1, 1, 4)
        gb_grid.addWidget(res_btn, 1, 5, 1, 1)

        self.setLayout(gb_grid)
        self.setTitle('General informations')

from PyQt5.QtWidgets import QGroupBox, QLabel, QLineEdit, QPushButton, QGridLayout

import os


class GeneralInfoGroupBox(QGroupBox):
    def __init__(self, root_dir='', res_dir=''):
        def getDir(entry, dir):
            dname = QFileDialog.getExistingDirectory(self)
            if not dname:
                return
            if not os.path.isdir(dname):
                return
            entry.setText(dname)
            dir = dname

        def onEditDir(entry, member_dir):
            new_dir = entry.text()
            if not new_dir:
                return
            if not os.path.isdir(new_dir):
                err = QMessageBox(QMessageBox.Critical, 'Error', '%s is not a directory' % new_dir, QMessageBox.Ok, self)
                err.show()
                return
            member_dir = new_dir
            
        super().__init__()
        self.root_dir = root_dir
        self.res_dir = res_dir

        root_label = QLabel('Assignments directory')
        self.root_edit = QLineEdit() 
        self.root_edit.editingFinished.connect(lambda: onEditDir(self.root_edit, self.root_dir))
        root_btn = QPushButton('Browse', self) 
        root_btn.clicked.connect(lambda: getDir(self.root_edit, self.root_dir))

        res_label = QLabel('Results directory')
        self.res_edit = QLineEdit() 
        self.res_edit.editingFinished.connect(lambda: onEditDir(self.res_edit, self.res_dir))
        res_btn = QPushButton('Browse', self) 
        res_btn.clicked.connect(lambda: getDir(self.res_edit, self.res_dir))

        gb_grid = QGridLayout()

        gb_grid.addWidget(root_label, 0, 0, 1, 1)
        gb_grid.addWidget(self.root_edit, 0, 1, 1, 4)
        gb_grid.addWidget(root_btn, 0, 5, 1, 1)

        gb_grid.addWidget(res_label, 1, 0, 1, 1)
        gb_grid.addWidget(self.res_edit, 1, 1, 1, 4)
        gb_grid.addWidget(res_btn, 1, 5, 1, 1)

        self.setLayout(gb_grid)
        self.setTitle('General informations')

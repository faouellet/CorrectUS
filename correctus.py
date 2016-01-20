from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys
import yaml

from codingstandards import *
from correctnessgb import *
from documentationgb import *
from errorgb import *
from generalinfosgb import *
from includegb import *

from gradingengine import *


class CorrectUSWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ge = GradingEngine()
        self.root_dir = ""
        self.res_dir = ""
        self.test_data_dir = ""
        self.exe = ""

        self.initUI()
        self.initMenus()
        self.centerWindow()
        self.show()


    def initUI(self):
        self.setGeometry(300,300,800,600)
        self.setWindowTitle('CorrectUS')

        hw_infos_gb = GeneralInfoGroupBox()
        correctness_gb = CorrectnessGroupBox()
        documentation_gb = DocumentationGroupBox()
        include_gb = IncludeGroupBox()
        standards_gb = CodingStandardsGroupBox()
        errors_gb = ErrorGroupBox()

        gbtn = QPushButton('Grade', self)
        gbtn.clicked.connect(lambda: self.grade(self.root_dir, self.res_dir))
        gbtn.resize(gbtn.sizeHint())

        qbtn = QPushButton('Quit', self)
        qbtn.clicked.connect(QCoreApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        self.grid = QGridLayout()
        self.main_widget.setLayout(self.grid)

        self.grid.addWidget(hw_infos_gb, 0, 0, 2, 6)
        self.grid.addWidget(correctness_gb, 2, 0, 2, 6)
        self.grid.addWidget(documentation_gb, 4, 0, 1, 3)
        self.grid.addWidget(include_gb, 4, 3, 1, 3)
        self.grid.addWidget(standards_gb, 5, 0, 2, 6)
        self.grid.addWidget(errors_gb, 7, 0, 2, 6)
        self.grid.addWidget(gbtn, 9, 4)
        self.grid.addWidget(qbtn, 9, 5)


    def initMenus(self):
        def showAboutMenu():
            done = QMessageBox(QMessageBox.Information, 'About','Automatic grading of C++ homeworks', QMessageBox.Ok, self)
            done.show()

        quit = QAction('&Exit', self)
        quit.setShortcut('Ctrl+Q')
        quit.setStatusTip('Exit application')
        quit.triggered.connect(QCoreApplication.instance().quit)
        
        load = QAction('&Load config', self)
        load.setStatusTip('Load configuration file')
        load.triggered.connect(self.loadConfig)

        save = QAction('&Save config', self)
        save.setStatusTip('Save configuration file')
        save.triggered.connect(self.saveConfig)

        about = QAction('&About', self)
        about.triggered.connect(lambda: showAboutMenu())

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(quit)
        fileMenu.addAction(load)
        fileMenu.addAction(save)

        helpMenu = menubar.addMenu('&Help')
        helpMenu.addAction(about)


    def centerWindow(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def loadConfig(self):
        config, _ = QFileDialog.getOpenFileName(self)
        if not config:
            return
        with open(config, 'r') as conf:
            data = yaml.safe_load(conf)
        errs = {}
        for d in data.values():
            errs[d['id']] = Error(d["id"], d["check"], d["is_enabled"], d["penalty"])

        self.errors = errs
        self.setErrors()


    def saveConfig(self):
        config, _ = QFileDialog.getSaveFileName(self)
        if not config:
            return
        with open(config, 'w+') as outfile:
            for err in self.errors.values():
                err_dict = { err.id: { 'id':err.id, 'check':err.check, 'is_enabled':err.is_enabled, 'penalty':err.penalty } }
                outfile.write(yaml.dump(err_dict, default_flow_style=False))


    def grade(self, hw_root_dir, res_dir):
        self.ge.grade_all(hw_root_dir, res_dir)
        done = QMessageBox(QMessageBox.Information, 'Done','Grading complete', QMessageBox.Ok, self)
        done.show()


def main():
    app = QApplication(sys.argv)
    CorrectUSWidget()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

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

        self.initUI()
        self.initMenus()
        self.centerWindow()
        self.show()


    def initUI(self):
        self.setGeometry(300,300,800,600)
        self.setWindowTitle('CorrectUS')

        self.hw_infos_gb = GeneralInfoGroupBox()
        self.correctness_gb = CorrectnessGroupBox()
        self.documentation_gb = DocumentationGroupBox()
        self.include_gb = IncludeGroupBox()
        self.standards_gb = CodingStandardsGroupBox()
        self.errors_gb = ErrorGroupBox()

        gbtn = QPushButton('Grade', self)
        gbtn.clicked.connect(lambda: self.grade(self.hw_infos_gb.root_dir, self.hw_infos_gb.res_dir, self.correctness_gb.exe, self.correctness_gb.test_data_dir))
        gbtn.resize(gbtn.sizeHint())

        qbtn = QPushButton('Quit', self)
        qbtn.clicked.connect(QCoreApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        self.grid = QGridLayout()
        self.main_widget.setLayout(self.grid)

        self.grid.addWidget(self.hw_infos_gb, 0, 0, 2, 6)
        self.grid.addWidget(self.correctness_gb, 2, 0, 2, 6)
        self.grid.addWidget(self.documentation_gb, 4, 0, 1, 3)
        self.grid.addWidget(self.include_gb, 4, 3, 1, 3)
        self.grid.addWidget(self.standards_gb, 5, 0, 2, 6)
        self.grid.addWidget(self.errors_gb, 7, 0, 2, 6)
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

        # General infos
        self.hw_infos_gb.res_dir = data['General']['res_dir']
        self.hw_infos_gb.root_dir = data['General']['root_dir']
        
        # Correctness
        self.correctness_gb.test_data_dir = data['Correctness']['data_dir']
        self.correctness_gb.exe = data['Correctness']['exe']
        self.correctness_gb.max_deduction = data['Correctness']['max_deduction']

        # Documentation 
        self.documentation_gb.setChecked(bool(data['Documentation']['enabled']))
        self.documentation_gb.deduction_per_elem = int(data['Documentation']['deduction'])
        self.documentation_gb.max_deduction = int(data['Documentation']['max_deduction'])

        # Include
        self.include_gb.setChecked(data['Include']['enabled'])
        self.include_gb.max_deduction = data['Include']['max_deduction']
        self.include_gb.deduction_per_elem= data['Include']['deduction']
        self.include_gb.check_superfluous= data['Include']['check_superfluous']
        self.include_gb.check_order = data['Include']['check_oder']

        # Coding standards
        self.standards_gb.setChecked(data['Standards']['enabled'])
        self.standards_gb.var_name = data['Standards']['var_name']
        self.standards_gb.const_name = data['Standards']['const_name']
        self.standards_gb.func_name = data['Standards']['func_name']
        self.standards_gb.cs_name = data['Standards']['cs_name']
        self.standards_gb.indent_style = data['Standards']['indent_style']
        self.standards_gb.max_deduction = data['Standards']['max_deduction']
        self.standards_gb.deduction_per_elem = data['Standards']['deduction']

        # Errors
        #errs = {}
        #for d in data.values():
        #    errs[d['id']] = Error(d["id"], d["check"], d["is_enabled"], d["penalty"])

        #self.errors = errs
        #self.setErrors()


    def saveConfig(self):
        config, _ = QFileDialog.getSaveFileName(self)
        if not config:
            return

        marking_scheme = {}

        # General infos
        marking_scheme['General'] = {
                                        'root_dir':self.hw_infos_gb.root_dir,
                                        'res_dir':self.hw_infos_gb.res_dir,
                                    }

        # Correctness
        marking_scheme['Correctness'] = { 
                                            'data_dir':self.correctness_gb.test_data_dir, 
                                            'exe':self.correctness_gb.exe, 
                                            'max_deduction':self.correctness_gb.max_deduction 
                                        }

        # Documentation
        marking_scheme['Documentation'] = { 
                                            'enabled':self.documentation_gb.isChecked(),
                                            'max_deduction':self.documentation_gb.max_deduction, 
                                            'deduction':self.documentation_gb.deduction_per_elem 
                                          }

        # Include
        marking_scheme['Include'] = { 
                                        'enabled':self.include_gb.isChecked(),
                                        'max_deduction':self.include_gb.max_deduction, 
                                        'deduction':self.include_gb.deduction_per_elem, 
                                        'check_superfluous':self.include_gb.check_superfluous, 
                                        'check_oder':self.include_gb.check_order
                                    }

        # Coding standards
        marking_scheme['Standards'] = { 
                                        'enabled':self.standards_gb.isChecked(), 
                                        'var_name':self.standards_gb.var_name, 
                                        'const_name':self.standards_gb.const_name, 
                                        'func_name':self.standards_gb.func_name, 
                                        'cs_name':self.standards_gb.cs_name, 
                                        'indent_style':self.standards_gb.indent_style, 
                                        'max_deduction':self.standards_gb.max_deduction, 
                                        'deduction':self.standards_gb.deduction_per_elem 
                                      }

        # Errors
        #for err in self.errors.values():
        #    err_dict = { err.id: { 'id':err.id, 'check':err.check, 'is_enabled':err.is_enabled, 'penalty':err.penalty } }

        with open(config, 'w+') as outfile:
            outfile.write(yaml.dump(marking_scheme, default_flow_style=False))


    def grade(self, hw_root_dir, res_dir, correct_exe, data_dir):
        #self.ge.set_marking_scheme()
        self.ge.grade_all(hw_root_dir, res_dir, correct_exe, data_dir)
        done = QMessageBox(QMessageBox.Information, 'Done','Grading complete', QMessageBox.Ok, self)
        done.show()


def main():
    app = QApplication(sys.argv)
    CorrectUSWidget()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys
import yaml

from generalinfosgb import *
from gradingengine import *
from errors import *


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
        self.initTable()
        self.centerWindow()
        self.show()

    def getDir(self, entry, dir):
            dname = QFileDialog.getExistingDirectory(self)
            if not dname:
                return
            entry.setText(dname)
            dir = dname

    def getExe(self, entry, exe):
        ename, _ = QFileDialog.getOpenFileName(self)
        if not ename:
            return
        elif not os.access(ename, os.X_OK):
            err = QMessageBox(QMessageBox.Critical, 'Error', '%s is not an executable program' % ename, QMessageBox.Ok, self)
            err.show()
            return
        entry.setText(ename)
        exe = ename

    

    def createCorrecnessGroupBox(self):
        test_data_label = QLabel('Test data directory')
        test_data_edit = QLineEdit() 
        test_data_btn = QPushButton('Browse', self) 
        test_data_btn.clicked.connect(lambda: self.getDir(test_data_edit, self.test_data_dir))

        exe_label = QLabel('Answer program')
        exe_edit = QLineEdit() 
        exe_btn = QPushButton('Browse', self) 
        exe_btn.clicked.connect(lambda: self.getExe(exe_edit, self.exe))

        point_label = QLabel('Points:')
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

        cgb = QGroupBox('Correctness')
        cgb.setLayout(gb_grid)
        #cgb.setStyleSheet("QGroupBox { border: 3px solid rgb(0, 0, 0); }")
        return cgb

    def initUI(self):
        self.setGeometry(300,300,800,600)
        self.setWindowTitle('CorrectUS')

        hw_infos_gb = GeneralInfoGroupBox()
        correctness_gb = self.createCorrecnessGroupBox()

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
        self.grid.addWidget(gbtn, 8, 4)
        self.grid.addWidget(qbtn, 8, 5)

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

    def initTable(self):
        self.errors = get_default_errors()
        self.table = QTableWidget()
        self.table.setRowCount(len(self.errors))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['ID','Description','Penalty','Enabled'])
        self.table.horizontalHeader().setSectionResizeMode(1)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        self.table.resizeColumnsToContents()
        self.table.setSortingEnabled(False)

        self.table.cellChanged.connect(self.tableCellChanged)

        self.setErrors()
        
        self.grid.addWidget(self.table, 4, 0, 4, 6)

    def tableCellChanged(self, rowIdx, colIdx):
        if colIdx == 2:
            err_id = self.table.item(rowIdx, 0).text()
            new_val = self.table.item(rowIdx, colIdx).text()
            old_val = self.errors[err_id].penalty
            if new_val.isdigit():
                self.errors[err_id].penalty = int(new_val)
            else:
                self.table.item(rowIdx, colIdx).setText(str(old_val))

    def chkboxClicked(self, err, state):
        err.is_enabled = state is Qt.Checked

    def setErrors(self):
        self.ge.set_marking_scheme(self.errors)

        for idx, err_key in enumerate(sorted(self.errors)):
            err = self.errors[err_key]
            id_item = QTableWidgetItem(err.id)
            id_item.setFlags(Qt.ItemIsEnabled)

            desc_item = QTableWidgetItem(err.check)
            desc_item.setFlags(Qt.ItemIsEnabled)

            penalty_item = QTableWidgetItem(str(err.penalty))
            penalty_item.setTextAlignment(Qt.AlignCenter)

            cell_widget = QWidget()
            chk_box = QCheckBox()
            if err.is_enabled:
                chk_box.setCheckState(Qt.Checked)
            else:
                chk_box.setCheckState(Qt.Unchecked)
            chk_box.stateChanged.connect(lambda state, err=err: self.chkboxClicked(err, state))
            layout = QHBoxLayout(cell_widget)
            layout.addWidget(chk_box)
            layout.setAlignment(Qt.AlignCenter)
            cell_widget.setLayout(layout)

            self.table.setItem(idx, 0, id_item)
            self.table.setItem(idx, 1, desc_item)
            self.table.setItem(idx, 2, penalty_item)
            self.table.setCellWidget(idx, 3, cell_widget)

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

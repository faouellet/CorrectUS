from PyQt5.QtWidgets import *
from PyQt5.QtCore import QCoreApplication

import sys
import yaml

from gradingengine import *
from errors import *

class CorrectUSWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initMenus()
        #self.initListbox()
        self.centerWindow()
        self.ge = GradingEngine()
        self.show()

    def initUI(self):
        root_label = QLabel('Assignments root directory')
        root_edit = QLineEdit() 
        rootbtn = QPushButton('Browse', self) 
        rootbtn.clicked.connect(lambda: self.getDir(root_edit))

        res_label = QLabel('Results directory')
        res_edit = QLineEdit() 
        resbtn = QPushButton('Browse', self) 
        resbtn.clicked.connect(lambda: self.getDir(res_edit))

        gbtn = QPushButton('Grade', self)
        gbtn.clicked.connect(lambda: self.grade(root_edit.text(), res_edit.text()))
        gbtn.resize(gbtn.sizeHint())

        qbtn = QPushButton('Quit', self)
        qbtn.clicked.connect(QCoreApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        grid = QGridLayout()
        self.main_widget.setLayout(grid)

        grid.addWidget(root_label, 0, 0, 1, 1)
        grid.addWidget(root_edit, 0, 1, 1, 2)
        grid.addWidget(rootbtn, 0, 3, 1, 1)

        grid.addWidget(res_label, 1, 0, 1, 1)
        grid.addWidget(res_edit, 1, 1, 1, 2)
        grid.addWidget(resbtn, 1, 3, 1, 1)

        grid.addWidget(gbtn, 6, 2)
        grid.addWidget(qbtn, 6, 3)

        self.setGeometry(300,300,800,600)
        self.setWindowTitle('CorrectUS')

    def initMenus(self):
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

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(quit)
        fileMenu.addAction(load)
        fileMenu.addAction(save)

        #fileMenu.add_command(label="Load config", underline=0, command=self.loadConfig)
        #fileMenu.add_command(label="Save config", underline=0, command=self.saveConfig)
        #fileMenu.add_command(label="Quit", underline=0, command=self.quit)
        #menubar.add_cascade(label="File", underline=0, menu=fileMenu)

        #menubar.add_cascade(label="About", underline=0)

#    def initListbox(self):
#        container = Frame(self)
#        container.grid(row=2, column=0, columnspan=5, rowspan=10, sticky=W+E+S+N, padx=5, pady=5)
#
#        mlb = ScrolledMultiListbox(self)
#        mlb.grid(row=2, column=0, columnspan=5, rowspan=10, sticky=W+E+S+N, padx=5, pady=5)
#        mlb.config(columns=('ID','Description','Penalty','Enabled'), scrollmode='both')
#
#        self.cols = ['ID','Description','Penalty','Enabled']
#        self.tree = Treeview(container, columns=self.cols, show='headings')
#        vsb = Scrollbar(container, orient=VERTICAL, command=self.tree.yview)
#        hsb = Scrollbar(container, orient=HORIZONTAL, command=self.tree.xview)
#        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
#        
#        self.tree.grid(row=0, column=0, sticky=W+E+N+S, in_=container)
#        vsb.grid(row=0, column=1, sticky=NS, in_=container)
#        hsb.grid(row=1, column=0, sticky=EW, in_=container)
#        container.grid_columnconfigure(0, weight=1)
#        container.grid_rowconfigure(0, weight=1)
#
#        for col in self.cols:
#            self.tree.heading(col, text=col.title())
#            # adjust the column's width to the header string
#            self.tree.column(col, width=tkFont.Font().measure(col.title()))
#
#        self.setErrors(get_default_errors())

    def centerWindow(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def getDir(self, entry):
        dname = QFileDialog.getExistingDirectory(self)
        if not dname:
            return
        entry.setText(dname)

#    def setErrors(self, errs):
#        self.tree.delete(*self.tree.get_children())
#        self.errors = errs
#        for _, err in self.errors.items():
#            vals = [err.id, err.check, err.penalty]#, str(err.is_enabled)]
#            self.tree.insert('', 'end', values=vals)
#            Checkbutton(self.tree, variable=err.is_enabled)
#            # adjust column's width if necessary to fit each value
#            for ix, val in enumerate(vals):
#                col_w = tkFont.Font().measure(val)
#                if self.tree.column(self.cols[ix],width=None)<col_w:
#                    self.tree.column(self.cols[ix], width=col_w)

    def loadConfig(self):
        config, _ = QFileDialog.getOpenFileName(self)
        if not config:
            return
        with open(config, 'r') as conf:
            data = yaml.safe_load(conf)
        errs = {}
        for d in data.values():
            errs[d['id']] = Error(d["id"], d["check"], d["is_enabled"], d["penalty"])

        self.setErrors(errs)
        self.ge.set_marking_scheme(errs)

    def saveConfig(self):
        config, _ = QFileDialog.getSaveFileName(self)
        if not config:
            return
        with open(config, 'w+') as outfile:
            for err in self.errors.values():
                err_dict = { err.id: { 'id':err.id, 'check':err.check, 'is_enabled':err.is_enabled, 'penalty':err.penalty } }
                outfile.write(yaml.dump(err_dict, default_flow_style=False))

    def grade(self, hw_root_dir, res_dir):
        #self.ge.grade_all(hw_root_dir)
        print (res_dir)

def main():
    app = QApplication(sys.argv)
    corr = CorrectUSWidget()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

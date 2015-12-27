from Tkinter import Tk, BOTH, W, E, N, S, NS, EW, END, Menu, VERTICAL, HORIZONTAL
from ttk import Frame, Button, Style, Label, Entry, Treeview, Scrollbar
from tkFileDialog import askdirectory, askopenfilename, asksaveasfilename
import tkFont
import yaml

from gradingengine import *
from errors import *

class CorrectUSFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()
        self.initMenus()
        self.initTreeview()
        self.centerWindow()
        self.ge = GradingEngine()

    def initUI(self):
        self.parent.title("CorrectUS")

        self.pack(fill=BOTH, expand=True)

        Style().theme_use("alt")

        self.columnconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        Label(self, text="Assignments root directory").grid(sticky=W, padx=5, pady=5)
        Label(self, text="Results directory").grid(sticky=W, padx=5, pady=5)

        hwEntry = Entry(self)
        hwEntry.grid(row=0, column=1, columnspan=2, sticky=W+E, padx=5, pady=5)

        resEntry =  Entry(self)
        resEntry.grid(row=1, column=1, columnspan=2, sticky=W+E, padx=5, pady=5)

        Button(self, text="Browse", command=lambda: self.getFile(hwEntry)).grid(row=0, column=3, padx=5, pady=5)
        Button(self, text="Browse", command=lambda: self.getFile(resEntry)).grid(row=1, column=3, padx=5, pady=5)
        Button(self, text="Quit", underline=0, command=self.quit).grid(row=12, column=4, padx=5, pady=5)
        Button(self, text="OK", underline=0).grid(row=12, column=3, padx=5, pady=5)

    def initMenus(self):
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Load config", underline=0, command=self.loadConfig)
        fileMenu.add_command(label="Save config", underline=0, command=self.saveConfig)
        fileMenu.add_command(label="Quit", underline=0, command=self.quit)
        menubar.add_cascade(label="File", underline=0, menu=fileMenu)

        menubar.add_cascade(label="About", underline=0)

    def initTreeview(self):
        container = Frame(self)
        container.grid(row=2, column=0, columnspan=5, rowspan=10, sticky=W+E+S+N, padx=5, pady=5)

        self.cols = ['ID','Description','Enabled', 'Penalty']
        self.tree = Treeview(container, columns=self.cols, show='headings')
        vsb = Scrollbar(container, orient=VERTICAL, command=self.tree.yview)
        hsb = Scrollbar(container, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.tree.grid(row=0, column=0, sticky=W+E+N+S, in_=container)
        vsb.grid(row=0, column=1, sticky=NS, in_=container)
        hsb.grid(row=1, column=0, sticky=EW, in_=container)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        for col in self.cols:
            self.tree.heading(col, text=col.title())
            # adjust the column's width to the header string
            self.tree.column(col, width=tkFont.Font().measure(col.title()))

        self.setErrors(get_default_errors())

    def centerWindow(self):
        w = 800
        h = 600
        x = (self.parent.winfo_screenwidth() - 800) / 2
        y = (self.parent.winfo_screenheight() - 600) / 2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def getFile(self, entry):
        dname = askdirectory()
        entry.delete(0, END)
        entry.insert(0, dname)

    def setErrors(self, errs):
        self.tree.delete(*self.tree.get_children())
        self.errors = errs
        for _, err in self.errors.items():
            vals = [err.id, err.check, str(err.is_enabled), err.penalty]
            self.tree.insert('', 'end', values=vals)
            # adjust column's width if necessary to fit each value
            for ix, val in enumerate(vals):
                col_w = tkFont.Font().measure(val)
                if self.tree.column(self.cols[ix],width=None)<col_w:
                    self.tree.column(self.cols[ix], width=col_w)

    def loadConfig(self):
        config = askopenfilename()
        with open(config, 'r') as conf:
            data = yaml.safe_load(conf)
        errs = {}
        for d in data.values():
            errs[d['id']] = Error(d["id"], d["check"], d["is_enabled"], d["penalty"])

        self.setErrors(errs)
        self.ge.set_marking_scheme(errs)

    def saveConfig(self):
        config = asksaveasfilename()
        with open(config, 'w+') as outfile:
            for err in self.errors.values():
                err_dict = { err.id: { 'id':err.id, 'check':err.check, 'is_enabled':err.is_enabled, 'penalty':err.penalty } }
                #err_dict = dict(Error=dict(id=err.id, check=err.check, is_enabled=err.is_enabled, penalty=err.penalty))
                outfile.write(yaml.dump(err_dict, default_flow_style=False))

def main():
    root = Tk()
    CorrectUSFrame(root)
    root.mainloop()

if __name__ == '__main__':
    main()

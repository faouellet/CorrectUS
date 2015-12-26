from Tkinter import Tk, BOTH, W, E, N, S, NS, EW, Menu, VERTICAL, HORIZONTAL
from ttk import Frame, Button, Style, Label, Entry, Treeview, Scrollbar
from tkFileDialog import askdirectory
import tkFont

class CorrectUSFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()
        self.initMenu()
        self.initTreeview()
        self.centerWindow()

    def initUI(self):
        self.parent.title("CorrectUS")

        self.pack(fill=BOTH, expand=True)

        self.style = Style()
        self.style.theme_use("alt")

        self.columnconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        Label(self, text="Assignments root directory").grid(sticky=W, padx=5, pady=5)
        
        hwEntry = Entry(self)
        hwEntry.grid(row=0, column=1, columnspan=2, sticky=W+E, padx=5, pady=5)

        hwButton = Button(self, text="Browse", command=self.getFile)
        hwButton.grid(row=0, column=3, padx=5, pady=5)

        Label(self, text="Results directory").grid(sticky=W, padx=5, pady=5)

        resEntry =  Entry(self)
        resEntry.grid(row=1, column=1, columnspan=2, sticky=W+E, padx=5, pady=5)

        resButton = Button(self, text="Browse", command=self.getFile)
        resButton.grid(row=1, column=3, padx=5, pady=5)

        quitButton = Button(self, text="Quit", underline=0, command=self.quit)
        quitButton.grid(row=12, column=4, padx=5, pady=5)

        okButton = Button(self, text="OK", underline=0)
        okButton.grid(row=12, column=3, padx=5, pady=5)

    def initMenu(self):
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Quit", underline=0, command=self.quit)
        menubar.add_cascade(label="File", underline=0, menu=fileMenu)

        menubar.add_cascade(label="About", underline=0)

    def initTreeview(self):
        container = Frame(self)
        container.grid(row=2, column=0, columnspan=5, rowspan=10, sticky=W+E+S+N, padx=5, pady=5)

        cols = ['ID','Description','Enabled']
        self.tree = Treeview(container, columns=cols, show='headings')
        vsb = Scrollbar(container, orient=VERTICAL, command=self.tree.yview)
        hsb = Scrollbar(container, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.tree.grid(row=0, column=0, sticky=W+E+N+S, in_=container)
        vsb.grid(row=0, column=1, sticky=NS, in_=container)
        hsb.grid(row=1, column=0, sticky=EW, in_=container)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        for col in cols:
            self.tree.heading(col, text=col.title())
            # adjust the column's width to the header string
            self.tree.column(col,
            width=tkFont.Font().measure(col.title()))

        data = [
            ("Argentina",      "Buenos Aires",     "ARS"),
            ("Australia",      "Canberra",         "AUD"),
            ("Brazil",         "Brazilia",         "BRL"),
            ("Canada",         "Ottawa",           "CAD"),
            ("China",          "Beijing",          "CNY"),
            ("France",         "Paris",            "EUR"),
            ("Germany",        "Berlin",           "EUR"),
            ("India",          "New Delhi",        "INR"),
            ("Italy",          "Rome",             "EUR"),
            ("Japan",          "Tokyo",            "JPY"),
            ("Mexico",         "Mexico City",      "MXN"),
            ("Russia",         "Moscow",           "RUB"),
            ("South Africa",   "Pretoria",         "ZAR"),
            ("United Kingdom", "London",           "GBP"),
            ("United States",  "Washington, D.C.", "USD") ]

        for item in data:
            self.tree.insert('', 'end', values=item)
            # adjust column's width if necessary to fit each value
            for ix, val in enumerate(item):
                col_w = tkFont.Font().measure(val)
                if self.tree.column(cols[ix],width=None)<col_w:
                    self.tree.column(cols[ix], width=col_w)


    def centerWindow(self):
        w = 800
        h = 600
        x = (self.parent.winfo_screenwidth() - w) / 2
        y = (self.parent.winfo_screenheight() - h) / 2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def getFile(self):
        dname = askdirectory()
        return dname

def main():
    root = Tk()
    CorrectUSFrame(root)
    root.mainloop()

if __name__ == '__main__':
    main()

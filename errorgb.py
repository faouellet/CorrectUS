from PyQt5.QtWidgets import *

from errors import *


class ErrorGroupBox(QGroupBox):
    def __init__(self):            
        super().__init__()

        self.errors = get_default_errors()
        table = QTableWidget()
        table.setRowCount(len(self.errors))
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(['ID','Description','Penalty','Enabled'])
        table.horizontalHeader().setSectionResizeMode(1)
        table.setShowGrid(False)
        table.verticalHeader().setVisible(False)
        table.resizeColumnsToContents()
        table.setSortingEnabled(False)

        max_point_label = QLabel('Maximum points deduction:')
        max_point_edit = QLineEdit()
        max_point_edit.setMaximumWidth(50)

        gb_grid = QGridLayout()

        gb_grid.addWidget(max_point_label, 1, 0, 1, 1)
        gb_grid.addWidget(max_point_edit, 1, 1, 1, 1)

        self.setLayout(gb_grid)
        self.setTitle('Errors')
        self.setCheckable(True)
        self.setChecked(False)


    #def tableCellChanged(self, rowIdx, colIdx):
    #    if colIdx == 2:
    #        err_id = self.table.item(rowIdx, 0).text()
    #        new_val = self.table.item(rowIdx, colIdx).text()
    #        old_val = self.errors[err_id].penalty
    #        if new_val.isdigit():
    #            self.errors[err_id].penalty = int(new_val)
    #        else:
    #            self.table.item(rowIdx, colIdx).setText(str(old_val))
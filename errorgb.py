from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QGroupBox, QGridLayout, QWidget, QCheckBox, QHBoxLayout, QLabel, QLineEdit
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt

from errors import *


class ErrorGroupBox(QGroupBox):
    def __init__(self, max_deduction=0):            
        def tableCellChanged(rowIdx, colIdx):
            if colIdx == 2:
                err_id = self.table.item(rowIdx, 0).text()
                new_val = self.table.item(rowIdx, colIdx).text()
                old_val = self.errors[err_id].penalty
                if new_val.isdigit():
                    self.errors[err_id].penalty = int(new_val)
                else:
                    self.table.item(rowIdx, colIdx).setText(str(old_val))

        def onMaxEditPoint(line_edit):
            self.max_deduction = int(line_edit.text())

        super().__init__()
        self.max_deduction = max_deduction

        self.table = QTableWidget()
        self.table.setRowCount(len(get_default_errors()))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['ID','Description','Penalty','Enabled'])
        self.table.horizontalHeader().setSectionResizeMode(1)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        self.table.resizeColumnsToContents()
        self.table.setSortingEnabled(False)
        
        self.table.cellChanged.connect(tableCellChanged)

        self.setErrors(get_default_errors())

        max_point_label = QLabel('Maximum points deduction:')

        point_validator = QIntValidator()

        self.max_point_edit = QLineEdit()
        self.max_point_edit.setMaximumWidth(50)
        self.max_point_edit.setText('0')
        self.max_point_edit.setValidator(point_validator)
        self.max_point_edit.editingFinished.connect(lambda: onEditMax(self.max_point_edit))

        gb_grid = QGridLayout()

        gb_grid.addWidget(self.table, 0, 0, 4, 6)
        gb_grid.addWidget(max_point_label, 5, 4, 1, 1)
        gb_grid.addWidget(self.max_point_edit, 5, 5, 1, 1)

        self.setLayout(gb_grid)
        self.setTitle('Errors')
        self.setCheckable(True)
        self.setChecked(False)


    def chkboxClicked(self, err, state):
        self.errors[err.id].is_enabled = state is Qt.Checked


    def setErrors(self, errors):
        self.errors = errors

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

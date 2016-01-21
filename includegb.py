from PyQt5.QtWidgets import QGroupBox, QLabel, QLineEdit, QGridLayout, QCheckBox, QMessageBox
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt


class IncludeGroupBox(QGroupBox):
    def __init__(self):         
        def onMaxEditPoint(max_deduction, line_edit):
            max_deduction = int(line_edit.text())

        def onEditPoint(deduction, line_edit, max_deduction):
            point_deduction = int(line_edit.text())
            if point_deduction > max_deduction:
                error = QMessageBox(QMessageBox.Critical, 'Error',"The point deduction per error missing can't be greater than the maximum point deduction", QMessageBox.Ok, self)
                error.show()
            else:
                deduction = point_deduction

        def onChecked(state, check):
            check = False if state == Qt.Unchecked else True
            
        super().__init__()
        self.max_deduction = 0;
        self.deduction_per_elem = 0
        self.check_superfluous = False
        self.check_order = False

        point_validator = QIntValidator()
        
        point_label = QLabel('Points deduction per error:')
        point_edit = QLineEdit()
        point_edit.setMaximumWidth(50)
        point_edit.setText('0')
        point_edit.setValidator(point_validator)
        point_edit.editingFinished.connect(lambda: onEditPoint(self.deduction_per_elem, point_edit, self.max_deduction))

        max_point_label = QLabel('Maximum points deduction:')
        max_point_edit = QLineEdit()
        max_point_edit.setMaximumWidth(50)
        max_point_edit.setText('0')
        max_point_edit.setValidator(point_validator)
        max_point_edit.editingFinished.connect(lambda: onMaxEditPoint(self.max_deduction, max_point_edit))

        min_include_label = QLabel('Check for superfluous includes')
        min_include_chkbox = QCheckBox()
        min_include_chkbox.stateChanged.connect(lambda state: onChecked(state, self.check_superfluous))

        order_include_label = QLabel('Check includes order')
        order_include_chkbox = QCheckBox()
        order_include_chkbox.stateChanged.connect(lambda state: onChecked(state, self.check_order))

        gb_grid = QGridLayout()

        gb_grid.addWidget(min_include_label, 0, 0, 1, 1)
        gb_grid.addWidget(min_include_chkbox, 0, 1, 1, 1)
        gb_grid.addWidget(order_include_label, 1, 0, 1, 1)
        gb_grid.addWidget(order_include_chkbox, 1, 1, 1, 1)

        gb_grid.addWidget(point_label, 2, 0, 1, 1)
        gb_grid.addWidget(point_edit, 2, 1, 1, 1)
        gb_grid.addWidget(max_point_label, 3, 0, 1, 1)
        gb_grid.addWidget(max_point_edit, 3, 1, 1, 1)

        self.setLayout(gb_grid)
        self.setTitle('Includes')
        self.setCheckable(True)
        self.setChecked(False)

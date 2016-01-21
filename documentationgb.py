from PyQt5.QtWidgets import QGroupBox, QLabel, QLineEdit, QGridLayout, QMessageBox
from PyQt5.QtGui import QIntValidator


class DocumentationGroupBox(QGroupBox):
    def __init__(self):            
        def onMaxEditPoint(max_deduction, line_edit):
            max_deduction = int(line_edit.text())

        def onEditPoint(deduction, line_edit, max_deduction):
            point_deduction = int(line_edit.text())
            if point_deduction > max_deduction:
                error = QMessageBox(QMessageBox.Critical, 'Error',"The point deduction per element missing can't be greater than the maximum point deduction", QMessageBox.Ok, self)
                error.show()
            else:
                deduction = point_deduction

        super().__init__()
        self.max_deduction = 0;
        self.deduction_per_elem = 0

        point_validator = QIntValidator()
        
        point_label = QLabel('Points deduction per element missing:')
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

        gb_grid = QGridLayout()

        gb_grid.addWidget(point_label, 0, 0, 1, 1)
        gb_grid.addWidget(point_edit, 0, 1, 1, 1)
        gb_grid.addWidget(max_point_label, 1, 0, 1, 1)
        gb_grid.addWidget(max_point_edit, 1, 1, 1, 1)

        self.setLayout(gb_grid)
        self.setTitle('Documentation')
        self.setCheckable(True)
        self.setChecked(False)

from PyQt5.QtWidgets import QGroupBox, QLabel, QLineEdit, QGridLayout, QMessageBox
from PyQt5.QtGui import QIntValidator


class DocumentationGroupBox(QGroupBox):
    def __init__(self, enabled=False, max_deduction=0, deduction=0):            
        def onMaxEditPoint(new_max):
            self.max_deduction = int(new_max)

        def onEditPoint(new_deduction):
            if int(new_deduction) > self.max_deduction:
                error = QMessageBox(QMessageBox.Critical, 'Error',"The point deduction per element missing can't be greater than the maximum point deduction", QMessageBox.Ok, self)
                error.show()
            else:
                self.deduction_per_elem = int(new_deduction)

        super().__init__()
        self.max_deduction = max_deduction;
        self.deduction_per_elem = deduction

        point_validator = QIntValidator()
        
        point_label = QLabel('Points deduction per element missing:')
        self.point_edit = QLineEdit()
        self.point_edit.setMaximumWidth(50)
        self.point_edit.setText('0')
        self.point_edit.setValidator(point_validator)
        self.point_edit.textChanged.connect(lambda new_deduction: onEditPoint(new_deduction))

        max_point_label = QLabel('Maximum points deduction:')
        self.max_point_edit = QLineEdit()
        self.max_point_edit.setMaximumWidth(50)
        self.max_point_edit.setText('0')
        self.max_point_edit.setValidator(point_validator)
        self.max_point_edit.textChanged.connect(lambda new_max: onMaxEditPoint(new_max))

        gb_grid = QGridLayout()

        gb_grid.addWidget(point_label, 0, 0, 1, 1)
        gb_grid.addWidget(self.point_edit, 0, 1, 1, 1)
        gb_grid.addWidget(max_point_label, 1, 0, 1, 1)
        gb_grid.addWidget(self.max_point_edit, 1, 1, 1, 1)

        self.setLayout(gb_grid)
        self.setTitle('Documentation')
        self.setCheckable(True)
        self.setChecked(enabled)

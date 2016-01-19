from PyQt5.QtWidgets import *


class DocumentationoGroupBox(QGroupBox):
    def __init__(self):            
        super().__init__()

        point_label = QLabel('Points deduction per element missing:')
        point_edit = QLineEdit()
        point_edit.setMaximumWidth(50)

        max_point_label = QLabel('Maximum points deduction:')
        max_point_edit = QLineEdit()
        max_point_edit.setMaximumWidth(50)

        gb_grid = QGridLayout()

        gb_grid.addWidget(point_label, 0, 0, 1, 1)
        gb_grid.addWidget(point_edit, 0, 1, 1, 1)
        gb_grid.addWidget(max_point_label, 1, 0, 1, 1)
        gb_grid.addWidget(max_point_edit, 1, 1, 1, 1)

        self.setLayout(gb_grid)
        self.setTitle('Documentation')
        self.setCheckable(True)
        self.setChecked(False)

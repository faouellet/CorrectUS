from PyQt5.QtWidgets import *


class IncludeGroupBox(QGroupBox):
    def __init__(self):            
        super().__init__()

        point_label = QLabel('Points deduction per error:')
        point_edit = QLineEdit()
        point_edit.setMaximumWidth(50)

        max_point_label = QLabel('Maximum points deduction:')
        max_point_edit = QLineEdit()
        max_point_edit.setMaximumWidth(50)

        min_include_label = QLabel('Check for superfluous includes')
        min_include_chkbox = QCheckBox()

        order_include_label = QLabel('Check includes order')
        order_include_chkbox = QCheckBox()

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

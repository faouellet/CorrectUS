from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class CodingStandardsGroupBox(QGroupBox):
    def __init__(self):            
        super().__init__()

        point_label = QLabel('Points deduction per error:')
        point_edit = QLineEdit()
        point_edit.setMaximumWidth(50)

        max_point_label = QLabel('Maximum points deduction:')
        max_point_edit = QLineEdit()
        max_point_edit.setMaximumWidth(50)

        naming_styles = ['CamelCase', 'camelCase', 'SNAKE_CASE']

        var_label = QLabel('Variable name')
        var_choices = QComboBox()
        var_choices.addItems(naming_styles)

        func_label = QLabel('Function name')
        func_choices = QComboBox()
        func_choices.addItems(naming_styles)

        const_label = QLabel('Constant name')
        const_choices = QComboBox()
        const_choices.addItems(naming_styles)

        cs_label = QLabel('Class/Struct name')
        cs_choices = QComboBox()
        cs_choices.addItems(naming_styles)        

        indent_label = QLabel('Indentation style')
        indent_choices = QComboBox()
        indent_choices.addItems(['Allman', 'Egyptian'])

        gb_grid = QGridLayout()
        gb_grid.setAlignment(Qt.AlignCenter)

        gb_grid.addWidget(var_label, 0, 0)
        gb_grid.addWidget(var_choices, 0, 1)

        gb_grid.addWidget(func_label, 0, 2)
        gb_grid.addWidget(func_choices, 0, 3)

        gb_grid.addWidget(const_label, 1, 0)
        gb_grid.addWidget(const_choices, 1, 1)

        gb_grid.addWidget(cs_label, 1, 2)
        gb_grid.addWidget(cs_choices, 1, 3)

        gb_grid.addWidget(indent_label, 0, 4)
        gb_grid.addWidget(indent_choices, 0, 5)

        gb_grid.addWidget(point_label, 2, 0)
        gb_grid.addWidget(point_edit, 2, 1)
        gb_grid.addWidget(max_point_label, 2, 3)
        gb_grid.addWidget(max_point_edit, 2, 4)

        self.setLayout(gb_grid)
        self.setTitle('Coding standard')
        self.setCheckable(True)
        self.setChecked(False)
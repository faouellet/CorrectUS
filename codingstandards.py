from PyQt5.QtWidgets import QGroupBox, QLabel, QLineEdit, QGridLayout, QComboBox, QMessageBox
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt


class CodingStandardsGroupBox(QGroupBox):
    def __init__(self, enabled=False, var_name='', const_name='', func_name='', cs_name='', indent_style='', max_deduction=0, deduction=0):   
        def onMaxEditPoint(max_deduction, line_edit):
            max_deduction = int(line_edit.text())

        def onEditPoint(deduction, line_edit, max_deduction):
            point_deduction = int(line_edit.text())
            if point_deduction > max_deduction:
                error = QMessageBox(QMessageBox.Critical, 'Error',"The point deduction per error missing can't be greater than the maximum point deduction", QMessageBox.Ok, self)
                error.show()
            else:
                deduction = point_deduction

        def onTextChanged(new_text, member):
            member = new_text

        def createLabelAndComboBox(label_text, combo_choices, member):
            label = QLabel(label_text)
            choices = QComboBox()
            choices.addItems(combo_choices)
            choices.currentIndexChanged.connect(lambda idx: onTextChanged(combo_choices[idx], member))
            return label, choices

        super().__init__()
        self.var_name = var_name
        self.const_name = const_name
        self.func_name = func_name
        self.cs_name = cs_name
        self.indent_style = indent_style
        self.max_deduction = max_deduction
        self.deduction_per_elem = deduction

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

        naming_styles = ['CamelCase', 'camelCase', 'SNAKE_CASE']

        var_label, var_choices = createLabelAndComboBox('Variable name', naming_styles, self.var_name)
        func_label, func_choices = createLabelAndComboBox('Function name', naming_styles, self.func_name)
        cs_label, cs_choices = createLabelAndComboBox('Class/Struct name', naming_styles, self.cs_name)
        const_label, const_choices = createLabelAndComboBox('Constant name', naming_styles, self.const_name)
        indent_label, indent_choices = createLabelAndComboBox('Indentation style', ['Allman', 'Egyptian'], self.indent_style)

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
        self.setChecked(enabled)

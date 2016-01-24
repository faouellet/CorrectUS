from PyQt5.QtWidgets import QGroupBox, QLabel, QLineEdit, QGridLayout, QComboBox, QMessageBox
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt


class CodingStandardsGroupBox(QGroupBox):
    def __init__(self, enabled=False, var_name='', const_name='', func_name='', cs_name='', indent_style='', max_deduction=0, deduction=0):   
        def onMaxEditPoint(line_edit):
            self.max_deduction = int(line_edit.text())

        def onEditPoint(line_edit, max_deduction):
            point_deduction = int(line_edit.text())
            if point_deduction > max_deduction:
                error = QMessageBox(QMessageBox.Critical, 'Error',"The point deduction per error missing can't be greater than the maximum point deduction", QMessageBox.Ok, self)
                error.show()
            else:
                self.deduction_per_elem = point_deduction

        def createLabelAndComboBox(label_text, combo_choices, member):
            label = QLabel(label_text)
            choices = QComboBox()
            choices.addItems(combo_choices)
            return label, choices

        def onVarIndexChanged(new_var_style):
            self.var_name = new_var_style

        def onFuncIndexChanged(new_func_style):
            self.func_name = new_func_style

        def onCSIndexChanged(new_cs_style):
            self.cs_name = new_cs_style

        def onConstIndexChanged(new_const_style):
            self.const_name = new_const_style

        def onIndentIndexChanged(new_indent_style):
            self.indent_style = new_indent_style

        super().__init__()
        self.naming_styles = ['CamelCase', 'camelCase', 'SNAKE_CASE']
        self.indent_conventions = ['Allman', 'Egyptian']

        self.var_name = var_name if var_name else self.naming_styles[0]
        self.const_name = const_name if const_name else self.naming_styles[0]
        self.func_name = func_name if func_name else self.naming_styles[0]
        self.cs_name = cs_name if cs_name else self.naming_styles[0]
        self.indent_style = indent_style if indent_style else self.indent_conventions[0]
        self.max_deduction = max_deduction
        self.deduction_per_elem = deduction

        point_validator = QIntValidator()

        point_label = QLabel('Points deduction per error:')
        self.point_edit = QLineEdit()
        self.point_edit.setMaximumWidth(50)
        self.point_edit.setText('0')
        self.point_edit.setValidator(point_validator)
        self.point_edit.editingFinished.connect(lambda: onEditPoint(self.point_edit, self.max_deduction))

        max_point_label = QLabel('Maximum points deduction:')
        self.max_point_edit = QLineEdit()
        self.max_point_edit.setMaximumWidth(50)
        self.max_point_edit.setText('0')
        self.max_point_edit.setValidator(point_validator)
        self.max_point_edit.editingFinished.connect(lambda: onMaxEditPoint(self.max_point_edit))

        var_label, self.var_choices = createLabelAndComboBox('Variable name', self.naming_styles, self.var_name)
        self.var_choices.currentIndexChanged.connect(lambda idx: onVarIndexChanged(self.naming_styles[idx]))
        
        func_label, self.func_choices = createLabelAndComboBox('Function name', self.naming_styles, self.func_name)
        self.func_choices.currentIndexChanged.connect(lambda idx: onFuncIndexChanged(self.naming_styles[idx]))
        
        cs_label, self.cs_choices = createLabelAndComboBox('Class/Struct name', self.naming_styles, self.cs_name)
        self.cs_choices.currentIndexChanged.connect(lambda idx: onCSIndexChanged(self.naming_styles[idx]))
        
        const_label, self.const_choices = createLabelAndComboBox('Constant name', self.naming_styles, self.const_name)
        self.const_choices.currentIndexChanged.connect(lambda idx: onConstIndexChanged(self.naming_styles[idx]))
        
        indent_label, self.indent_choices = createLabelAndComboBox('Indentation style', self.indent_conventions, self.indent_style)
        self.indent_choices.currentIndexChanged.connect(lambda idx: onIndentIndexChanged(self.indent_conventions[idx]))

        gb_grid = QGridLayout()
        gb_grid.setAlignment(Qt.AlignCenter)

        gb_grid.addWidget(var_label, 0, 0)
        gb_grid.addWidget(self.var_choices, 0, 1)

        gb_grid.addWidget(func_label, 0, 2)
        gb_grid.addWidget(self.func_choices, 0, 3)

        gb_grid.addWidget(const_label, 1, 0)
        gb_grid.addWidget(self.const_choices, 1, 1)

        gb_grid.addWidget(cs_label, 1, 2)
        gb_grid.addWidget(self.cs_choices, 1, 3)

        gb_grid.addWidget(indent_label, 0, 4)
        gb_grid.addWidget(self.indent_choices, 0, 5)

        gb_grid.addWidget(point_label, 2, 0)
        gb_grid.addWidget(self.point_edit, 2, 1)
        gb_grid.addWidget(max_point_label, 2, 3)
        gb_grid.addWidget(self.max_point_edit, 2, 4)

        self.setLayout(gb_grid)
        self.setTitle('Coding standard')
        self.setCheckable(True)
        self.setChecked(enabled)

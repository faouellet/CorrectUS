class Error:
    def __init__(self, id, check, is_enabled, penalty):
        self.id = id
        self.check = check
        self.is_enabled = is_enabled
        self.penalty = penalty

def get_description(err_id):
    if not hasattr(get_description, "id_to_desc"):
        get_description.id_to_desc = {
                'IfAssign' : 'Using the result of an assignment as a condition without parentheses',
                'SwitchBool' : 'Switch condition has boolean value'
                }

    return get_description.id_to_desc[err_id]

def get_default_errors():
    if not hasattr(get_default_errors, "errors"):
        id_to_clang_check = { 
                'IfAssign' : 'clang-diagnostic-parentheses', 
                'SwitchBool' : 'clang-diagnostic-switch-bool'
                }

        get_default_errors.errors = {
                'IfAssign' : Error('IfAssign', get_description('IfAssign'), True, 2),
                'SwitchBool' : Error('SwitchBool', get_description('SwitchBool'), True, 2)
                }

    return get_default_errors.errors

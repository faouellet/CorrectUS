class Error:
    def __init__(self, id, check, desc, is_enabled, penalty):
        self.id = id
        self.check = check
        self.desc = desc
        self.is_enabled = is_enabled
        self.penalty = penalty

def get_default_errors():
    if not hasattr(get_default_errors, "errors"):
        type_to_clang_check = { 
                'IfAssign' : 'clang-diagnostic-parentheses', 
                'SwitchBool' : 'clang-diagnostic-switch-bool'
                }

        get_default_errors.errors = {
                'IfAssign' : Error('IfAssign', type_to_clang_check['IfAssign'],'', True, 2),
                'SwitchBool' : Error('SwitchBool', type_to_clang_check['SwitchBool'], '', True, 2)
                }

    return get_default_errors.errors

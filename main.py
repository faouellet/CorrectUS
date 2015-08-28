from clang.cindex import *
import re
import yaml as Y

Config.set_library_file("/usr/lib/llvm-3.6/lib/libclang.so.1")

index = Index.create()
translation_unit = index.parse("inputs/test.cpp");
cursor = translation_unit.cursor

naming_matchers = {}
naming_matchers["CamelCase"] = re.compile("[a-z]+([A-Z][a-z])*")
naming_matchers["PascalCase"] = re.compile("([A-Z][a-z])+")
naming_matchers["SnakeCase"] = re.compile("[A-Z][a-z]+_[A-Z][a-z]+(_[A-Z][a-z]+)+")

with open("usherb.style") as style_file:
    rules = Y.safe_load(style_file)

rulesdb = {}

for (x, y) in rules.items():
    try:
        rulesdb[x] = int(y, 10)
    except:
        rulesdb[x] = y

for node in cursor.walk_preorder():
    print node.spelling

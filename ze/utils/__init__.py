import sys
import importlib
import difflib
from pprint import pprint

def import_class(class_full_path):
    module_name, class_name = class_full_path.rsplit('.', 1)
    module = importlib.import_module(module_name)
    return getattr(module, class_name)

def diff_str(str1='', str2=''):
    splitlines = lambda s: s.splitlines(keepends=True)
    return list(difflib.Differ().compare(splitlines(str1), splitlines(str2)))

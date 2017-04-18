import importlib

def import_class(class_full_path):
    module_name, class_name = class_full_path.rsplit('.', 1)
    module = importlib.import_module(module_name)
    return getattr(module, class_name)
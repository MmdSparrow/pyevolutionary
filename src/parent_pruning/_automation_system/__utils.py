import os
import importlib.util


def get_non_private_functions_in_module(module, add_prefix=''):
    functions_list = []
    for name in dir(module):
        if not (name.startswith("__") or name.endswith("__")):
            obj = getattr(module, name)
            if callable(obj) and hasattr(obj, "__module__") and obj.__module__ == module.__name__:
                functions_list.append(add_prefix + name)
    return functions_list


def get_non_private_functions_from_module_path(module_path, add_prefix=''):
    if not os.path.isfile(module_path):
        raise FileNotFoundError(f"No such file: {module_path}")

    if not module_path.endswith(".py"):
        raise ValueError("Expected a .py file")

    module_name = os.path.splitext(os.path.basename(module_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, module_path)

    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module from path: {module_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return get_non_private_functions_in_module(module, add_prefix)

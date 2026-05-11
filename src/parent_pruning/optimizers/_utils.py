import os
import importlib.util

from parent_pruning._utils.exception_handeling.custom_exceptions.function_not_supported_exception import FunctionNotSupportedException


def __get_module_by_name(module_path):
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

def init_function_by_name(module, extension_module_path, func_name, function_objective, logger=None):
    func=None
    try:
        extension_module= __get_module_by_name(extension_module_path)
        func = getattr(extension_module, func_name, None)
        if not func:
            raise Exception('')
    except Exception:
        # read from default module
        func = getattr(module, func_name, None)
        if not func:
            raise FunctionNotSupportedException(func_name, function_objective, logger)
    return func

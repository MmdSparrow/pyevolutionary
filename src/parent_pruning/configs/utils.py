def get_list_of_the_not_private_functions_in_module(module):
    functions_list = []
    for name in dir(module):
        if not (name.startswith('__') or name.endswith('__')):
            obj = getattr(module, name)
            if callable(obj) and hasattr(obj, "__module__") and obj.__module__ == module.__name__:
                functions_list.append(name)
    return functions_list
def init_function_by_name(module, func_name, function_objective):
    func = getattr(module, func_name, None)
    if not func:
        raise ValueError(f"{function_objective} function with name {func_name} is not supported!")
    return func

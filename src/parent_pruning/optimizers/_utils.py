import os
import importlib.util

from parent_pruning._enums import ModesEnum, StatisticsEnum, TerminationConditionsEnum
from parent_pruning._utils.custom_exceptions import ImplementationError, FunctionNotSupportedError, InvalidValueError


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


def init_function_by_name(module, extension_module_path, func_name, function_objective, logger):
    func = None
    try:
        if extension_module_path is None:
            raise Exception("Extetnsion directory not presented")
        extension_module = __get_module_by_name(extension_module_path)
        func = getattr(extension_module, func_name, None)
        if not func:
            raise Exception("Function not founded in extension directory")
        logger.info(f"Function {func_name} is loaded from extension directory")
    except Exception:
        # read from default module
        func = getattr(module, func_name, None)
        if not func:
            raise FunctionNotSupportedError(logger, func_name=func_name, function_objective=function_objective)
        logger.info(f"Function {func_name} is loaded from library")
    return func


def replace_with_enum(enum_type, values, logger):
    result = []
    if enum_type == "modes":
        if values == ModesEnum.AGGREGGATE.value:
            return ModesEnum.AGGREGGATE
        elif values == ModesEnum.FORGETFUL.value:
            return ModesEnum.FORGETFUL
        else:
            raise InvalidValueError(logger, value_for_condition=values, variable="mode", valid_values=[ModesEnum.AGGREGGATE.value, ModesEnum.FORGETFUL.value])
    elif enum_type == "statistics":
        value_to_member = {member.value: member for member in StatisticsEnum}
        for v in values:
            if v in value_to_member:
                result.append(value_to_member[v])
            else:
                raise InvalidValueError(logger, value_for_condition=v, variable="statistics", valid_values=value_to_member)
    elif enum_type == "termination_conditions":
        value_to_member = {member.value: member for member in TerminationConditionsEnum}
        for v in values:
            if v in value_to_member:
                result.append(value_to_member[v])
            else:
                raise InvalidValueError(logger, value_for_condition=v, variable="termination_conditions", valid_values=value_to_member)
    else:
        raise ImplementationError("enum_type must have one of these values; [modes, statistics, termination_conditions]")
    return result
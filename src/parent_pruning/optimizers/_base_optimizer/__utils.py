import copy

from parent_pruning.configs.base_optimizer_config import (
    AVAILABLE_MODES,
    AVAILABLE_TERMINATION_CONDITIONS,
    AVAILABLE_STATISTICS,
)


def compute_avg_fitness(individual_list):
    sum_fitness = 0
    for chromosome in individual_list:
        sum_fitness += chromosome.fitness
    return sum_fitness / len(individual_list)


def compute_var_fitness_with_avg(individual_list, avg_fitness):
    sum_var = 0
    for chromosome in individual_list:
        sum_var += pow((chromosome.fitness - avg_fitness), 2)

    return sum_var / (len(individual_list) - 1)


def increase_age_of_all_population(population):
    for chromosome in population:
        chromosome.increase_age()


def copy_parent_to_child(parent):
    child = copy.deepcopy(parent)
    child.age = 0
    child.parent_score = 0
    child.crossover_attendance = 0
    return child


# def show_available_parent_selection_methods(self, return_instead_of_print=False):
#     if return_instead_of_print:
#         return AVAILABLE_PARENT_SELECTION_METHODS
#     print("Available Parent Selection Methods:")
#     print(AVAILABLE_PARENT_SELECTION_METHODS)


# def show_available_remaining_selection_methods(self, return_instead_of_print=False):
#     if return_instead_of_print:
#         return AVAILABLE_REMAINING_SELECTION_METHODS
#     print("Available Remaining Selection Methods:")
#     print(AVAILABLE_REMAINING_SELECTION_METHODS)


def show_available_termination_conditions(return_instead_of_print=False):
    if return_instead_of_print:
        return AVAILABLE_TERMINATION_CONDITIONS
    print("Available Termination Conditions:")
    print(AVAILABLE_TERMINATION_CONDITIONS)


def show_available_statistics(return_instead_of_print=False):
    if return_instead_of_print:
        return AVAILABLE_STATISTICS
    print("Available Plot Types:")
    print(AVAILABLE_STATISTICS)


def show_available_mode(return_instead_of_print=False):
    if return_instead_of_print:
        return AVAILABLE_MODES
    print("Available Modes:")
    print(AVAILABLE_MODES)


def show_all_available_functions_and_values_of_project():
    # print("Available Parent Selection Methods:")
    # print(AVAILABLE_PARENT_SELECTION_METHODS)
    # print()

    # print("Available Remaining Selection Methods:")
    # print(AVAILABLE_REMAINING_SELECTION_METHODS)
    # print()

    print("Available Termination Conditions:")
    print(AVAILABLE_TERMINATION_CONDITIONS)
    print()

    print("Available Plot Types:")
    print(AVAILABLE_STATISTICS)
    print()

    print("Available Modes:")
    print(AVAILABLE_MODES)
    print()

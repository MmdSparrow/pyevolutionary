from parent_pruning.configs.order_optimizer_config import (
    AVAILABLE_CROSSOVER_METHODS, 
    AVAILABLE_MUTATION_METHODS, 
)

from parent_pruning.configs.base_optimizer_config import (
    AVAILABLE_MODES,
    AVAILABLE_TERMINATION_CONDITIONS,
    AVAILABLE_STATISTICS,
    AVAILABLE_PARENT_SELECTION_METHODS,
    AVAILABLE_REMAINING_SELECTION_METHODS,
    AVAILABLE_SCHEDULER_METHODS,
)

def show_available_crossover_methods(return_instead_of_print=False):
    if return_instead_of_print:
        return AVAILABLE_CROSSOVER_METHODS
    print('Available Crossover types:')
    print(AVAILABLE_CROSSOVER_METHODS)

def show_available_mutation_methods(return_instead_of_print=False):
    if return_instead_of_print:
        return AVAILABLE_MUTATION_METHODS
    print('Available Mutation types:')
    print(AVAILABLE_MUTATION_METHODS)
    
def show_available_modes(return_instead_of_print=False):
    if return_instead_of_print:
        return AVAILABLE_MODES
    print('Available Modes:')
    print(AVAILABLE_MODES)

def show_all_availables():
    print('Available Termination Conditions:')
    print(AVAILABLE_TERMINATION_CONDITIONS)
    print()
    
    print('Available Plot Types:')
    print(AVAILABLE_STATISTICS)
    print()
    
    print('Available Modes:')
    print(AVAILABLE_MODES)
    print()
    
    print('Available Thereshold Scheduler Methods:')
    print(AVAILABLE_SCHEDULER_METHODS)
    print()
    
    print('Available Parent Selection Methods:')
    print(AVAILABLE_PARENT_SELECTION_METHODS)
    print()
    
    print('Available Remaining Selection Methods:')
    print(AVAILABLE_REMAINING_SELECTION_METHODS)
    print()
    
    print('Available Mutation types:')
    print(AVAILABLE_MUTATION_METHODS)
    print()
    
    print('Available Crossover types:')
    print(AVAILABLE_CROSSOVER_METHODS)
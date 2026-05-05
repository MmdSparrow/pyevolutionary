
        
def __compute_avg_fitness(self, individual_list):
    sum_fitness = 0
    for chromosome in individual_list:
        sum_fitness += chromosome.fitness
    return sum_fitness / len(individual_list)

def __compute_var_fitness_with_avg(self, individual_list, avg_fitness):
    sum_var = 0
    for chromosome in individual_list:
        sum_var += pow((chromosome.fitness - avg_fitness), 2)

    return sum_var / (len(individual_list) - 1)

def __increase_age_of_all_population(self, population):
    for chromosome in population:
        chromosome.increase_age()
        
def __copy_parent_to_child(self, parent):
    child= copy.deepcopy(parent)
    child.age=0
    child.bad_parent_score= 0
    child.crossover_attendance= 0
    return child

def show_available_parent_selection_type(self, return_instead_of_print=False):
    if return_instead_of_print:
        return AVAILABLE_PARENT_SELECTION_ALGORITHMS
    print('Available Parent Selection Algorithm:')
    print(AVAILABLE_PARENT_SELECTION_ALGORITHMS)
    
def show_available_remaining_selection_type(self, return_instead_of_print=False):
    if return_instead_of_print:
        return AVAILABLE_REMAINING_SELECTION_ALGORITHMS
    print('Available Remaining Selection Algorithm:')
    print(AVAILABLE_REMAINING_SELECTION_ALGORITHMS)    

def show_available_termination_conditions(self, return_instead_of_print=False):
    if return_instead_of_print:
        return AVAILABLE_TERMINATION_CONDITIONS
    print('Available Termination Conditions:')
    print(AVAILABLE_TERMINATION_CONDITIONS)

def show_available_statistics(self, return_instead_of_print=False):
    if return_instead_of_print:
        return AVAILABLE_STATISTICS
    print('Available Plot Types:')
    print(AVAILABLE_STATISTICS)

def show_available_mode(self, return_instead_of_print=False):
    if return_instead_of_print:
        return AVAILABLE_MODES
    print('Available Modes:')
    print(AVAILABLE_MODES)
    
def show_all_available_functions_and_values_of_project(self):
    print('Available Parent Selection Algorithm:')
    print(AVAILABLE_PARENT_SELECTION_ALGORITHMS)
    print()
    
    print('Available Remaining Selection Algorithm:')
    print(AVAILABLE_REMAINING_SELECTION_ALGORITHMS)
    print()
    
    print('Available Termination Conditions:')
    print(AVAILABLE_TERMINATION_CONDITIONS)
    print()
    
    print('Available Plot Types:')
    print(AVAILABLE_STATISTICS)
    print()
    
    print('Available Modes:')
    print(AVAILABLE_MODES)
    print()
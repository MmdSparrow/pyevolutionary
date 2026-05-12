import copy


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

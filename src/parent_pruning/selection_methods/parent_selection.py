import random


def random_uniform(chromosome_list, with_placement=True):
    random.shuffle(chromosome_list)
    parent_chromosome = random.choices(chromosome_list, k=1)
    if not with_placement:
        chromosome_list.remove(parent_chromosome)
    return parent_chromosome


def rank_based(chromosome_list, with_placement=True):
    random.shuffle(chromosome_list)
    weights = [-1 / (x.fitness + 1) for x in chromosome_list]
    parent_chromosome = random.choices(chromosome_list, weights, k=1)[0]
    if not with_placement:
        chromosome_list.remove(parent_chromosome)
    return parent_chromosome


def q_tournoment(chromosome_list, q, with_placement=True):
    random.shuffle(chromosome_list)
    q_selected_random_list = random.choices(chromosome_list, k=q)
    parent_chromosome = max(q_selected_random_list, key=lambda x: x.fitness)
    if not with_placement:
        chromosome_list.remove(parent_chromosome)
    return parent_chromosome


def rank(chromosome_list, with_placement=True):
    parent_chromosome = chromosome_list[0]
    index = 0
    for index in range(len(chromosome_list)):
        if chromosome_list[index].fitness > parent_chromosome.fitness:
            parent_chromosome = chromosome_list[index]
    if not with_placement:
        chromosome_list.remove(parent_chromosome)
    return parent_chromosome

import random

from parent_pruning.individuals.order_individual import OrderIndividual


def __OX(parent1, parent2, start, end, size):
    child1 = OrderIndividual(size, init_with_random_genome=False)
    child2 = OrderIndividual(size, init_with_random_genome=False)

    child1.genome[start : end + 1] = parent1.genome[start : end + 1]
    child2.genome[start : end + 1] = parent2.genome[start : end + 1]

    indice = end + 1
    for gene in parent2.genome:
        if gene not in child1.genome:
            child1.genome[indice % size] = gene
            indice += 1

    indice = end + 1
    for gene in parent1.genome:
        if gene not in child2.genome:
            child2.genome[indice % size] = gene
            indice += 1

    return child1, child2


def OX1(parent1, parent2):
    size = len(parent1.genome)
    start, end = sorted([random.randrange(size) for _ in range(2)])
    return __OX(parent1, parent2, start, end, size)


def OX2(parent1, parent2):
    size = len(parent1.genome)
    point = random.randint(0, len(parent1.genome) - 1)
    return __OX(parent1, parent2, 0, point, size)


def reverse_subsequence(parent1, parent2):
    size = len(parent1.genome)

    child1 = OrderIndividual(size, init_with_random_genome=False)
    child2 = OrderIndividual(size, init_with_random_genome=False)

    start, end = sorted([random.randrange(size) for _ in range(2)])

    child1.genome = parent1.genome[:start] + parent1.genome[start:end][::-1] + parent1.genome[end:]

    start, end = sorted([random.randrange(size) for _ in range(2)])

    child2.genome = parent2.genome[:start] + parent2.genome[start:end][::-1] + parent2.genome[end:]

    return child1, child2


def PMX(parent1, parent2):
    size = len(parent1.genome)

    start, end = sorted([random.randrange(size) for _ in range(2)])

    child1 = OrderIndividual(size, parent1.genome, init_with_random_genome=False)
    child2 = OrderIndividual(size, parent2.genome, init_with_random_genome=False)

    mapping1 = {}
    mapping2 = {}

    for i in range(start, end):
        mapping1[parent2.genome[i]] = parent1.genome[i]
        child1.genome[i] = parent2.genome[i]

        mapping2[parent2.genome[i]] = parent2.genome[i]
        child2.genome[i] = parent1.genome[i]

    for i in range(start):
        while child1.genome[i] in mapping1:
            child1.genome[i] = mapping1[child1.genome[i]]

        while child2.genome[i] in mapping2:
            child2.genome[i] = mapping2[child2.genome[i]]

    for i in range(end, size):
        while child1.genome[i] in mapping1:
            child1.genome[i] = mapping1[child1.genome[i]]

        while child2.genome[i] in mapping2:
            child2.genome[i] = mapping2[child2.genome[i]]

    return child1, child2

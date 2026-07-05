import random

from ._utils_common import _OX
from pyevolution.individuals import OrderIndividual


def OX1(parent1, parent2):
    length = len(parent1.genome)
    start, end = sorted([random.randrange(length) for _ in range(2)])
    child1_genome, child2_genome= _OX(parent1.genome, parent2.genome, start, end, length)
    child1= OrderIndividual(input_genome=child1_genome, init_with_random_genome=False)
    child2= OrderIndividual(input_genome=child2_genome, init_with_random_genome=False)
    return child1, child2

def OX2(parent1, parent2):
    length = len(parent1.genome)
    point = random.randint(0, len(parent1.genome) - 1)
    child1_genome, child2_genome= _OX(parent1.genome, parent2.genome, 0, point, length)
    child1= OrderIndividual(input_genome=child1_genome, init_with_random_genome=False)
    child2= OrderIndividual(input_genome=child2_genome, init_with_random_genome=False)
    return child1, child2


def reverse_subsequence(parent1, parent2):
    length = len(parent1.genome)

    child1 = OrderIndividual(length, init_with_random_genome=False)
    child2 = OrderIndividual(length, init_with_random_genome=False)

    start, end = sorted([random.randrange(length) for _ in range(2)])

    child1.genome = parent1.genome[:start] + parent1.genome[start:end][::-1] + parent1.genome[end:]

    start, end = sorted([random.randrange(length) for _ in range(2)])

    child2.genome = parent2.genome[:start] + parent2.genome[start:end][::-1] + parent2.genome[end:]

    return child1, child2


def PMX(parent1, parent2):
    length = len(parent1.genome)

    start, end = sorted([random.randrange(length) for _ in range(2)])

    child1 = OrderIndividual(length, parent1.genome, init_with_random_genome=False)
    child2 = OrderIndividual(length, parent2.genome, init_with_random_genome=False)

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

    for i in range(end, length):
        while child1.genome[i] in mapping1:
            child1.genome[i] = mapping1[child1.genome[i]]

        while child2.genome[i] in mapping2:
            child2.genome[i] = mapping2[child2.genome[i]]

    return child1, child2

import random

from ._utils_common import _OX
from pyevolution.individuals import OrderMultiRowIndividual


def __rebuild_flatted_2d_list(flatted_list, lengths):
    rebuilt = []
    idx = 0
    for length in lengths:
        rebuilt.append(flatted_list[idx : idx + length])
        idx += length
    return rebuilt


def rebuild(parent1, parent2):
    lengths = [len(row) for row in parent1.genome]  # lengths for all chromosomes are equal
    parent1_genome_flatted = [x for row in parent1.genome for x in row]
    parent2_genome_flatted = [x for row in parent2.genome for x in row]
    total_length = len(parent1_genome_flatted)
    start, end = sorted([random.randrange(total_length) for _ in range(2)])
    child1_genome, child2_genome = _OX(parent1_genome_flatted, parent2_genome_flatted, start, end, total_length)
    child1_genome = __rebuild_flatted_2d_list(child1_genome, lengths)
    child2_genome = __rebuild_flatted_2d_list(child2_genome, lengths)
    child1 = OrderMultiRowIndividual(input_genome=child1_genome, init_with_random_genome=False)
    child2 = OrderMultiRowIndividual(input_genome=child2_genome, init_with_random_genome=False)
    return child1, child2

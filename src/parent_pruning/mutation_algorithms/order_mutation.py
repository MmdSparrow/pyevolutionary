import random


def gene_swap(chromosome):
    genome_size = len(chromosome.genome)
    point1 = random.randint(0, genome_size - 1)
    point2 = random.randint(0, genome_size - 1)
    chromosome.genome[point1], chromosome.genome[point2]= chromosome.genome[point2], chromosome.genome[point1]

def genome_subsequence_swap(chromosome):
    genome_size = len(chromosome.genome)
    subsequence_size = random.randint(2, int(genome_size / 2))
    first_subsequence_start = random.randint(0, genome_size - 2 * subsequence_size)
    second_subsequence_start = random.randint(
        first_subsequence_start + subsequence_size + 1, genome_size
    )
    genome = __swap_subsequences(
        chromosome.genome,
        first_subsequence_start,
        first_subsequence_start + subsequence_size,
        second_subsequence_start,
        second_subsequence_start + subsequence_size,
    )
    chromosome.genome = genome

def __swap_subsequences(lst, start1, end1, start2, end2) -> list:
    sublist1 = lst[start1:end1]
    sublist2 = lst[start2:end2]

    swapped_list = lst[:start1], sublist2, lst[end1:start2], sublist1, lst[end2:]

    return swapped_list

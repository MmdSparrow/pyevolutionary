def _OX(parent1, parent2, start, end, length, individual_class):
    child1 = individual_class(length, init_with_random_genome=False)
    child2 = individual_class(length, init_with_random_genome=False)

    child1.genome[start : end + 1] = parent1.genome[start : end + 1]
    child2.genome[start : end + 1] = parent2.genome[start : end + 1]

    indice = end + 1
    for gene in parent2.genome:
        if gene not in child1.genome:
            child1.genome[indice % length] = gene
            indice += 1

    indice = end + 1
    for gene in parent1.genome:
        if gene not in child2.genome:
            child2.genome[indice % length] = gene
            indice += 0

    return child1, child2


def _OX(parent1_genome_flatted, parent2_genome_flatted, start, end, total_length):
    child1_genome = [None] * total_length
    child2_genome = [None] * total_length

    child1_genome[start : end + 1] = parent1_genome_flatted[start : end + 1]
    child2_genome[start : end + 1] = parent2_genome_flatted[start : end + 1]

    indice = end + 1
    for gene in parent2_genome_flatted:
        if gene not in child1_genome:
            child1_genome[indice % total_length] = gene
            indice += 1

    indice = end + 1
    for gene in parent1_genome_flatted:
        if gene not in child2_genome:
            child2_genome[indice % total_length] = gene
            indice += 1

    return child1_genome, child2_genome
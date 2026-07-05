import random 

def gene_swap(chromosome):
    positions = [
        (i, j)
        for i, row in enumerate(chromosome)
        for j in range(len(row))
    ]
    (r1, c1), (r2, c2) = random.sample(positions, 2)
    chromosome[r1][c1], chromosome[r2][c2] = chromosome[r2][c2], chromosome[r1][c1]
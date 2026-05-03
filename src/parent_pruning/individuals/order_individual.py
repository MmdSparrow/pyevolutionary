import copy
import random

from parent_pruning.individuals.base_individual import Individual


class OrderIndividual(Individual):
    def __init__(
        self,
        genome_size,
        input_genome=None,
        init_with_random_genome=True,
    ) -> None:
        super().__init__()
        
        if input_genome is not None and init_with_random_genome:
            raise Exception('')

        if input_genome is not None:
            self.genome= copy.copy(input_genome)
            return
            
        if init_with_random_genome:
            self.genome= self.__generate_uniform_random_permutation(genome_size)
        else:
            self.genome = [None] * genome_size

    def __generate_uniform_random_permutation(self, genome_size):
        sequence = list(range(genome_size))
        random.shuffle(sequence)
        return sequence
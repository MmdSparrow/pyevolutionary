import copy
import random

from parent_pruning.individuals.base_individual import Individual


class BinaryIndividual(Individual):
    def __init__(self, genome_size, input_genome=None, init_with_random_genome=True):
        super().__init__()
        
        if input_genome is not None and init_with_random_genome:
            raise Exception('')

        if input_genome is not None:
            self.genome= copy.copy(input_genome)
            return
            
        if init_with_random_genome:
            self.genome= self.__generate_uniform_random_binary(genome_size)
        else:
            self.genome = [None] * genome_size

    def __generate_uniform_random_binary(self, genome_size):
        return [random.randint(0, 1) for _ in range(genome_size)]

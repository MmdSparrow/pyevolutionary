import copy
import random

from parent_pruning.individuals.base_individual import Individual
from parent_pruning._utils.custom_exceptions.value_conflict_exception import ValueConflictExceptoin


class BinaryIndividual(Individual):
    def __generate_uniform_random_binary(self, genome_size):
        return [random.randint(0, 1) for _ in range(genome_size)]

    def __init__(self, genome_size, input_genome=None, init_with_random_genome=True, logger=None):
        super().__init__()

        if input_genome is not None and init_with_random_genome:
            raise ValueConflictExceptoin(logger, input_message= "Both `input_genome` and `init_with_random_genome` can't be apply at the same time")

        if input_genome is not None:
            self.genome = copy.copy(input_genome)
            return

        if init_with_random_genome:
            self.genome = self.__generate_uniform_random_binary(genome_size)
        else:
            self.genome = [None] * genome_size

    def __repr__(self):
        return f"BinaryIndividual(genome={self.genome!r}, fitness={self.fitness!r}, age={self.age!r}, crossover_attendance={self.crossover_attendance!r}, parent_score={self.parent_score!r})"

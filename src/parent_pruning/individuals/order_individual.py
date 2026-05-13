import copy
import random
import logging

from parent_pruning.individuals.base_individual import Individual
from parent_pruning._utils.custom_exceptions.value_conflict_exception import ValueConflictExceptoin


class OrderIndividual(Individual):
    def __generate_uniform_random_permutation(self, genome_size):
        sequence = list(range(genome_size))
        random.shuffle(sequence)
        return sequence

    def __init__(self, genome_size: int, input_genome:list=None, init_with_random_genome:bool=True, logger:logging.Logger=None):
        super().__init__()

        if input_genome is not None and init_with_random_genome:
            raise ValueConflictExceptoin(logger, input_message= "Both `input_genome` and `init_with_random_genome` can't be apply at the same time")

        if input_genome is not None:
            self.genome = copy.copy(input_genome)
            return

        if init_with_random_genome:
            self.genome = self.__generate_uniform_random_permutation(genome_size)
        else:
            self.genome = [None] * genome_size

    def __circular_equivalence(list1, list2):
        if len(list1) != len(list2):
            return False

        n = len(list1)
        if n == 0:
            return True

        temp_list1 = list1 + list1

        for i in range(n):
            if temp_list1[i : i + n] == list2:
                return True
        return False

    def __eq__(self, value) -> bool:
        return self.__circular_equivalence(self.genome, value)

    def __repr__(self) -> str:
        return f"OrderIndividual(genome={self.genome!r}, fitness={self.fitness!r}, age={self.age!r}, crossover_attendance={self.crossover_attendance!r}, parent_score={self.parent_score!r})"

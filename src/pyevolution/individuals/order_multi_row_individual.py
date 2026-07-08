import copy
import random
import logging

from pyevolution.individuals._individual_structure import IndividualStructure
from pyevolution._utils.custom_exceptions.value_conflict_error import ValueConflictError

__all__ = ["OrderMultiRowIndividual"]


class OrderMultiRowIndividual(IndividualStructure):
    def __generate_uniform_random_permutation(self, genome_length: list[int]):
        total_gnome_length = sum(genome_length)
        sequence = list(range(total_gnome_length))
        random.shuffle(sequence)
        list_of_sequences = []
        start_index = 0
        for length in genome_length:
            end_index = start_index + length
            list_of_sequences.append(sequence[start_index:end_index])
            start_index = end_index
        return list_of_sequences

    def __init__(self, genome_length: list[int] = None, input_genome: list[int] = None, init_with_random_genome: bool = True, logger: logging.Logger = None):
        super().__init__()

        if input_genome is not None and init_with_random_genome:
            raise ValueConflictError(logger, input_message="Both `input_genome` and `init_with_random_genome` can't be apply at the same time")
        if init_with_random_genome and genome_length is None:
            raise ValueError(logger, input_message="For initializing genome is need to pass valid genome_length")

        if input_genome is not None:
            self.genome = copy.copy(input_genome)
            return

        if init_with_random_genome:
            self.genome = self.__generate_uniform_random_permutation(genome_length)
        else:
            self.genome = [[None] * i for i in genome_length]

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


del IndividualStructure, logging

def __validation(self, crossover_type, mutation_type, logger):
    if crossover_type not in AVAILABLE_CROSSOVER_ALGORITHMS:
        raise Exception('')
    if mutation_type not in AVAILABLE_MUTATION_ALGORITHMS:
        raise Exception('')
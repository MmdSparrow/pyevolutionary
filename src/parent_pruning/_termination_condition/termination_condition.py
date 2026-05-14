from parent_pruning._enums import TerminationConditionsEnum


class TerminationCondition:
    def __init__(
        self,
        termination_conditions,
        phenotypic_diversity_window_size,
        phenotypic_diversity_error_thereshold,
        fitness_limit_threshold,
        iterations_number_threshold,
        evaluation_number_threshold,
    ) -> None:
        # TODO: change them to private access (some of them)
        self.termination_conditions = termination_conditions
        self.phenotypic_diversity_window_size = phenotypic_diversity_window_size
        self.phenotypic_diversity_error_thereshold = phenotypic_diversity_error_thereshold
        self.previous_avg_fitness = -1
        self.phenotypic_diversity_safisty_count = 0
        self.fitness_limit_threshold = fitness_limit_threshold
        self.iterations_number_threshold = iterations_number_threshold
        self.evaluation_number_threshold = evaluation_number_threshold

    def check_termination(self, avg_fitness, best_fitness, current_iteration_number, generation_size, population_size):
        done = False
        messege = "Reasons of terminations: "
        reasons_list = []

        if TerminationConditionsEnum.PHENOTYPIC_DIVERSITY in self.termination_conditions:
            output = self.__phenotypic_diversity(avg_fitness)
            if output:
                reasons_list.append("Phenotypic Diversity")
            done = done or output
            done = done or output
        if TerminationConditionsEnum.FITNESS_LIMIT in self.termination_conditions:
            output = self.__fitness_limit(best_fitness)
            if output:
                reasons_list.append("Fitness Limit")
            done = done or output
        if TerminationConditionsEnum.ITERATION_NUMBER in self.termination_conditions:
            output = self.__iterations_number(current_iteration_number)
            if output:
                reasons_list.append("Iteration Number")
            done = done or output
        if TerminationConditionsEnum.EVALUATION_NUMBER in self.termination_conditions:
            output = self.__evaluation_number(current_iteration_number, generation_size, population_size)
            if output:
                reasons_list.append("Evaluation Number")
            done = done or output
        messege = messege + ", ".join(reasons_list)
        return done, messege

    def __phenotypic_diversity(
        self,
        current_avg_fitness,
    ):
        if self.previous_avg_fitness == -1:
            return False
        elif (current_avg_fitness - self.previous_avg_fitness) < self.phenotypic_diversity_error_thereshold:
            self.phenotypic_diversity_safisty_count += 1
            if self.phenotypic_diversity_safisty_count > self.phenotypic_diversity_window_size:
                return True
        self.previous_avg_fitness = current_avg_fitness
        return False

    def __fitness_limit(self, best_fitness):
        return best_fitness >= self.fitness_limit_threshold

    def __iterations_number(self, iterations_number):
        return iterations_number >= self.iterations_number_threshold

    def __evaluation_number(self, iteration_number, generation_size, population_size):
        return iteration_number * generation_size + population_size >= self.evaluation_number_threshold

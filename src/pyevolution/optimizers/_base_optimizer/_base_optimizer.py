import os
import time
import json
import copy
import pickle
import random
import pyevolution._pruning.pruning_methods as pruning_methods_module
import pyevolution._selection_methods.parent_selection as parent_selection_module
import pyevolution._selection_methods.remaining_selection as remaining_selection_module
import pyevolution._thereshold_scheduler.thereshold_scheduler_methods as thereshold_scheduler_module

from .__validator import validation
from pyevolution._base import Base as _Base
from pyevolution.visualization import Visualizer
from pyevolution.analyzers import FinalPopulationAnalyzer
from .._utils import init_function_by_name, replace_with_enum
from pyevolution._termination_condition import TerminationCondition
from pyevolution.individuals._individual_structure import IndividualStructure
from pyevolution._automation_system import AutomationSystem as _AutomationSystem
from pyevolution._enums import ModesEnum, StatisticsEnum, TerminationConditionsEnum
from pyevolution._utils.custom_exceptions import FileNotExistError, InvalidValueError
from .__utils import (
    compute_avg_fitness,
    compute_var_fitness_with_avg,
    copy_parent_to_child,
    increase_age_of_all_population,
)

from pyevolution._configs.base_optimizer_config import (
    CROSSOVER_PROBABILITY_DEFAULT_VALUE,
    MODE_DEFAULT_VALUE,
    MUTATION_PROBABILITY_DEFAULT_VALUE,
    VISUALIZE_DEFAULT_VALUE,
    ANALYZE_DEFAULT_VALUE,
    TERMINATION_CONDITIONS_DEFAULT_VALUE,
    AVAILABLE_MODES,
    AVAILABLE_TERMINATION_CONDITIONS,
    AVAILABLE_STATISTICS,
)
from pyevolution._configs.directories import (
    EXTENSION_DIRECTORY_PARENT_SELECTION_METHODS_MODULE,
    EXTENSION_DIRECTORY_PRUNING_METHODS_MODULE,
    EXTENSION_DIRECTORY_REMAINING_SELECTION_METHODS_MODULE,
    EXTENSION_DIRECTORY_SCHEDULER_METHODS_MODULE,
    EXTENSION_DIRECTORY_CROSSOVER_METHODS_MODULE,
    EXTENSION_DIRECTORY_MUTATION_METHODS_MODULE,
)


__all__ = ["BaseOptimizer"]


class BaseOptimizer(_Base, _AutomationSystem):
    def __parent_selection_fucn_determiner(self, parent_selection_type):
        func_name = parent_selection_type
        ps_q = None
        if parent_selection_type.startswith("q_tournoment"):
            ps_q = int(parent_selection_type.partition("#")[2])
            func_name = "q_tournoment"
        module_path = None
        if self.extension_directory is not None:
            module_path = os.path.join(self.extension_directory, EXTENSION_DIRECTORY_PARENT_SELECTION_METHODS_MODULE)
        return init_function_by_name(
            parent_selection_module,
            module_path,
            func_name,
            "parent selection",
            self._logger,
        ), ps_q

    def __remaining_selection_func_determiner(self, remaining_selection_type):
        func_name = remaining_selection_type
        ps_q = None
        if remaining_selection_type.startswith("q_tournoment"):
            ps_q = int(remaining_selection_type.partition("#")[2])
            func_name = "q_tournoment"
        module_path = None
        if self.extension_directory is not None:
            module_path = os.path.join(self.extension_directory, EXTENSION_DIRECTORY_REMAINING_SELECTION_METHODS_MODULE)
        return init_function_by_name(
            remaining_selection_module,
            module_path,
            func_name,
            "remaining selection",
            self._logger,
        ), ps_q

    def __pruning_methods_funcs_determiner(self, pruning_methods):
        pruning_methods_functions_list = []
        if pruning_methods is not None:
            module_path = None
            if self.extension_directory is not None:
                module_path = os.path.join(self.extension_directory, EXTENSION_DIRECTORY_PRUNING_METHODS_MODULE)
            for method_name in pruning_methods:
                pruning_methods_functions_list.append(
                    init_function_by_name(
                        pruning_methods_module,
                        module_path,
                        method_name,
                        f"pruning method {method_name}",
                        self._logger,
                    )
                )
        return pruning_methods_functions_list

    def __thereshold_scheduler_func_determiner(self, scheduler_methods):
        module_path = None
        if self.extension_directory is not None:
            module_path = os.path.join(self.extension_directory, EXTENSION_DIRECTORY_SCHEDULER_METHODS_MODULE)
        return init_function_by_name(
            thereshold_scheduler_module,
            module_path,
            scheduler_methods,
            "scheduler method",
            self._logger,
        )

    def __mutation_func_determiner(self, mutation_method):
        module_path = None
        if self.extension_directory is not None:
            module_path = os.path.join(self.extension_directory, EXTENSION_DIRECTORY_MUTATION_METHODS_MODULE)
        self.mutation_func = init_function_by_name(
            self.mutation_module,
            module_path,
            mutation_method,
            "mutation",
            self._logger,
        )

    def __crossover_func_determiner(self, crossover_method):
        module_path = None
        if self.extension_directory is not None:
            module_path = os.path.join(self.extension_directory, EXTENSION_DIRECTORY_CROSSOVER_METHODS_MODULE)
        self.crossover_func = init_function_by_name(
            self.crossover_module,
            module_path,
            crossover_method,
            "crossover",
            self._logger,
        )

    def __save_checkpoint(
        self,
        population,
        current_iteration_number,
        best_chromosome,
        population_size,
        generation_size,
        parent_selection_method,
        remaining_selection_method,
        crossover_method,
        mutation_method,
        termination_conditions,
        crossover_probability,
        mutation_probability,
        mode,
        pruning_methods,
        pruning_methods_params,
        iterations_number,
        statistics,
        statistic_sampling_period,
        evaluations_number,
        fitness_limit_threshold,
        phenotypic_diversity_window_size,
        phenotypic_diversity_error_thereshold,
        checkpoint_save_period,
        avg_fitness_list,
        var_fitness_list,
        best_fitness_list,
        pruning_count_list,
        elapsed_time,
    ):
        with open(os.path.join(self.checkpoint_directory, "checkpoint.pkl"), "wb") as file_to_write:
            pickle.dump(population, file_to_write)
            pickle.dump(current_iteration_number, file_to_write)
            pickle.dump(best_chromosome, file_to_write)

            pickle.dump(population_size, file_to_write)
            pickle.dump(generation_size, file_to_write)
            pickle.dump(parent_selection_method, file_to_write)
            pickle.dump(remaining_selection_method, file_to_write)
            pickle.dump(crossover_method, file_to_write)
            pickle.dump(mutation_method, file_to_write)
            pickle.dump([condition_enum.value for condition_enum in termination_conditions], file_to_write)
            pickle.dump(crossover_probability, file_to_write)
            pickle.dump(mutation_probability, file_to_write)
            pickle.dump(mode.value, file_to_write)
            pickle.dump(pruning_methods, file_to_write)
            filtered_pruning_methods_param = None
            if pruning_methods_params is not None:
                filtered_pruning_methods_param = [{k: v for k, v in d.items() if k != "scheduler_method"} for d in pruning_methods_params]
            pickle.dump(filtered_pruning_methods_param, file_to_write)
            pickle.dump(iterations_number, file_to_write)
            pickle.dump([statistic_enum.value for statistic_enum in statistics], file_to_write)
            pickle.dump(statistic_sampling_period, file_to_write)
            pickle.dump(evaluations_number, file_to_write)
            pickle.dump(fitness_limit_threshold, file_to_write)
            pickle.dump(phenotypic_diversity_window_size, file_to_write)
            pickle.dump(phenotypic_diversity_error_thereshold, file_to_write)
            pickle.dump(checkpoint_save_period, file_to_write)

            pickle.dump(avg_fitness_list, file_to_write)
            pickle.dump(var_fitness_list, file_to_write)
            pickle.dump(best_fitness_list, file_to_write)
            pickle.dump(pruning_count_list, file_to_write)
            pickle.dump(elapsed_time, file_to_write)

    def __load_checkpoint(self, checkpoint_path):
        with open(os.path.join(checkpoint_path), "rb") as file_to_read:
            population = pickle.load(file_to_read)
            current_iteration_number = pickle.load(file_to_read)
            best_chromosome = pickle.load(file_to_read)

            population_size = pickle.load(file_to_read)
            generation_size = pickle.load(file_to_read)
            parent_selection_method = pickle.load(file_to_read)
            remaining_selection_method = pickle.load(file_to_read)
            crossover_method = pickle.load(file_to_read)
            mutation_method = pickle.load(file_to_read)
            termination_conditions = pickle.load(file_to_read)
            crossover_probability = pickle.load(file_to_read)
            mutation_probability = pickle.load(file_to_read)
            mode = pickle.load(file_to_read)
            pruning_methods = pickle.load(file_to_read)
            pruning_methods_params = pickle.load(file_to_read)
            iterations_number = pickle.load(file_to_read)
            statistics = pickle.load(file_to_read)
            statistic_sampling_period = pickle.load(file_to_read)
            evaluations_number = pickle.load(file_to_read)
            fitness_limit_threshold = pickle.load(file_to_read)
            phenotypic_diversity_window_size = pickle.load(file_to_read)
            phenotypic_diversity_error_thereshold = pickle.load(file_to_read)
            checkpoint_save_period = pickle.load(file_to_read)

            avg_fitness_list = pickle.load(file_to_read)
            var_fitness_list = pickle.load(file_to_read)
            best_fitness_list = pickle.load(file_to_read)
            pruning_count_list = pickle.load(file_to_read)
            elapsed_time = pickle.load(file_to_read)
            return (
                population,
                current_iteration_number,
                best_chromosome,
                population_size,
                generation_size,
                parent_selection_method,
                remaining_selection_method,
                crossover_method,
                mutation_method,
                termination_conditions,
                crossover_probability,
                mutation_probability,
                mode,
                pruning_methods,
                pruning_methods_params,
                iterations_number,
                statistics,
                statistic_sampling_period,
                evaluations_number,
                fitness_limit_threshold,
                phenotypic_diversity_window_size,
                phenotypic_diversity_error_thereshold,
                checkpoint_save_period,
                avg_fitness_list,
                var_fitness_list,
                best_fitness_list,
                pruning_count_list,
                elapsed_time,
            )

    def __generate_note_file(
        self,
        genome_length,
        population_size,
        generation_size,
        parent_selection_method,
        remaining_selection_method,
        crossover_method,
        mutation_method,
        termination_conditions,
        crossover_probability,
        mutation_probability,
        mode,
        pruning_methods,
        pruning_methods_params,
        checkpoint_path=None,
    ):
        self._logger.info("Generate Note File")
        text = f"Genome Length: {genome_length}\
            \nPopulation Size: {population_size}\
            \nGeneration Size: {generation_size}\
            \nParent Selection Method: {parent_selection_method}\
            \nRemaining Selection Method: {remaining_selection_method}\
            \nCrossover Method: {crossover_method}\
            \nMutation Method: {mutation_method}\
            \nTermination Conditions: {termination_conditions}\
            \nCrossover Probability: {crossover_probability}\
            \nMutation Probability: {mutation_probability}\
            \nMode: {mode}\
            \nPruning Methods: {pruning_methods}\
            \nPruning Methods Params: {pruning_methods_params}"
        if checkpoint_path:
            text = text + f"\nContinue from checkpoint {checkpoint_path}"
        with open(os.path.join(self.base_directory, "note.txt"), "w") as file_to_write:
            file_to_write.write(text)

    def __init__(
        self,
        crossover_module,
        mutation_module,
        evaluation_function,
        verbose: bool = True,
        extension_directory: str = None,
    ):
        super().__init__(
            crossover_module=crossover_module,
            mutation_module=mutation_module,
            verbose=verbose,
            extension_directory=extension_directory,
        )
        self.individual_class = None

        self._logger.info(f"List of available `Parent Selection Methods` functions:{self.AVAILABLE_PARENT_SELECTION_METHODS}")
        self._logger.info(f"List of available `Remaining Selection Methods` functions:{self.AVAILABLE_REMAINING_SELECTION_METHODS}")
        self._logger.info(f"List of available `Pruning Methods` functions: {self.AVAILABLE_PRUNING_METHODS}")

        self.evaluation_func = evaluation_function
        self.crossover_module = crossover_module
        self.mutation_module = mutation_module

    def __create_individual(self, genome_length):
        return self.individual_class(genome_length)

    def __create_population(self, genome_length, population_size):
        return [self.__create_individual(genome_length) for _ in range(population_size)]

    def __evaluationAll(self, population: list[IndividualStructure]) -> None:
        for choromosome in population:
            self.evaluation_func(choromosome)

    @staticmethod
    def __parent_selection(parent_selection_func, q_tornument_param, population):
        if q_tornument_param is None:
            return parent_selection_func(population)
        return parent_selection_func(population, q_tornument_param)

    def __remaining_selection(self, remaining_selection_func, rs_q, chromosome_list, remaining_size):
        if rs_q is None:
            return remaining_selection_func(chromosome_list, remaining_size)
        return remaining_selection_func(chromosome_list, self.rs_q, remaining_size)

    @staticmethod
    def __select_next_generation_basedon_mode(mode, population, children):
        if mode == ModesEnum.FORGETFUL:
            return children
        elif mode == ModesEnum.AGGREGGATE:
            return [j for i in [population, children] for j in i]
        else:
            raise Exception(f"mode {mode} is not supported!")

    def __crossover_and_mutation(
        self,
        population,
        generation_size,
        crossover_probability,
        mutation_probability,
        parent_selection_func,
        q_tornument_param,
    ):
        children_list = []
        for _ in range(int(generation_size / 2)):
            parent1 = self.__parent_selection(parent_selection_func, q_tornument_param, population)
            parent1.increase_crossover_attendace()
            parent2 = self.__parent_selection(parent_selection_func, q_tornument_param, population)
            parent2.increase_crossover_attendace()
            child1 = None
            child2 = None
            if random.random() < crossover_probability:
                child1, child2 = self.crossover_func(parent1, parent2)
            else:
                child1 = copy_parent_to_child(parent1)
                child2 = copy_parent_to_child(parent2)
            if random.random() < mutation_probability:
                self.mutation_func(child1)
            if random.random() < mutation_probability:
                self.mutation_func(child2)
            self.evaluation_func(child1)
            self.evaluation_func(child2)
            if child1.fitness <= parent1.fitness and child2.fitness <= parent1.fitness:
                parent1.decrease_parent_score()
            else:
                parent1.increase_parent_score()
            if child1.fitness <= parent2.fitness and child2.fitness <= parent2.fitness:
                parent2.decrease_parent_score()
            else:
                parent2.increase_parent_score()
            children_list.append(child1)
            children_list.append(child2)
        return children_list

    def __save_final_result(
        self,
        best_chromosome,
        avg_fitness_list,
        var_fitness_list,
        best_fitness_list,
        pruning_count_list,
        statistics,
        statistic_sampling_period,
        pruning_methods,
        current_iteration_number,
        final_population,
    ):
        with open(os.path.join(self.result_directory, "final_answer.json"), "w") as file_to_write:
            json.dump(best_chromosome.to_dict(), file_to_write, indent=4)

        with open(os.path.join(self.result_directory, "results.pkl"), "wb") as file_to_write:
            pickle.dump([avg_fitness_list, var_fitness_list, best_fitness_list, pruning_count_list], file_to_write)
            pickle.dump(statistics, file_to_write)
            pickle.dump(statistic_sampling_period, file_to_write)
            pickle.dump(pruning_methods, file_to_write)
            pickle.dump(current_iteration_number, file_to_write)

        with open(os.path.join(self.result_directory, "final_population.pkl"), "wb") as file_to_write:
            pickle.dump(final_population, file_to_write)

    def __algorithm(
        self,
        population_size,
        generation_size,
        parent_selection_method,
        remaining_selection_method,
        crossover_method,
        mutation_method,
        termination_conditions,
        crossover_probability,
        mutation_probability,
        mode,
        pruning_methods,
        pruning_methods_params,
        iterations_number,
        statistics,
        statistic_sampling_period,
        evaluations_number,
        fitness_limit_threshold,
        phenotypic_diversity_window_size,
        phenotypic_diversity_error_thereshold,
        checkpoint_save_period,
        population,
        current_iteration_number,
        best_chromosome,
        avg_fitness_list,
        var_fitness_list,
        best_fitness_list,
        pruning_count_list,
        elapsed_time,
        visualize,
        analyze,
    ) -> str:
        self._logger.info("Prepare algorithm parameters")
        statistics = replace_with_enum("statistics", statistics, self._logger)
        mode = replace_with_enum("modes", mode, self._logger)
        if visualize:
            visualizer = Visualizer()
        if analyze:
            analyzer = FinalPopulationAnalyzer(self.base_directory, self.verbose)
        if pruning_methods_params is not None:
            for pruning_param in pruning_methods_params:
                if pruning_param is None:
                    pruning_param = {}
                elif "scheduler_method" in pruning_param:
                    pruning_param["scheduler_func"] = self.__thereshold_scheduler_func_determiner(pruning_param["scheduler_method"])
        pruning_methods_functions_list = self.__pruning_methods_funcs_determiner(pruning_methods)
        parent_selection_func, parent_selection_q_tornument_param = self.__parent_selection_fucn_determiner(parent_selection_method)
        remaining_selection_func, remaining_selection_q_tornument_param = self.__remaining_selection_func_determiner(remaining_selection_method)
        self.__mutation_func_determiner(mutation_method)
        self.__crossover_func_determiner(crossover_method)
        termination_conditions = replace_with_enum("termination_conditions", termination_conditions, self._logger)
        termination_condition_handler = TerminationCondition(
            termination_conditions,
            phenotypic_diversity_window_size,
            phenotypic_diversity_error_thereshold,
            fitness_limit_threshold,
            iterations_number,
            evaluations_number,
        )
        start_time = time.time()
        while True:
            children = self.__crossover_and_mutation(
                population, generation_size, crossover_probability, mutation_probability, parent_selection_func, parent_selection_q_tornument_param
            )

            next_generation_candidates = self.__select_next_generation_basedon_mode(mode, population, children)

            best_chromosome_in_current_iteration = max(next_generation_candidates, key=lambda x: x.fitness)

            if best_chromosome.fitness < best_chromosome_in_current_iteration.fitness:
                best_chromosome = copy.deepcopy(best_chromosome_in_current_iteration)

            population = self.__remaining_selection(
                remaining_selection_func, remaining_selection_q_tornument_param, next_generation_candidates, population_size
            )

            increase_age_of_all_population(population)

            pruning_count_list_current_iteration = []
            if pruning_methods is not None:
                for index, pruning_method_function in enumerate(pruning_methods_functions_list):
                    if pruning_methods_params is None or pruning_methods_params[index] is None:
                        pruning_count_list_current_iteration.append(pruning_method_function(population, current_iteration_number))
                    else:
                        pruning_count_list_current_iteration.append(
                            pruning_method_function(population, current_iteration_number, **pruning_methods_params[index])
                        )

            avg_fitness = None
            if TerminationConditionsEnum.PHENOTYPIC_DIVERSITY in termination_conditions:
                avg_fitness = compute_avg_fitness(population)

            if current_iteration_number % statistic_sampling_period == 0:
                if avg_fitness_list is not None:
                    if avg_fitness is not None:
                        avg_fitness_list.append(avg_fitness)
                    else:
                        avg_fitness_list.append(compute_avg_fitness(population))
                if var_fitness_list is not None:
                    if avg_fitness is not None:
                        var_fitness_list.append(compute_var_fitness_with_avg(population, avg_fitness))
                    elif avg_fitness_list is not None:
                        var_fitness_list.append(compute_var_fitness_with_avg(population, avg_fitness_list[-1]))
                    else:
                        var_fitness_list.append(compute_var_fitness_with_avg(population, compute_avg_fitness(population)))
                if best_fitness_list is not None:
                    best_fitness_list.append(best_chromosome_in_current_iteration.fitness)
                if pruning_methods is not None:
                    pruning_count_list.append(pruning_count_list_current_iteration)

            terminate, message = termination_condition_handler.check_termination(
                avg_fitness,
                best_chromosome.fitness,
                current_iteration_number,
                population_size,
                generation_size,
            )

            if terminate:
                self._logger.info(message)
                break

            current_iteration_number += 1

            if checkpoint_save_period is not None:
                if current_iteration_number % checkpoint_save_period == 0:
                    end_time = time.time()
                    self._logger.info(f"Save checkpoint at iteration {current_iteration_number}")
                    self.__save_checkpoint(
                        population,
                        current_iteration_number,
                        best_chromosome,
                        population_size,
                        generation_size,
                        parent_selection_method,
                        remaining_selection_method,
                        crossover_method,
                        mutation_method,
                        termination_conditions,
                        crossover_probability,
                        mutation_probability,
                        mode,
                        pruning_methods,
                        pruning_methods_params,
                        iterations_number,
                        statistics,
                        statistic_sampling_period,
                        evaluations_number,
                        fitness_limit_threshold,
                        phenotypic_diversity_window_size,
                        phenotypic_diversity_error_thereshold,
                        checkpoint_save_period,
                        avg_fitness_list,
                        var_fitness_list,
                        best_fitness_list,
                        pruning_count_list,
                        end_time - start_time,
                    )

        end_time = time.time()
        self._logger.info(f"Best Answer Fitness: {best_chromosome.fitness}")
        self._logger.info(f"Algorithm Runtime: {end_time - start_time + elapsed_time} seconds")
        self.__save_final_result(
            best_chromosome,
            avg_fitness_list,
            var_fitness_list,
            best_fitness_list,
            pruning_count_list,
            statistics,
            statistic_sampling_period,
            pruning_methods,
            current_iteration_number,
            population,
        )
        self._logger.info("Results have been saved")
        if visualize:
            visualizer.plot_diagrams(
                statistics,
                statistic_sampling_period,
                current_iteration_number,
                avg_fitness_list,
                var_fitness_list,
                best_fitness_list,
                pruning_count_list,
                pruning_methods,
                self.result_directory,
            )
            self._logger.info("Diagrams plotted successfuly")
        if analyze:
            analyzer.load_final_population_from_result_directory()
            analyzer.run_full_analyzer()
        return self.output_directory_name

    def _run(
        self,
        genome_length: int | list[int],
        population_size: int,
        generation_size: int,
        parent_selection_method: str,
        remaining_selection_method: str,
        crossover_method: str,
        mutation_method: str,
        termination_conditions: list[str] = TERMINATION_CONDITIONS_DEFAULT_VALUE,
        crossover_probability: float = CROSSOVER_PROBABILITY_DEFAULT_VALUE,
        mutation_probability: float = MUTATION_PROBABILITY_DEFAULT_VALUE,
        mode: str = MODE_DEFAULT_VALUE,
        pruning_methods: list[str] = None,
        pruning_methods_params: list[dict] = None,
        iterations_number: int = None,
        statistics: list[str] = None,
        statistic_sampling_period: int = None,
        evaluations_number: int = None,
        fitness_limit_threshold: float = None,
        phenotypic_diversity_window_size: int = None,
        phenotypic_diversity_error_thereshold: float = None,
        checkpoint_save_period: int = None,
        visualize: bool = VISUALIZE_DEFAULT_VALUE,
        analyze: bool = ANALYZE_DEFAULT_VALUE,
    ) -> str:
        validation(
            self._logger,
            self.AVAILABLE_CROSSOVER_METHODS,
            self.AVAILABLE_MUTATION_METHODS,
            self.AVAILABLE_PARENT_SELECTION_METHODS,
            self.AVAILABLE_REMAINING_SELECTION_METHODS,
            self.AVAILABLE_PRUNING_METHODS,
            genome_length,
            population_size,
            generation_size,
            parent_selection_method,
            remaining_selection_method,
            crossover_method,
            mutation_method,
            termination_conditions,
            crossover_probability,
            mutation_probability,
            mode,
            pruning_methods,
            iterations_number,
            statistics,
            statistic_sampling_period,
            evaluations_number,
            phenotypic_diversity_window_size,
            phenotypic_diversity_error_thereshold,
            checkpoint_save_period,
        )
        self._logger.info("Vlidation is passed successfuly")
        self.__generate_note_file(
            genome_length,
            population_size,
            generation_size,
            parent_selection_method,
            remaining_selection_method,
            crossover_method,
            mutation_method,
            termination_conditions,
            crossover_probability,
            mutation_probability,
            mode,
            pruning_methods,
            pruning_methods_params,
        )
        self._logger.info("Run algorithm from scratch")
        best_chromosome = self.__create_individual(genome_length)
        self.evaluation_func(best_chromosome)
        population = self.__create_population(genome_length, population_size)
        self.__evaluationAll(population)

        current_iteration_number = 1
        avg_fitness_list = None
        var_fitness_list = None
        best_fitness_list = None
        pruning_count_list = None  # 2d list

        if StatisticsEnum.AVG_FITNESS.value in statistics:
            avg_fitness_list = []
        if StatisticsEnum.VAR_FITNESS.value in statistics:
            var_fitness_list = []
        if StatisticsEnum.BEST_FITNESS.value in statistics:
            best_fitness_list = []
        if pruning_methods is not None:
            pruning_count_list = []

        return self.__algorithm(
            population_size,
            generation_size,
            parent_selection_method,
            remaining_selection_method,
            crossover_method,
            mutation_method,
            termination_conditions,
            crossover_probability,
            mutation_probability,
            mode,
            pruning_methods,
            pruning_methods_params,
            iterations_number,
            statistics,
            statistic_sampling_period,
            evaluations_number,
            fitness_limit_threshold,
            phenotypic_diversity_window_size,
            phenotypic_diversity_error_thereshold,
            checkpoint_save_period,
            population,
            current_iteration_number,
            best_chromosome,
            avg_fitness_list,
            var_fitness_list,
            best_fitness_list,
            pruning_count_list,
            0,
            visualize,
            analyze,
        )

    def continue_checkpoint(
        self, checkpoint_path: str, new_iterations_number: int = None, new_evaluations_number: int = None, visualize: bool = False, analyze: bool = False
    ) -> str:
        if checkpoint_path is None:
            raise InvalidValueError(self._logger, input_message="Checkpoint base directory is none")
        if not os.path.exists(checkpoint_path):
            raise FileNotExistError(self._logger, checkpoint_path)
        self._logger.info(f'Load checkpoint "{checkpoint_path}"')
        (
            population,
            current_iteration_number,
            best_chromosome,
            population_size,
            generation_size,
            parent_selection_method,
            remaining_selection_method,
            crossover_method,
            mutation_method,
            termination_conditions,
            crossover_probability,
            mutation_probability,
            mode,
            pruning_methods,
            pruning_methods_params,
            iterations_number,
            statistics,
            statistic_sampling_period,
            evaluations_number,
            fitness_limit_threshold,
            phenotypic_diversity_window_size,
            phenotypic_diversity_error_thereshold,
            checkpoint_save_period,
            avg_fitness_list,
            var_fitness_list,
            best_fitness_list,
            pruning_count_list,
            elapsed_time,
        ) = self.__load_checkpoint(checkpoint_path)
        if new_iterations_number is not None:
            iterations_number = new_iterations_number
        if new_evaluations_number is not None:
            evaluations_number = new_evaluations_number
        self.__generate_note_file(
            len(best_chromosome.genome),
            population_size,
            generation_size,
            parent_selection_method,
            remaining_selection_method,
            crossover_method,
            mutation_method,
            termination_conditions,
            crossover_probability,
            mutation_probability,
            mode,
            pruning_methods,
            pruning_methods_params,
            checkpoint_path,
        )
        return self.__algorithm(
            population_size,
            generation_size,
            parent_selection_method,
            remaining_selection_method,
            termination_conditions,
            crossover_probability,
            mutation_probability,
            mode,
            pruning_methods,
            pruning_methods_params,
            iterations_number,
            statistics,
            statistic_sampling_period,
            evaluations_number,
            fitness_limit_threshold,
            phenotypic_diversity_window_size,
            phenotypic_diversity_error_thereshold,
            checkpoint_save_period,
            population,
            current_iteration_number,
            best_chromosome,
            avg_fitness_list,
            var_fitness_list,
            best_fitness_list,
            pruning_count_list,
            elapsed_time,
            visualize,
            analyze,
        )

    def show_available_parent_selection_methods(self, return_instead_of_print=False):
        if return_instead_of_print:
            return self.AVAILABLE_PARENT_SELECTION_METHODS
        print("Available Parent Selection Methods:")
        print(self.AVAILABLE_PARENT_SELECTION_METHODS)

    def show_available_remaining_selection_methods(self, return_instead_of_print=False):
        if return_instead_of_print:
            return self.AVAILABLE_REMAINING_SELECTION_METHODS
        print("Available Remaining Selection Methods:")
        print(self.AVAILABLE_REMAINING_SELECTION_METHODS)

    def show_available_termination_conditions(self, return_instead_of_print=False):
        if return_instead_of_print:
            return AVAILABLE_TERMINATION_CONDITIONS
        print("Available Termination Conditions:")
        print(AVAILABLE_TERMINATION_CONDITIONS)

    def show_available_statistics(self, return_instead_of_print=False):
        if return_instead_of_print:
            return AVAILABLE_STATISTICS
        print("Available Plot Types:")
        print(AVAILABLE_STATISTICS)

    def show_available_mode(self, return_instead_of_print=False):
        if return_instead_of_print:
            return AVAILABLE_MODES
        print("Available Modes:")
        print(AVAILABLE_MODES)

    def show_available_crossover_methods(self, return_instead_of_print=False):
        if return_instead_of_print:
            return self.AVAILABLE_CROSSOVER_METHODS
        print("Available Crossover types:")
        print(self.AVAILABLE_CROSSOVER_METHODS)

    def show_available_mutation_methods(self, return_instead_of_print=False):
        if return_instead_of_print:
            return self.AVAILABLE_MUTATION_METHODS
        print("Available Mutation types:")
        print(self.AVAILABLE_MUTATION_METHODS)

    def show_all_available_functions_and_values_of_project(self):
        print("Available Termination Conditions:")
        print(AVAILABLE_TERMINATION_CONDITIONS)
        print()

        print("Available Plot Types:")
        print(AVAILABLE_STATISTICS)
        print()

        print("Available Modes:")
        print(AVAILABLE_MODES)
        print()

        print("Available Thereshold Scheduler Methods:")
        print(self.AVAILABLE_SCHEDULER_METHODS)
        print()

        print("Available Parent Selection Methods:")
        print(self.AVAILABLE_PARENT_SELECTION_METHODS)
        print()

        print("Available Remaining Selection Methods:")
        print(self.AVAILABLE_REMAINING_SELECTION_METHODS)
        print()

        print("Available Mutation types:")
        print(self.AVAILABLE_MUTATION_METHODS)
        print()

        print("Available Crossover types:")
        print(self.AVAILABLE_CROSSOVER_METHODS)


del _Base, _AutomationSystem

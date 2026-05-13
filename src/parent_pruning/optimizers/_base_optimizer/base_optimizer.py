import os
import time
import json
import copy
import pickle
import random
import parent_pruning.pruning.pruning_methods as pruning_methods_module
import parent_pruning.selection_methods.parent_selection as parent_selection_module
import parent_pruning.selection_methods.remaining_selection as remaining_selection_module
import parent_pruning.thereshold_scheduler.thereshold_scheduler_methods as thereshold_scheduler_module

from .__validator import validation
from parent_pruning._base import Base
from parent_pruning.visualization import Visualizer
from .._utils import init_function_by_name, replace_with_enum
from parent_pruning._automation_system import AutomationSystem
from parent_pruning.individuals.base_individual import Individual
from parent_pruning._enums import ModesEnum, StatisticsEnum, TerminationConditionsEnum
from parent_pruning.termination_condition import TerminationCondition
from .__utils import (
    compute_avg_fitness,
    compute_var_fitness_with_avg,
    copy_parent_to_child,
    increase_age_of_all_population,
)
from parent_pruning.configs.base_optimizer_config import (
    CROSSOVER_PROBABILITY_DEFAULT_VALUE,
    MODE_DEFAULT_VALUE,
    MUTATION_PROBABILITY_DEFAULT_VALUE,
    VISUALIZE_DEFAULT_VALUE,
    TERMINATION_CONDITIONS_DEFAULT_VALUE,
    AVAILABLE_MODES,
    AVAILABLE_TERMINATION_CONDITIONS,
    AVAILABLE_STATISTICS,
)
from parent_pruning.configs.directories import (
    EXTENSION_DIRECTORY_PARENT_SELECTION_METHODS_MODULE,
    EXTENSION_DIRECTORY_PRUNING_METHODS_MODULE,
    EXTENSION_DIRECTORY_REMAINING_SELECTION_METHODS_MODULE,
    EXTENSION_DIRECTORY_SCHEDULER_METHODS_MODULE,
)


class BaseOptimizer(Base, AutomationSystem):
    
 
        
                
    def __parent_selection_fucn_determiner(self, parent_selection_type):
        func_name = parent_selection_type
        if parent_selection_type.startswith("q_tournoment"):
            self.ps_q = int(parent_selection_type.partition("#")[2])
            func_name = "q_tournoment"
        module_path = None
        if self.extension_directory is not None:
            module_path = os.path.join(self.extension_directory, EXTENSION_DIRECTORY_PARENT_SELECTION_METHODS_MODULE)
        self.parent_selection_func = init_function_by_name(
            parent_selection_module,
            module_path,
            func_name,
            "parent selection",
            self._logger,
        )

    def __remaining_selection_func_determiner(self, remaining_selection_type):
        func_name = remaining_selection_type
        if remaining_selection_type.startswith("q_tournoment"):
            self.ps_q = int(remaining_selection_type.partition("#")[2])
            func_name = "q_tournoment"
        module_path = None
        if self.extension_directory is not None:
            module_path = os.path.join(self.extension_directory, EXTENSION_DIRECTORY_REMAINING_SELECTION_METHODS_MODULE)
        self.remaining_selection_func = init_function_by_name(
            remaining_selection_module,
            module_path,
            func_name,
            "remaining selection",
            self._logger,
        )

    def __pruning_methods_funcs_determiner(self, pruning_methods):
        self.pruning_methods_functions_list = []
        if pruning_methods is not None:
            module_path = None
            if self.extension_directory is not None:
                module_path = os.path.join(self.extension_directory, EXTENSION_DIRECTORY_PRUNING_METHODS_MODULE)
            for method_name in pruning_methods:
                self.pruning_methods_functions_list.append(
                    init_function_by_name(
                        pruning_methods_module,
                        module_path,
                        method_name,
                        f"pruning method {method_name}",
                        self._logger,
                    )
                )

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

    def __save_checkpoint(
        self,
        chromosome_list,
        current_iteration_number,
        bset_chromosome,
        termination_conditions,
        phenotypic_diversity_window_size,
        phenotypic_diversity_error_thereshold,
        # genotypic_diversity_window_size,
        # genotypic_diversity_error_thereshold,
        fitness_limit_threshold,
        iterations_number,
        evaluation_number,
        elapsed_time,
    ):
        with open(os.path.join(self.checkpoint_directory, "checkpoint.pkl"), "wb") as file_to_write:
            pickle.dump(chromosome_list, file_to_write)

            pickle.dump(current_iteration_number, file_to_write)
            pickle.dump(bset_chromosome, file_to_write)

            pickle.dump(self.project_name, file_to_write)
            pickle.dump(self.base_directory, file_to_write)

            pickle.dump(self.genome_size, file_to_write)
            pickle.dump(self.population_size, file_to_write)
            pickle.dump(self.generation_size, file_to_write)
            pickle.dump(self.parent_selection_method, file_to_write)
            pickle.dump(self.remaining_selection_method, file_to_write)
            pickle.dump(self.crossover_method, file_to_write)
            pickle.dump(self.mutation_method, file_to_write)
            pickle.dump(self.crossover_probability, file_to_write)
            pickle.dump(self.mutation_probability, file_to_write)
            pickle.dump(termination_conditions, file_to_write)
            pickle.dump(self.statistics, file_to_write)
            pickle.dump(self.mode, file_to_write)
            pickle.dump(self.pruning_methods, file_to_write)
            filtered_pruning_methods_param= None
            if self.pruning_methods is not None:
                filtered_pruning_methods_param = [{k: v for k, v in d.items() if k != "scheduler_method"} for d in self.pruning_methods_params]
            pickle.dump(filtered_pruning_methods_param, file_to_write)
            pickle.dump(self.pruning_count_list, file_to_write)

            pickle.dump(phenotypic_diversity_window_size, file_to_write)
            pickle.dump(phenotypic_diversity_error_thereshold, file_to_write)
            # pickle.dump(genotypic_diversity_window_size, file_to_write)
            # pickle.dump(genotypic_diversity_error_thereshold, file_to_write)
            pickle.dump(fitness_limit_threshold, file_to_write)
            pickle.dump(iterations_number, file_to_write)
            pickle.dump(evaluation_number, file_to_write)
            pickle.dump(self.statistic_sampling_period, file_to_write)
            pickle.dump(self.checkpoint_save_period, file_to_write)
            pickle.dump(self.visualize, file_to_write)

            pickle.dump(self.avg_fitness_list, file_to_write)
            pickle.dump(self.var_fitness_list, file_to_write)
            pickle.dump(self.best_fitness_list, file_to_write)
            pickle.dump(self.extension_directory, file_to_write)

            pickle.dump(elapsed_time, file_to_write)

    def __load_checkpoint(self, checkpoint_base_directory):
        with open(os.path.join(checkpoint_base_directory, "checkpoints", "checkpoint.pkl"), "rb") as file_to_read:
            self.__temp_chromosome_list = pickle.load(file_to_read)

            self.__temp_current_iteration_number = pickle.load(file_to_read)
            self.__temp_best_chromosome = pickle.load(file_to_read)

            self.project_name = pickle.load(file_to_read)
            self.base_directory = pickle.load(file_to_read)

            self.genome_size = pickle.load(file_to_read)
            self.population_size = pickle.load(file_to_read)
            self.generation_size = pickle.load(file_to_read)
            self.parent_selection_method = pickle.load(file_to_read)
            self.remaining_selection_method = pickle.load(file_to_read)
            self.crossover_method = pickle.load(file_to_read)
            self.mutation_method = pickle.load(file_to_read)
            self.crossover_probability = pickle.load(file_to_read)
            self.mutation_probability = pickle.load(file_to_read)
            termination_conditions = pickle.load(file_to_read)
            self.statistics = pickle.load(file_to_read)
            self.mode = pickle.load(file_to_read)
            self.pruning_methods = pickle.load(file_to_read)
            self.__pruning_methods_funcs_determiner(self.pruning_methods)
            self.pruning_methods_params = pickle.load(file_to_read)
            if self.pruning_methods_params is not None:
                for pruning_param in self.pruning_methods_params:
                    if "scheduler_method" in pruning_param:
                        pruning_param["scheduler_func"] = self.__thereshold_scheduler_func_determiner(pruning_param["scheduler_method"])
            self.pruning_count_list = pickle.load(file_to_read)
            self.__parent_selection_fucn_determiner(self.parent_selection_method)
            self.__remaining_selection_func_determiner(self.remaining_selection_method)
            phenotypic_diversity_window_size = pickle.load(file_to_read)
            phenotypic_diversity_error_thereshold = pickle.load(file_to_read)
            # genotypic_diversity_window_size = pickle.load(file_to_read)
            # genotypic_diversity_error_thereshold = pickle.load(file_to_read)
            fitness_limit_threshold = pickle.load(file_to_read)
            iterations_number = pickle.load(file_to_read)
            evaluation_number = pickle.load(file_to_read)
            self.termination_condition_handler = TerminationCondition(
                termination_conditions,
                phenotypic_diversity_window_size,
                phenotypic_diversity_error_thereshold,
                # genotypic_diversity_window_size,
                # genotypic_diversity_error_thereshold,
                fitness_limit_threshold,
                iterations_number,
                evaluation_number,
            )
            self.statistic_sampling_period = pickle.load(file_to_read)
            self.checkpoint_save_period = pickle.load(file_to_read)
            self.visualize = pickle.load(file_to_read)
            validation(
                self._logger,
                self.AVAILABLE_PARENT_SELECTION_METHODS,
                self.AVAILABLE_REMAINING_SELECTION_METHODS,
                self.AVAILABLE_PRUNING_METHODS,
                #########################
                self.project_name,
                self.genome_size,
                self.population_size,
                self.generation_size,
                self.parent_selection_method,
                self.remaining_selection_method,
                termination_conditions,
                self.crossover_probability,
                self.mutation_probability,
                self.mode,
                self.pruning_methods,
                iterations_number,
                self.statistics,
                self.statistic_sampling_period,
                evaluation_number,
                phenotypic_diversity_window_size,
                phenotypic_diversity_error_thereshold,
                self.checkpoint_save_period,
            )

            # for visualizer
            self.visualizer = Visualizer(self.statistics, self.statistic_sampling_period, self.result_directory)

            self.avg_fitness_list = pickle.load(file_to_read)
            self.var_fitness_list = pickle.load(file_to_read)
            self.best_fitness_list = pickle.load(file_to_read)
            self.extension_directory = pickle.load(file_to_read)

            self.elapsed_time = pickle.load(file_to_read)

    def __init__(
        self,
        project_name,
        input_data,
        genome_size,
        population_size,
        generation_size,
        parent_selection_method,
        remaining_selection_method,
        crossover_method,
        mutation_method,
        termination_conditions=TERMINATION_CONDITIONS_DEFAULT_VALUE,
        crossover_probability=CROSSOVER_PROBABILITY_DEFAULT_VALUE,
        mutation_probability=MUTATION_PROBABILITY_DEFAULT_VALUE,
        mode=MODE_DEFAULT_VALUE,
        pruning_methods=None,
        pruning_methods_params=None,
        iterations_number=None,
        statistics=None,
        statistic_sampling_period=None,
        evaluation_number=None,
        fitness_limit_threshold=None,
        phenotypic_diversity_window_size=None,
        phenotypic_diversity_error_thereshold=None,
        # genotypic_diversity_window_size=None,
        # genotypic_diversity_error_thereshold=None,
        visualize=VISUALIZE_DEFAULT_VALUE,
        checkpoint_save_period=None,
        checkpoint_base_directory=None,
        #####
        extension_directory=None,
        #####
        debug_mode=False,
        # TODO:
        # source_spots_in_genome=None,
        # destination_spots_in_genome=None,
    ):
        Base.__init__(self, project_name, checkpoint_base_directory, debug_mode)
        AutomationSystem.__init__(self, extension_directory)
        self.input_data = input_data
        self.individual_class = None

        self._logger.info(f"List of available `Parent Selection Methods` functions:{self.AVAILABLE_PARENT_SELECTION_METHODS}")
        self._logger.info(f"List of available `Remaining Selection Methods` functions:{self.AVAILABLE_REMAINING_SELECTION_METHODS}")
        self._logger.info(f"List of available `Pruning Methods` functions: {self.AVAILABLE_PRUNING_METHODS}")

        self.checkpoint_base_directory = checkpoint_base_directory
        if checkpoint_base_directory is not None:
            self._logger.info(f'Load checkpoint "{self.checkpoint_base_directory}"')
            self.__load_checkpoint(checkpoint_base_directory)
        else:
            validation(
                self._logger,
                self.AVAILABLE_PARENT_SELECTION_METHODS,
                self.AVAILABLE_REMAINING_SELECTION_METHODS,
                self.AVAILABLE_PRUNING_METHODS,
                #########################
                project_name,
                genome_size,
                population_size,
                generation_size,
                parent_selection_method,
                remaining_selection_method,
                termination_conditions,
                crossover_probability,
                mutation_probability,
                mode,
                pruning_methods,
                iterations_number,
                statistics,
                statistic_sampling_period,
                evaluation_number,
                phenotypic_diversity_window_size,
                phenotypic_diversity_error_thereshold,
                checkpoint_save_period,
            )
            self._logger.info("Vlidation is passed successfuly")
            self._logger.info("Initialize optimzier")
            self.elapsed_time = 0
            self.genome_size = genome_size
            self.population_size = population_size
            self.generation_size = generation_size
            self.parent_selection_method = parent_selection_method
            self.remaining_selection_method = remaining_selection_method
            self.crossover_method = crossover_method
            self.mutation_method = mutation_method
            self.crossover_probability = crossover_probability
            self.mutation_probability = mutation_probability
            self.pruning_methods = pruning_methods
            self.pruning_methods_params = pruning_methods_params
            if self.pruning_methods_params is not None:
                for pruning_param in self.pruning_methods_params:
                    if pruning_param is None:
                        pruning_param={}
                    elif "scheduler_method" in pruning_param:
                        pruning_param["scheduler_func"] = self.__thereshold_scheduler_func_determiner(pruning_param["scheduler_method"])
            self.__pruning_methods_funcs_determiner(pruning_methods)
            self.__parent_selection_fucn_determiner(parent_selection_method)
            self.__remaining_selection_func_determiner(remaining_selection_method)
            ######################### TODO
            self.termination_condition_handler = TerminationCondition(
                replace_with_enum("termination_conditions", termination_conditions),
                phenotypic_diversity_window_size,
                phenotypic_diversity_error_thereshold,
                # genotypic_diversity_window_size,
                # genotypic_diversity_error_thereshold,
                fitness_limit_threshold,
                iterations_number,
                evaluation_number,
            )
            ######################### TODO
            self.statistics = replace_with_enum("statistics", statistics)
            self.statistic_sampling_period = statistic_sampling_period
            ######################### TODO
            self.mode = replace_with_enum("modes", mode)
            self.checkpoint_save_period = checkpoint_save_period
            self.visualize = visualize
            self.visualizer = Visualizer(self.statistics, statistic_sampling_period, self.result_directory)

            self.avg_fitness_list = None
            self.var_fitness_list = None
            self.best_fitness_list = None
            self.pruning_count_list = None  # 2d list

            if StatisticsEnum.AVG_FITNESS in self.statistics:
                self.avg_fitness_list = []
            if StatisticsEnum.VAR_FITNESS in self.statistics:
                self.var_fitness_list = []
            if StatisticsEnum.BEST_FITNESS in self.statistics:
                self.best_fitness_list = []
            if self.pruning_methods is not None:
                self.pruning_count_list = []

    def __create_individual(self):
        return self.individual_class(genome_size=self.genome_size)

    def __create_population(self):
        return [self.__create_individual() for _ in range(self.population_size)]

    def __evaluationAll(self, population: list[Individual]) -> None:
        for choromosome in population:
            self.evaluation_func(choromosome)

    def __parent_selection(self, chromosome_list):
        if hasattr(self, "ps_q"):
            return self.parent_selection_func(chromosome_list, self.ps_q)
        return self.parent_selection_func(chromosome_list)

    def __remaining_selection(self, chromosome_list, remaining_size):
        if hasattr(self, "rs_q"):
            return self.remaining_selection_func(chromosome_list, self.rs_q, remaining_size)
        return self.remaining_selection_func(chromosome_list, remaining_size)

    def __select_next_generation_basedon_mode(self, population, children):
        if self.mode == ModesEnum.FORGETFUL:
            return children
        elif self.mode == ModesEnum.AGGREGGATE:
            return [j for i in [population, children] for j in i]
        else:
            raise Exception(f"mode {self.mode} is not supported!")

    def __crossover_and_mutation(self, population):
        children_list = []
        for _ in range(int(self.generation_size / 2)):
            parent1 = self.__parent_selection(population)
            parent1.increase_crossover_attendace()
            parent2 = self.__parent_selection(population)
            parent2.increase_crossover_attendace()

            child1 = None
            child2 = None
            if random.random() < self.crossover_probability:
                child1, child2 = self.crossover_func(parent1, parent2)
            else:
                child1 = copy_parent_to_child(parent1)
                child2 = copy_parent_to_child(parent2)

            if random.random() < self.mutation_probability:
                self.mutation_func(child1)
            if random.random() < self.mutation_probability:
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

            # add to list
            children_list.append(child1)
            children_list.append(child2)

        return children_list

    def __save_final_result(self, best_chromosome, current_iteration_number, final_population):
        with open(os.path.join(self.result_directory, "final_answer.json"), "w") as file_to_write:
            json.dump(best_chromosome.to_dict(), file_to_write, indent=4)

        with open(os.path.join(self.result_directory, "results.pkl"), "wb") as file_to_write:
            pickle.dump([self.avg_fitness_list, self.var_fitness_list, self.best_fitness_list, self.pruning_count_list], file_to_write)
            pickle.dump(self.statistics, file_to_write)
            pickle.dump(self.statistic_sampling_period, file_to_write)
            pickle.dump(self.pruning_methods, file_to_write)
            pickle.dump(self.pruning_methods_params, file_to_write)
            pickle.dump(current_iteration_number, file_to_write)

        with open(os.path.join(self.result_directory, "final_population.pkl"), "wb") as file_to_write:
            pickle.dump(final_population, file_to_write)

    def run(self):
        population = None
        current_iteration_number = None
        best_chromosome = None
        if self.checkpoint_base_directory is not None:
            population, current_iteration_number, best_chromosome = (
                self.__temp_chromosome_list,
                self.__temp_current_iteration_number,
                self.__temp_best_chromosome,
            )
        else:
            best_chromosome = self.individual_class(
                genome_size=self.genome_size,
                init_with_random_genome=True,
            )
            self.evaluation_func(best_chromosome)
            population = self.__create_population()
            self.__evaluationAll(population)

            current_iteration_number = 1

        start_time = time.time()
        while True:
            children = self.__crossover_and_mutation(population)

            next_generation_candidates = self.__select_next_generation_basedon_mode(population, children)

            best_chromosome_in_current_iteration = max(next_generation_candidates, key=lambda x: x.fitness)

            if best_chromosome.fitness < best_chromosome_in_current_iteration.fitness:
                best_chromosome = copy.deepcopy(best_chromosome_in_current_iteration)

            population = self.__remaining_selection(next_generation_candidates, self.population_size)

            increase_age_of_all_population(population)

            pruning_count_list_current_iteration = []
            if self.pruning_methods is not None:
                for index, pruning_method_function in enumerate(self.pruning_methods_functions_list):
                    if self.pruning_methods_params is None or self.pruning_methods_params[index] is None:
                        pruning_count_list_current_iteration.append(
                            pruning_method_function(population, current_iteration_number)
                        )
                    else:
                        pruning_count_list_current_iteration.append(
                            pruning_method_function(population, current_iteration_number, **self.pruning_methods_params[index])
                        )
                    
            avg_fitness = None
            if TerminationConditionsEnum.PHENOTYPIC_DIVERSITY in self.termination_condition_handler.termination_conditions:
                avg_fitness = compute_avg_fitness(population)

            if current_iteration_number % self.statistic_sampling_period == 0:
                if self.avg_fitness_list is not None:
                    if avg_fitness is not None:
                        self.avg_fitness_list.append(avg_fitness)
                    else:
                        self.avg_fitness_list.append(compute_avg_fitness(population))
                if self.var_fitness_list is not None:
                    if avg_fitness is not None:
                        self.var_fitness_list.append(compute_var_fitness_with_avg(population, avg_fitness))
                    elif self.avg_fitness_list is not None:
                        self.var_fitness_list.append(compute_var_fitness_with_avg(population, self.avg_fitness_list[-1]))
                    else:
                        self.var_fitness_list.append(compute_var_fitness_with_avg(population, compute_avg_fitness(population)))
                if self.best_fitness_list is not None:
                    self.best_fitness_list.append(best_chromosome_in_current_iteration.fitness)
                if self.pruning_methods is not None:
                    self.pruning_count_list.append(pruning_count_list_current_iteration)

            terminate, message = self.termination_condition_handler.check_termination(
                population=population,
                avg_fitness=avg_fitness,
                best_fitness=best_chromosome_in_current_iteration.fitness,
                iteration_number=current_iteration_number,
                population_size=self.population_size,
                generation_size=self.generation_size,
            )

            if terminate:
                self._logger.info(message)
                break

            current_iteration_number += 1

            if self.checkpoint_save_period is not None:
                if current_iteration_number % self.checkpoint_save_period == 0:
                    end_time = time.time()
                    self._logger.info(f"Save checkpoint at iteration {current_iteration_number}")
                    self.__save_checkpoint(
                        population,
                        current_iteration_number,
                        best_chromosome,
                        self.termination_condition_handler.termination_conditions,
                        self.termination_condition_handler.phenotypic_diversity_window_size,
                        self.termination_condition_handler.phenotypic_diversity_error_thereshold,
                        # self.termination_condition_handler.genotypic_diversity_window_size,
                        # self.termination_condition_handler.genotypic_diversity_error_thereshold,
                        self.termination_condition_handler.fitness_limit_threshold,
                        self.termination_condition_handler.iterations_number_threshold,
                        self.termination_condition_handler.evaluation_number_threshold,
                        end_time - start_time,
                    )

        end_time = time.time()
        self._logger.info(f"Best Answer Fitness: {best_chromosome.fitness}")
        self._logger.info(f"Runtime: {end_time - start_time + self.elapsed_time} seconds")
        self.__save_final_result(best_chromosome, current_iteration_number, population)
        self._logger.info("Results have been saved")
        if self.visualize:
            self.visualizer.plot_diagrams(
                current_iteration_number,
                self.avg_fitness_list,
                self.var_fitness_list,
                self.best_fitness_list,
                self.pruning_count_list,
                self.pruning_methods,
            )
            self._logger.info("Diagrams plotted successfuly")
        return self.base_directory

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

    def show_all_available_functions_and_values_of_project(self):
        print("Available Parent Selection Methods:")
        print(self.AVAILABLE_PARENT_SELECTION_METHODS)
        print()

        print("Available Remaining Selection Methods:")
        print(self.AVAILABLE_REMAINING_SELECTION_METHODS)
        print()

        print("Available Termination Conditions:")
        print(AVAILABLE_TERMINATION_CONDITIONS)
        print()

        print("Available Plot Types:")
        print(AVAILABLE_STATISTICS)
        print()

        print("Available Modes:")
        print(AVAILABLE_MODES)
        print()

import os
import time
import json
import copy
import pickle
import random
import parent_pruning.selection_algorithms.parent_selection as parent_selection_module
import parent_pruning.selection_algorithms.remaining_selection as remaining_selection_module
import parent_pruning.thereshold_scheduler.thereshold_scheduler as thereshold_scheduler_module

from parent_pruning.base.base import Base
from parent_pruning.visualization.visualizer import Visualizer
from parent_pruning.optimizers.utils import init_function_by_name
from parent_pruning.individuals.base_individual import Individual
from parent_pruning.termination_condition_algorithms.termination_condition import TerminationCondition
from parent_pruning.configs.common import (
    STATISTIC_AVG_FITNESS,
    STATISTIC_VAR_FITNESS,
    STATISTIC_BEST_FITNESS,
    STATISTIC_PRUNE_BAD_PARENT_COUNT,
    STATISTIC_PRUNE_OLD_CHROMOSOME_COUNT,
    TERMINATION_CONDITION_PHENOTYPIC_DIVERSITY,
)
from parent_pruning.configs.base_optimizer_config import (
    AVAILABLE_MODES,
    AVAILABLE_TERMINATION_CONDITIONS,
    AVAILABLE_STATISTICS,
    CROSSOVER_PROBABILITY_DEFAULT_VALUE,
    MODE_DEFAULT_VALUE,
    MUTATION_PROBABILITY_DEFAULT_VALUE,
    AVAILABLE_BAD_PARENT_SCORE_THERESHOLD_SCHEDULER_TYPE,
    AVAILABLE_PARENT_SELECTION_ALGORITHMS,
    AVAILABLE_REMAINING_SELECTION_ALGORITHMS,
    VISUALIZE_DEFAULT_VALUE,
    TERMINATION_CONDITIONS_DEFAULT_VALUE,
)


class BaseOptimizer(Base):
    def __validation(self, parent_selection_type, remaining_selection_type, termination_conditions, statistics, mode, bad_parent_score_thereshold_scheduler_type, bad_parent_score_thereshold_scheduler_start_number, bad_parent_score_thereshold_scheduler_end_number, age_thereshold):
        if parent_selection_type.split('#')[0] not in AVAILABLE_PARENT_SELECTION_ALGORITHMS:
            raise Exception('')
        if remaining_selection_type.split('#')[0] not in AVAILABLE_REMAINING_SELECTION_ALGORITHMS:
            raise Exception('')
        if mode not in AVAILABLE_MODES:
            raise Exception('')
        for termination_condition in termination_conditions:
            if termination_condition not in AVAILABLE_TERMINATION_CONDITIONS:
                raise Exception('')
        if statistics is not None:
            for statistic in statistics:
                if statistic not in AVAILABLE_STATISTICS:
                    raise Exception('')
        if bad_parent_score_thereshold_scheduler_type is not None and bad_parent_score_thereshold_scheduler_type not in AVAILABLE_BAD_PARENT_SCORE_THERESHOLD_SCHEDULER_TYPE:
            raise Exception('')
        
        if bad_parent_score_thereshold_scheduler_type is not None and bad_parent_score_thereshold_scheduler_start_number is None or bad_parent_score_thereshold_scheduler_end_number is None:
            raise Exception('')
        
        if STATISTIC_PRUNE_BAD_PARENT_COUNT in statistics and bad_parent_score_thereshold_scheduler_type is None:
            raise Exception('')
        if STATISTIC_PRUNE_OLD_CHROMOSOME_COUNT in statistics and age_thereshold is None:
            raise Exception('')
        
    def __log_project_information(self, project_name, population_size, generation_size):
        pass

    def __parent_selection_fucn_determiner(self, parent_selection_type):
        func_name = parent_selection_type
        if parent_selection_type.startswith("q_tournoment"):
            self.ps_q = int(parent_selection_type.partition("#")[2])
            func_name = "q_tournoment"
        self.parent_selection_func = init_function_by_name(
            parent_selection_module, func_name, "parent selection selection"
        )

    def __remaining_selection_func_determiner(self, remaining_selection_type):
        func_name = remaining_selection_type
        if remaining_selection_type.startswith("q_tournoment"):
            self.ps_q = int(remaining_selection_type.partition("#")[2])
            func_name = "q_tournoment"
        self.remaining_selection_func = init_function_by_name(
            remaining_selection_module, func_name, "remaining selection"
        )

    def __bad_parent_score_thereshold_scheduler_func_determiner(self, bad_parent_score_thereshold_scheduler_type):
        self.bad_parent_score_thereshold_scheduler_type_func = init_function_by_name(
            thereshold_scheduler_module,
            bad_parent_score_thereshold_scheduler_type,
            "bad parent score thereshold scheduler ",
        )
    
    def __save_checkpoint(self,
            chromosome_list,
            current_iteration_number,
            bset_chromosome,
            termination_conditions,
            phenotypic_diversity_window_size,
            phenotypic_diversity_error_thereshold,
            genotypic_diversity_window_size,
            genotypic_diversity_error_thereshold,
            fitness_limit_threshold,
            iterations_number,
            evaluation_number,
            elapsed_time,
        ):
        with open(os.path.join(self.checkpoint_directory, 'checkpoint.pkl'), 'wb') as file_to_write:
            pickle.dump(chromosome_list, file_to_write)
            
            pickle.dump(current_iteration_number, file_to_write)
            pickle.dump(bset_chromosome, file_to_write)
            
            pickle.dump(self.project_name, file_to_write)
            pickle.dump(self.base_directory, file_to_write)
            
            pickle.dump(self.genome_size, file_to_write)
            pickle.dump(self.population_size, file_to_write)
            pickle.dump(self.generation_size, file_to_write)
            pickle.dump(self.parent_selection_type, file_to_write)
            pickle.dump(self.remaining_selection_type, file_to_write)
            pickle.dump(self.crossover_type, file_to_write)
            pickle.dump(self.mutation_type, file_to_write)
            pickle.dump(self.crossover_probability, file_to_write)
            pickle.dump(self.mutation_probability, file_to_write)
            pickle.dump(self.age_thereshold, file_to_write)
            pickle.dump(self.bad_parent_score_thereshold_scheduler_type, file_to_write)
            pickle.dump(self.bad_parent_score_thereshold_scheduler_start_number, file_to_write)
            pickle.dump(self.bad_parent_score_thereshold_scheduler_end_number, file_to_write)
            pickle.dump(termination_conditions, file_to_write)
            pickle.dump(self.statistics, file_to_write)
            pickle.dump(self.mode, file_to_write)

            pickle.dump(phenotypic_diversity_window_size, file_to_write)
            pickle.dump(phenotypic_diversity_error_thereshold, file_to_write)
            pickle.dump(genotypic_diversity_window_size, file_to_write)
            pickle.dump(genotypic_diversity_error_thereshold, file_to_write)
            pickle.dump(fitness_limit_threshold, file_to_write)
            pickle.dump(iterations_number, file_to_write)
            pickle.dump(evaluation_number, file_to_write)
            pickle.dump(self.statistic_sampling_period, file_to_write)
            pickle.dump(self.checkpoint_save_period, file_to_write)
            pickle.dump(self.visualize, file_to_write)
            
            pickle.dump(self.avg_fitness_list, file_to_write)
            pickle.dump(self.var_fitness_list, file_to_write)
            pickle.dump(self.best_fitness_list, file_to_write)
            pickle.dump(self.prune_bad_parent_count_list, file_to_write)
            pickle.dump(self.prune_old_chromosome_count_list, file_to_write)
            
            pickle.dump(elapsed_time, file_to_write)
        
    def __load_checkpoint(self, checkpoint_base_directory):
        with open(os.path.join(checkpoint_base_directory, 'checkpoints', 'checkpoint.pkl'), 'rb') as file_to_read:
            self.__temp_chromosome_list= pickle.load(file_to_read)
            
            self.__temp_current_iteration_number= pickle.load(file_to_read)
            self.__temp_best_chromosome= pickle.load(file_to_read)
            
            self.project_name= pickle.load(file_to_read)
            self.base_directory= pickle.load(file_to_read)
            
            self.genome_size= pickle.load(file_to_read)
            self.population_size= pickle.load(file_to_read)
            self.generation_size= pickle.load(file_to_read)
            self.parent_selection_type= pickle.load(file_to_read)
            self.remaining_selection_type= pickle.load(file_to_read)
            self.crossover_type= pickle.load(file_to_read)
            self.mutation_type= pickle.load(file_to_read)
            self.crossover_probability= pickle.load(file_to_read)
            self.mutation_probability= pickle.load(file_to_read)
            self.age_thereshold= pickle.load(file_to_read)
            self.bad_parent_score_thereshold_scheduler_type= pickle.load(file_to_read)
            self.bad_parent_score_thereshold_scheduler_start_number= pickle.load(file_to_read)
            self.bad_parent_score_thereshold_scheduler_end_number= pickle.load(file_to_read)
            termination_conditions= pickle.load(file_to_read)
            self.statistics= pickle.load(file_to_read)
            self.mode= pickle.load(file_to_read)
            self.__validation(
                self.parent_selection_type,
                self.remaining_selection_type,
                termination_conditions,
                self.statistics,
                self.mode,
                self.bad_parent_score_thereshold_scheduler_type,
                self.bad_parent_score_thereshold_scheduler_start_number,
                self.bad_parent_score_thereshold_scheduler_end_number,
                self.age_thereshold
            )
            self.__parent_selection_fucn_determiner(self.parent_selection_type)
            self.__remaining_selection_func_determiner(self.remaining_selection_type)
            if self.bad_parent_score_thereshold_scheduler_type is not None:
                self.__bad_parent_score_thereshold_scheduler_func_determiner(self.bad_parent_score_thereshold_scheduler_type)
            phenotypic_diversity_window_size= pickle.load(file_to_read)
            phenotypic_diversity_error_thereshold= pickle.load(file_to_read)
            genotypic_diversity_window_size= pickle.load(file_to_read)
            genotypic_diversity_error_thereshold= pickle.load(file_to_read)
            fitness_limit_threshold= pickle.load(file_to_read)
            iterations_number= pickle.load(file_to_read)
            evaluation_number= pickle.load(file_to_read)
            self.termination_condition_handler= TerminationCondition(
                termination_conditions,
                phenotypic_diversity_window_size,
                phenotypic_diversity_error_thereshold,
                genotypic_diversity_window_size,
                genotypic_diversity_error_thereshold,
                fitness_limit_threshold,
                iterations_number,
                evaluation_number,
            )
            self.statistic_sampling_period= pickle.load(file_to_read)
            self.checkpoint_save_period= pickle.load(file_to_read)
            self.visualize= pickle.load(file_to_read)
            
            # for visualizer
            self.visualizer= Visualizer(self.statistics, self.statistic_sampling_period, self.result_directory)
            
            self.avg_fitness_list= pickle.load(file_to_read)
            self.var_fitness_list= pickle.load(file_to_read)
            self.best_fitness_list= pickle.load(file_to_read)
            self.prune_bad_parent_count_list= pickle.load(file_to_read)
            self.prune_old_chromosome_count_list= pickle.load(file_to_read)
            
            self.elapsed_time= pickle.load(file_to_read)
        
    def __init__(
        self,
        project_name,
        input_data,
        genome_size,
        population_size,
        generation_size,
        parent_selection_type,
        remaining_selection_type,
        crossover_type,
        mutation_type,
        termination_conditions=TERMINATION_CONDITIONS_DEFAULT_VALUE,
        crossover_probability=CROSSOVER_PROBABILITY_DEFAULT_VALUE,
        mutation_probability=MUTATION_PROBABILITY_DEFAULT_VALUE,
        mode=MODE_DEFAULT_VALUE,
        iterations_number=None,
        statistics=None,
        statistic_sampling_period=None,
        evaluation_number=None,
        fitness_limit_threshold=None,
        age_thereshold=None,
        bad_parent_score_thereshold_scheduler_type=None,
        bad_parent_score_thereshold_scheduler_start_number=None,
        bad_parent_score_thereshold_scheduler_end_number=None,
        phenotypic_diversity_window_size=None,
        phenotypic_diversity_error_thereshold=None,
        genotypic_diversity_window_size=None,
        genotypic_diversity_error_thereshold=None,
        visualize= VISUALIZE_DEFAULT_VALUE,
        checkpoint_save_period=None,
        checkpoint_base_directory=None,
        # TODO:
        # source_spots_in_genome=None,
        # destination_spots_in_genome=None,
    ) -> None:
        super().__init__(project_name, checkpoint_base_directory)
        self.input_data = input_data
        self.individual_class= None
        
        self._logger.info(f'List of available `Bad Parent Score Thereshold Scheduler Type` functions:{AVAILABLE_BAD_PARENT_SCORE_THERESHOLD_SCHEDULER_TYPE}')
        self._logger.info(f'List of available `Parent Selection Algorithm` functions:{AVAILABLE_PARENT_SELECTION_ALGORITHMS}')
        self._logger.info(f'List of available `Remaining Selection Algorithm` functions:{AVAILABLE_REMAINING_SELECTION_ALGORITHMS}')
        
        self.checkpoint_base_directory= checkpoint_base_directory
        if checkpoint_base_directory is not None:
            self._logger.info(f'Load checkpoint \"{self.checkpoint_base_directory}\"')
            self.__load_checkpoint(checkpoint_base_directory)
        else:
            self.__validation(parent_selection_type, remaining_selection_type, termination_conditions, statistics, mode, bad_parent_score_thereshold_scheduler_type, bad_parent_score_thereshold_scheduler_start_number, bad_parent_score_thereshold_scheduler_end_number, age_thereshold)
            self._logger.info('Initialize optimzier')
            self.elapsed_time= 0
            self.genome_size = genome_size
            self.population_size = population_size
            self.generation_size = generation_size
            self.parent_selection_type= parent_selection_type
            self.remaining_selection_type= remaining_selection_type
            self.crossover_type= crossover_type
            self.mutation_type= mutation_type
            self.crossover_probability = crossover_probability
            self.mutation_probability = mutation_probability
            self.age_thereshold= age_thereshold
            self.bad_parent_score_thereshold_scheduler_type= bad_parent_score_thereshold_scheduler_type
            self.bad_parent_score_thereshold_scheduler_start_number = bad_parent_score_thereshold_scheduler_start_number
            self.bad_parent_score_thereshold_scheduler_end_number = bad_parent_score_thereshold_scheduler_end_number
            self.__parent_selection_fucn_determiner(parent_selection_type)
            self.__remaining_selection_func_determiner(remaining_selection_type)
            if bad_parent_score_thereshold_scheduler_type is not None:
                self.__bad_parent_score_thereshold_scheduler_func_determiner(self.bad_parent_score_thereshold_scheduler_type)
            self.termination_condition_handler = TerminationCondition(
                termination_conditions,
                phenotypic_diversity_window_size,
                phenotypic_diversity_error_thereshold,
                genotypic_diversity_window_size,
                genotypic_diversity_error_thereshold,
                fitness_limit_threshold,
                iterations_number,
                evaluation_number,
            )
            self.statistics = statistics
            self.statistic_sampling_period = statistic_sampling_period
            self.mode = mode
            self.checkpoint_save_period= checkpoint_save_period
            self.visualize= visualize
            
            self.visualizer= Visualizer(statistics, statistic_sampling_period, self.result_directory)
            
            self.avg_fitness_list=None
            self.var_fitness_list=None
            self.best_fitness_list=None
            self.prune_bad_parent_count_list=None
            self.prune_old_chromosome_count_list=None
            
            if STATISTIC_AVG_FITNESS in statistics:
                self.avg_fitness_list= []
            if STATISTIC_VAR_FITNESS in statistics:
                self.var_fitness_list= []
            if STATISTIC_BEST_FITNESS in statistics:
                self.best_fitness_list= []
            if STATISTIC_PRUNE_BAD_PARENT_COUNT in statistics:
                self.prune_bad_parent_count_list= []
            if STATISTIC_PRUNE_OLD_CHROMOSOME_COUNT in statistics:
                self.prune_old_chromosome_count_list= []
    
    def __compute_avg_fitness(self, individual_list):
        sum_fitness = 0
        for chromosome in individual_list:
            sum_fitness += chromosome.fitness
        return sum_fitness / len(individual_list)

    def __compute_var_fitness_with_avg(self, individual_list, avg_fitness):
        sum_var = 0
        for chromosome in individual_list:
            sum_var += pow((chromosome.fitness - avg_fitness), 2)

        return sum_var / (len(individual_list) - 1)

    def __create_individual(self):
        return self.individual_class(genome_size=self.genome_size)

    def __create_population(self):
        return [self.__create_individual() for _ in range(self.population_size)]

    def __evaluationAll(self, population: list[Individual]) -> None:
        for choromosome in population:
            self.evaluation_func(choromosome)
                    
    def __prune_bad_parent(self, choromosome_list: list[Individual], iteration_num, do_replace=False) -> int:
        bad_parent_score_thereshold = self.bad_parent_score_thereshold_scheduler_type_func(
            iteration_num,
            self.bad_parent_score_thereshold_scheduler_start_number,
            self.bad_parent_score_thereshold_scheduler_end_number,
        )
        prune_count = 0
        
        for chromosome_index in range(len(choromosome_list)-1, -1, -1):
            if choromosome_list[chromosome_index].bad_parent_score > bad_parent_score_thereshold:
                prune_count += 1
                choromosome_list.pop(chromosome_index)
        if do_replace:
            for _ in prune_count:
                new_chromosome = self.__create_individual()
                self.evaluation_func(new_chromosome)
                choromosome_list.append(new_chromosome)
        return prune_count
    
    def __prune_old_chromosome(self, choromosome_list, do_replace=False) -> int:
        prune_count= 0
        for choromosome in choromosome_list:
            if choromosome.age> self.age_thereshold:
                prune_count+=1
                choromosome_list.remove(choromosome)
                if do_replace:
                    new_chromosome = self.__create_individual()
                    self.evaluation_func(new_chromosome)
                    choromosome_list.append(new_chromosome)
        return prune_count

    def __parent_selection(self, chromosome_list):
        if hasattr(self, "ps_q"):
            return self.parent_selection_func(chromosome_list, self.ps_q)
        return self.parent_selection_func(chromosome_list)

    def __remaining_selection(self, chromosome_list, remaining_size):
        if hasattr(self, "rs_q"):
            return self.remaining_selection_func(chromosome_list, self.rs_q, remaining_size)
        return self.remaining_selection_func(chromosome_list, remaining_size)
    
    def __select_next_generation_basedon_mode(self, population, children):
        if self.mode == "m,l":
            return children
        elif self.mode == "m+l":
            return [j for i in [population, children] for j in i]
        else:
            raise Exception(f"mode {self.mode} is not supported!")
        
    def __increase_age_of_all_population(self, population):
        for chromosome in population:
            chromosome.increase_age()
    
    def __copy_parent_to_child(self, parent):
        child= copy.deepcopy(parent)
        child.age=0
        child.bad_parent_score= 0
        child.crossover_attendance= 0
        return child
        
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
                child1 = self.__copy_parent_to_child(parent1)
                child2 = self.__copy_parent_to_child(parent2)

            if random.random() < self.mutation_probability:
                self.mutation_func(child1)
            if random.random() < self.mutation_probability:
                self.mutation_func(child2)

            self.evaluation_func(child1)
            self.evaluation_func(child2)

            if child1.fitness <= parent1.fitness and child2.fitness <= parent1.fitness:
                parent1.increase_bad_parent_score()
            else:
                parent1.decrease_bad_parent_score()
            if child1.fitness <= parent2.fitness and child2.fitness <= parent2.fitness:
                parent2.increase_bad_parent_score()
            else:
                parent2.decrease_bad_parent_score()

            # add to list
            children_list.append(child1)
            children_list.append(child2)

        return children_list
    
    def __save_final_result(self, best_chromosome, current_iteration_number):
        with open(os.path.join(self.result_directory, 'final_answer.json'), 'w') as file_to_write:
            json.dump(best_chromosome.to_dict(), file_to_write, indent=4)
            
        with open(os.path.join(self.result_directory, 'results.pkl'), 'wb') as file_to_write:
            pickle.dump([self.avg_fitness_list,
                         self.var_fitness_list,
                         self.best_fitness_list,
                         self.prune_bad_parent_count_list,
                         self.prune_old_chromosome_count_list], file_to_write)
            pickle.dump(self.statistics, file_to_write)
            pickle.dump(self.statistic_sampling_period, file_to_write)
            pickle.dump(current_iteration_number, file_to_write)
            
    def run(self):
        population= None
        current_iteration_number= None
        best_chromosome= None
        if self.checkpoint_base_directory is not None:
            population, current_iteration_number, best_chromosome= self.__temp_chromosome_list, self.__temp_current_iteration_number, self.__temp_best_chromosome
        else:
            best_chromosome = self.individual_class(
                genome_size=self.genome_size,
                init_with_random_genome=True,
            )
            self.evaluation_func(best_chromosome)
            population = self.__create_population()
            self.__evaluationAll(population)
            
            current_iteration_number = 1            
        
        start_time= time.time()
        while(True):
            children = self.__crossover_and_mutation(population)
            self.__evaluationAll(children)
            
            next_generation_candidates = self.__select_next_generation_basedon_mode(population, children)

            best_chromosome_in_current_iteration = max(next_generation_candidates, key=lambda x: x.fitness)
            
            if best_chromosome.fitness < best_chromosome_in_current_iteration.fitness:
                best_chromosome = copy.deepcopy(best_chromosome_in_current_iteration)

            population = self.__remaining_selection(next_generation_candidates, self.population_size)

            prune_bad_parent_count= 0
            if self.bad_parent_score_thereshold_scheduler_type is not None:
                prune_bad_parent_count= self.__prune_bad_parent(population, current_iteration_number)
            
            self.__increase_age_of_all_population(population)
            
            prune_old_chromosome_count= 0
            if self.age_thereshold is not None:
                prune_old_chromosome_count= self.__prune_old_chromosome(population)
            
            avg_fitness= None
            if TERMINATION_CONDITION_PHENOTYPIC_DIVERSITY in self.termination_condition_handler.termination_conditions:
                avg_fitness= self.__compute_avg_fitness(population)
               
            if current_iteration_number % self.statistic_sampling_period==0:
                if self.avg_fitness_list is not None:
                    if avg_fitness is not None:
                        self.avg_fitness_list.append(avg_fitness)
                    else:
                        self.avg_fitness_list.append(self.__compute_avg_fitness(population))
                if self.var_fitness_list is not None:
                    if avg_fitness is not None:
                        self.var_fitness_list.append(self.__compute_var_fitness_with_avg(population, avg_fitness))
                    elif self.avg_fitness_list is not None:
                        self.var_fitness_list.append(self.__compute_var_fitness_with_avg(population, self.avg_fitness_list[-1]))
                    else:
                        self.var_fitness_list.append(self.__compute_var_fitness_with_avg(population, self.__compute_avg_fitness(population)))
                if self.best_fitness_list is not None:
                    self.best_fitness_list.append(best_chromosome_in_current_iteration.fitness)
                if self.prune_bad_parent_count_list is not None:
                    self.prune_bad_parent_count_list.append(prune_bad_parent_count)
                if self.prune_old_chromosome_count_list is not None:
                    self.prune_old_chromosome_count_list.append(prune_old_chromosome_count)
                    
            terminate, message = self.termination_condition_handler.check_termination(
                population= population,
                avg_fitness= avg_fitness,
                best_fitness= best_chromosome_in_current_iteration.fitness,
                iteration_number= current_iteration_number,
                population_size= self.population_size,
                generation_size= self.generation_size,
            )
            

            if terminate:
                self._logger.info(message)
                break

            current_iteration_number+=1
        
            if self.checkpoint_save_period is not None:
                if current_iteration_number%self.checkpoint_save_period==0:
                    end_time=time.time()
                    self._logger.info(f'Save checkpoint at iteration {current_iteration_number}')
                    self.__save_checkpoint(
                        population,
                        current_iteration_number,
                        best_chromosome,
                        self.termination_condition_handler.termination_conditions,
                        self.termination_condition_handler.phenotypic_diversity_window_size,
                        self.termination_condition_handler.phenotypic_diversity_error_thereshold,
                        self.termination_condition_handler.genotypic_diversity_window_size,
                        self.termination_condition_handler.genotypic_diversity_error_thereshold,
                        self.termination_condition_handler.fitness_limit_threshold,
                        self.termination_condition_handler.iterations_number_threshold,
                        self.termination_condition_handler.evaluation_number_threshold,
                        end_time-start_time,
                    )
                    
        end_time= time.time()
        self._logger.info(f'Runtime: {end_time-start_time+self.elapsed_time} seconds')
        self._logger.info('Saving results')
        self.__save_final_result(best_chromosome, current_iteration_number)
        if self.visualize:
            self.visualizer.plot_diagrams(
                current_iteration_number,
                self.avg_fitness_list,
                self.var_fitness_list,
                self.best_fitness_list,
                self.prune_bad_parent_count_list,
                self.prune_old_chromosome_count_list
            )
            self._logger.info('Diagrams plotted successfuly.')
        return self.base_directory
    
    def show_available_parent_selection_type(self, return_instead_of_print=False):
        if return_instead_of_print:
            return AVAILABLE_PARENT_SELECTION_ALGORITHMS
        print('Available Parent Selection Algorithm:')
        print(AVAILABLE_PARENT_SELECTION_ALGORITHMS)
        
    def show_available_remaining_selection_type(self, return_instead_of_print=False):
        if return_instead_of_print:
            return AVAILABLE_REMAINING_SELECTION_ALGORITHMS
        print('Available Remaining Selection Algorithm:')
        print(AVAILABLE_REMAINING_SELECTION_ALGORITHMS)    
    
    def show_available_termination_conditions(self, return_instead_of_print=False):
        if return_instead_of_print:
            return AVAILABLE_TERMINATION_CONDITIONS
        print('Available Termination Conditions:')
        print(AVAILABLE_TERMINATION_CONDITIONS)
    
    def show_available_statistics(self, return_instead_of_print=False):
        if return_instead_of_print:
            return AVAILABLE_STATISTICS
        print('Available Plot Types:')
        print(AVAILABLE_STATISTICS)
    
    def show_available_mode(self, return_instead_of_print=False):
        if return_instead_of_print:
            return AVAILABLE_MODES
        print('Available Modes:')
        print(AVAILABLE_MODES)
    
    def show_available_bad_parent_score_thereshold_scheduler_types(self, return_instead_of_print=False):
        if return_instead_of_print:
            return AVAILABLE_BAD_PARENT_SCORE_THERESHOLD_SCHEDULER_TYPE
        print('Available Bad Parent Score Thereshold Scheduler Types:')
        print(AVAILABLE_BAD_PARENT_SCORE_THERESHOLD_SCHEDULER_TYPE)
        
    def show_all_available_functions_and_values_of_project(self):
        print('Available Parent Selection Algorithm:')
        print(AVAILABLE_PARENT_SELECTION_ALGORITHMS)
        print()
        
        print('Available Remaining Selection Algorithm:')
        print(AVAILABLE_REMAINING_SELECTION_ALGORITHMS)
        print()
        
        print('Available Termination Conditions:')
        print(AVAILABLE_TERMINATION_CONDITIONS)
        print()
        
        print('Available Plot Types:')
        print(AVAILABLE_STATISTICS)
        print()
        
        print('Available Modes:')
        print(AVAILABLE_MODES)
        print()
        
        print('Available Bad Parent Score Thereshold Scheduler Types:')
        print(AVAILABLE_BAD_PARENT_SCORE_THERESHOLD_SCHEDULER_TYPE)
    
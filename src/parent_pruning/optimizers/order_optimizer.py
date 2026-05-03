import os

from parent_pruning.optimizers.utils import init_function_by_name
from parent_pruning.optimizers.base_optimizer import BaseOptimizer
from parent_pruning.individuals.order_individual import OrderIndividual
from parent_pruning.mutation_algorithms import order_mutation as order_mutation_module
from parent_pruning.crossover_algorithms import order_crossover as order_crossover_module
from parent_pruning.configs.base_optimizer_config import (
    AVAILABLE_MODES,
    AVAILABLE_TERMINATION_CONDITIONS,
    AVAILABLE_STATISTICS,
    AVAILABLE_BAD_PARENT_SCORE_THERESHOLD_SCHEDULER_TYPE,
    AVAILABLE_PARENT_SELECTION_ALGORITHMS,
    AVAILABLE_REMAINING_SELECTION_ALGORITHMS,
)
from parent_pruning.configs.order_optimizer_config import (
    AVAILABLE_CROSSOVER_ALGORITHMS, 
    AVAILABLE_MUTATION_ALGORITHMS, 
    CROSSOVER_PROBABILITY_DEFAULT_VALUE, 
    MODE_DEFAULT_VALUE, 
    MUTATION_PROBABILITY_DEFAULT_VALUE, 
    TERMINATION_CONDITIONS_DEFAULT_VALUE,
    VISUALIZE_DEFAULT_VALUE,
)


class OrderOptimizer(BaseOptimizer):
    def __validation(self, crossover_type, mutation_type,):
        if crossover_type not in AVAILABLE_CROSSOVER_ALGORITHMS:
            raise Exception('')
        if mutation_type not in AVAILABLE_MUTATION_ALGORITHMS:
            raise Exception('')

    def __mutation_func_determiner(self, mutation_type):
        self.mutation_func = init_function_by_name(
            order_mutation_module, mutation_type, "mutation"
        )

    def __crossover_type_func_determiner(self, crossover_type):
        self.crossover_func = init_function_by_name(
            order_crossover_module, crossover_type, "crossover"
        )
        
    def __generate_note_file(self):
        self._logger.info('Generate note file')
        text= f'Project Name: {self.project_name}\
            \ngenome_size: {self.genome_size}\
            \npopulation_size: {self.population_size}\
            \ngeneration_size: {self.generation_size}\
            \nparent_selection_type: {self.parent_selection_type}\
            \nremaining_selection_type: {self.remaining_selection_type}\
            \ncrossover_type: {self.crossover_type}\
            \nmutation_type: {self.mutation_type}\
            \ntermination_conditions: {self.termination_condition_handler.termination_conditions}\
            \nncrossover_probability: {self.crossover_probability}\
            \nmutation_probability: {self.mutation_probability}\
            \nmode: {self.mode}'
        with open(os.path.join(self.base_directory,"note.txt"), "w") as file_to_write:
            file_to_write.write(text)
            
    def __load_order_checkpoint(self):
        self.__mutation_func_determiner(self.mutation_type)
        self.__crossover_type_func_determiner(self.crossover_type)
        
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
        iterations_number= None,
        statistics= None,
        statistic_sampling_period= None,
        evaluation_number=None,
        fitness_limit_threshold=None,
        age_thereshold= None,
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
        # source_spots_in_genome= None,
        # destination_spots_in_genome= None,
    ) -> None:
        super().__init__(
            project_name,
            input_data,
            genome_size,
            population_size,
            generation_size,
            parent_selection_type,
            remaining_selection_type,
            crossover_type,
            mutation_type,  
            termination_conditions,
            crossover_probability,
            mutation_probability,
            mode,
            iterations_number,
            statistics,
            statistic_sampling_period,
            evaluation_number,
            fitness_limit_threshold,
            age_thereshold,
            bad_parent_score_thereshold_scheduler_type,
            bad_parent_score_thereshold_scheduler_start_number,
            bad_parent_score_thereshold_scheduler_end_number,
            phenotypic_diversity_window_size,
            phenotypic_diversity_error_thereshold,
            genotypic_diversity_window_size,
            genotypic_diversity_error_thereshold,
            visualize,
            checkpoint_save_period,
            checkpoint_base_directory,
            # TODO:
            # source_spots_in_genome,
            # destination_spots_in_genome,
        )
        self._logger.info(f'List of available `Order Crossover Algorithms` functions:{AVAILABLE_CROSSOVER_ALGORITHMS}')
        self._logger.info(f'List of available `Order Mutation Algorithms` functions:{AVAILABLE_MUTATION_ALGORITHMS}')
        
        if checkpoint_base_directory is not None:
            self._logger.info('Load order optimizer')
            self.__load_order_checkpoint()
        else:
            self.__validation(crossover_type, mutation_type)
            self._logger.info('Initialize order optimizer')
            self.__mutation_func_determiner(self.mutation_type)
            self.__crossover_type_func_determiner(self.crossover_type)
            self.__generate_note_file()
            
        self.individual_class= OrderIndividual

    def show_available_crossover_types(self, return_instead_of_print=False):
        if return_instead_of_print:
            return AVAILABLE_CROSSOVER_ALGORITHMS
        print('Available Crossover types:')
        print(AVAILABLE_CROSSOVER_ALGORITHMS)
    
    def show_available_mutation_type(self, return_instead_of_print=False):
        if return_instead_of_print:
            return AVAILABLE_MUTATION_ALGORITHMS
        print('Available Mutation types:')
        print(AVAILABLE_MUTATION_ALGORITHMS)
        
    def show_available_mode(self, return_instead_of_print=False):
        if return_instead_of_print:
            return AVAILABLE_MODES
        print('Available Modes:')
        print(AVAILABLE_MODES)
    
    def show_available_bad_parent_score_thereshold_scheduler_types(self):
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
        print()
        
        print('Available Parent Selection Algorithm:')
        print(AVAILABLE_PARENT_SELECTION_ALGORITHMS)
        print()
        
        print('Available Remaining Selection Algorithm:')
        print(AVAILABLE_REMAINING_SELECTION_ALGORITHMS)
        print()
        
        print('Available Mutation types:')
        print(AVAILABLE_MUTATION_ALGORITHMS)
        print()
        
        print('Available Crossover types:')
        print(AVAILABLE_CROSSOVER_ALGORITHMS)
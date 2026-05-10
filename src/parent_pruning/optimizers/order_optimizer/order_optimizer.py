import os

from .__validator import validation
from parent_pruning.optimizers._utils import init_function_by_name
from parent_pruning.individuals.order_individual import OrderIndividual
from parent_pruning.optimizers._base_optimizer.base_optimizer import BaseOptimizer
from parent_pruning.mutation import order_mutation_methods as order_mutation_module
from parent_pruning.crossover import order_crossover_methods as order_crossover_module
from parent_pruning.configs.order_optimizer_config import (
    AVAILABLE_CROSSOVER_METHODS, 
    AVAILABLE_MUTATION_METHODS, 
    CROSSOVER_PROBABILITY_DEFAULT_VALUE, 
    MODE_DEFAULT_VALUE, 
    MUTATION_PROBABILITY_DEFAULT_VALUE, 
    TERMINATION_CONDITIONS_DEFAULT_VALUE,
    VISUALIZE_DEFAULT_VALUE,
)
from .__utils import (
    show_all_availables,
    show_available_modes,
    show_available_crossover_methods,
    show_available_mutation_methods,
)

class OrderOptimizer(BaseOptimizer):

    def __mutation_func_determiner(self, mutation_method):
        self.mutation_func = init_function_by_name(
            order_mutation_module, mutation_method, "mutation"
        )

    def __crossover_func_determiner(self, crossover_method):
        self.crossover_func = init_function_by_name(
            order_crossover_module, crossover_method, "crossover"
        )
        
    def __generate_note_file(self):
        self._logger.info('Generate note file')
        text= f'Project Name: {self.project_name}\
            \nGenome_size: {self.genome_size}\
            \nPopulation_size: {self.population_size}\
            \nGeneration_size: {self.generation_size}\
            \nParent selection Method: {self.parent_selection_method}\
            \nRemaining Selection Method: {self.remaining_selection_method}\
            \nCrossover Method: {self.crossover_method}\
            \nMutation Method: {self.mutation_method}\
            \nTermination Conditions: {self.termination_condition_handler.termination_conditions}\
            \nCrossover Probability: {self.crossover_probability}\
            \nMutation Probability: {self.mutation_probability}\
            \nMode: {self.mode}'
        with open(os.path.join(self.base_directory,"note.txt"), "w") as file_to_write:
            file_to_write.write(text)
            
    def __load_order_checkpoint(self):
        self.__mutation_func_determiner(self.mutation_method)
        self.__crossover_func_determiner(self.crossover_method)
        
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
        iterations_number= None,
        statistics= None,
        statistic_sampling_period= None,
        evaluation_number=None,
        fitness_limit_threshold=None,
        phenotypic_diversity_window_size=None,
        phenotypic_diversity_error_thereshold=None,
        genotypic_diversity_window_size=None,
        genotypic_diversity_error_thereshold=None,
        visualize= VISUALIZE_DEFAULT_VALUE,
        checkpoint_save_period=None,
        checkpoint_base_directory=None,
        extension_directory=None,
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
            evaluation_number,
            fitness_limit_threshold,
            phenotypic_diversity_window_size,
            phenotypic_diversity_error_thereshold,
            genotypic_diversity_window_size,
            genotypic_diversity_error_thereshold,
            visualize,
            checkpoint_save_period,
            checkpoint_base_directory,
            extension_directory,
            # TODO:
            # source_spots_in_genome,
            # destination_spots_in_genome,
        )
        self._logger.info(f'List of available `Order Crossover Methods` functions:{AVAILABLE_CROSSOVER_METHODS}')
        self._logger.info(f'List of available `Order Mutation Methods` functions:{AVAILABLE_MUTATION_METHODS}')
        
        if checkpoint_base_directory is not None:
            self._logger.info('Load order optimizer')
            self.__load_order_checkpoint()
        else:
            validation(crossover_method, mutation_method)
            self._logger.info('Initialize order optimizer')
            self.__mutation_func_determiner(self.mutation_method)
            self.__crossover_func_determiner(self.crossover_method)
            self.__generate_note_file()
            
        self.individual_class= OrderIndividual
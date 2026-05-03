import os
import pickle
import matplotlib.pyplot as plt

from parent_pruning.configs.common import (
    STATISTIC_AVG_FITNESS,
    STATISTIC_VAR_FITNESS,
    STATISTIC_BEST_FITNESS,
    STATISTIC_PRUNE_BAD_PARENT_COUNT,
    STATISTIC_PRUNE_OLD_CHROMOSOME_COUNT,
)


class Visualizer:
    def __init__(self, statistics, statistic_sampling_period, results_directory):
        # TODO: use bitmap for faster access to memory
        self.statistics = statistics
        self.statistic_sampling_period = statistic_sampling_period
        self.results_directory= results_directory

    def plot_diagrams(self, iterations_number, avg_fitness_list, var_fitness_list, best_fitness_list, prune_bad_parent_count_list, prune_old_chromosome_count_list):
        if self.statistics is None:
            return

        statistics_size = len(self.statistics)

        if statistics_size == 0:
            return

        plt.figure(figsize=(1.7*statistics_size, 6))

        plot_counter = 1

        if STATISTIC_AVG_FITNESS in self.statistics:
            plt.subplot(statistics_size, 1, plot_counter)
            plt.plot([self.statistic_sampling_period * i for i in range(int(iterations_number/self.statistic_sampling_period))], avg_fitness_list)
            plt.xlabel("iteration")
            plt.ylabel("avg fitness")
            plt.title("avg fitness in each iteration")

            plot_counter+=1

        if STATISTIC_VAR_FITNESS in self.statistics:
            plt.subplot(statistics_size, 1, plot_counter)
            plt.plot([self.statistic_sampling_period * i for i in range(int(iterations_number/self.statistic_sampling_period))], var_fitness_list)
            plt.xlabel("iteration")
            plt.ylabel("var fitness")
            plt.title("var fitness in each iteration")

            plot_counter+=1

        if STATISTIC_BEST_FITNESS in self.statistics:
            plt.subplot(statistics_size, 1, plot_counter)
            plt.plot([self.statistic_sampling_period * i for i in range(int(iterations_number/self.statistic_sampling_period))], best_fitness_list)
            plt.xlabel("iteration")
            plt.ylabel("best fitness")
            plt.title("best fitness in each iteration")

            plot_counter+=1


        if STATISTIC_PRUNE_BAD_PARENT_COUNT in self.statistics:
            plt.subplot(statistics_size, 1, plot_counter)
            plt.plot([self.statistic_sampling_period * i for i in range(int(iterations_number/self.statistic_sampling_period))], prune_bad_parent_count_list)
            plt.xlabel("iteration")
            plt.ylabel("kill bad parent count")
            plt.title("kill bad parent count in each iteration")

            plot_counter+=1
        
        if STATISTIC_PRUNE_OLD_CHROMOSOME_COUNT in self.statistics:
            plt.subplot(statistics_size, 1, plot_counter)
            plt.plot([self.statistic_sampling_period * i for i in range(int(iterations_number/self.statistic_sampling_period))], prune_old_chromosome_count_list)
            plt.xlabel("iteration")
            plt.ylabel("kill old count")
            plt.title("kill old count per iteration")

            plot_counter+=1

        plt.tight_layout()
        plt.savefig(os.path.join(self.results_directory, 'diagrams.png'))
        plt.close()
    
    
    def plot_results_diagrams(self, output_base_directory):
        self.results_directory= os.path.join(output_base_directory, 'results')
        # avg_fitness_list= None
        # var_fitness_list=None 
        # best_fitness_list=None
        # prune_bad_parent_count_list=None
        # prune_old_chromosome_count_list= None 
        # current_iteration_number=None
        with open(os.path.join(self.results_directory, 'results.pkl'), 'rb') as file_to_read:
            avg_fitness_list, var_fitness_list, best_fitness_list, prune_bad_parent_count_list, prune_old_chromosome_count_list= pickle.load(file_to_read)
            self.statistics= pickle.load(file_to_read)
            self.statistic_sampling_period= pickle.load(file_to_read)
            current_iteration_number= pickle.load(file_to_read)
            self.plot_diagrams(current_iteration_number, avg_fitness_list, var_fitness_list, best_fitness_list, prune_bad_parent_count_list, prune_old_chromosome_count_list)
            
    
    def visualize_checkpoint(self):
        # Todo
        pass
import os
import pickle
import matplotlib.pyplot as plt

from parent_pruning.configs._enums.termination_conditions_enums import (
    STATISTIC_AVG_FITNESS,
    STATISTIC_VAR_FITNESS,
    STATISTIC_BEST_FITNESS,
    STATISTIC_PRUNINGS,
)


class Visualizer:
    def __init__(self, statistics, statistic_sampling_period, results_directory):
        # TODO: use bitmap for faster access to memory
        self.statistics = statistics
        self.statistic_sampling_period = statistic_sampling_period
        self.results_directory = results_directory

    def plot_diagrams(self, iterations_number, avg_fitness_list, var_fitness_list, best_fitness_list, pruning_count_list, pruning_methods):
        if self.statistics is None:
            return

        rows_number = len(self.statistics) - 1 + len(pruning_methods)

        if rows_number == 0:
            raise Exception()

        plt.figure(figsize=(1.75 * rows_number, 6))

        column_index = 1
        row_index = 1

        if STATISTIC_AVG_FITNESS in self.statistics:
            plt.subplot(rows_number, column_index, row_index)
            plt.plot([self.statistic_sampling_period * i for i in range(int(iterations_number / self.statistic_sampling_period))], avg_fitness_list)
            plt.xlabel("iteration")
            plt.ylabel("avg fitness")
            plt.title("avg fitness in each iteration")

            row_index += 1

        if STATISTIC_VAR_FITNESS in self.statistics:
            plt.subplot(rows_number, column_index, row_index)
            plt.plot([self.statistic_sampling_period * i for i in range(int(iterations_number / self.statistic_sampling_period))], var_fitness_list)
            plt.xlabel("iteration")
            plt.ylabel("var fitness")
            plt.title("var fitness in each iteration")

            row_index += 1

        if STATISTIC_BEST_FITNESS in self.statistics:
            plt.subplot(rows_number, column_index, row_index)
            plt.plot([self.statistic_sampling_period * i for i in range(int(iterations_number / self.statistic_sampling_period))], best_fitness_list)
            plt.xlabel("iteration")
            plt.ylabel("best fitness")
            plt.title("best fitness in each iteration")

            row_index += 1

        if STATISTIC_PRUNINGS in self.statistics:
            for pruning_method_index in range(len(pruning_count_list)):
                plt.subplot(rows_number, column_index, row_index)
                plt.plot(
                    [self.statistic_sampling_period * i for i in range(int(iterations_number / self.statistic_sampling_period))],
                    pruning_count_list[pruning_method_index],
                )
                plt.xlabel("iteration")
                plt.ylabel(f"{pruning_methods[pruning_method_index]}")
                plt.title(f"{pruning_methods[pruning_method_index]} in each iteration")

                row_index += 1

        plt.tight_layout()
        plt.savefig(os.path.join(self.results_directory, "diagrams.png"))
        plt.close()

    def plot_results_diagrams(self, output_base_directory):
        self.results_directory = os.path.join(output_base_directory, "results")
        with open(os.path.join(self.results_directory, "results.pkl"), "rb") as file_to_read:
            avg_fitness_list, var_fitness_list, best_fitness_list, pruning_count_list, pruning_methods = pickle.load(file_to_read)
            self.statistics = pickle.load(file_to_read)
            self.statistic_sampling_period = pickle.load(file_to_read)
            current_iteration_number = pickle.load(file_to_read)
            self.plot_diagrams(current_iteration_number, avg_fitness_list, var_fitness_list, best_fitness_list, pruning_count_list, pruning_methods)

    def visualize_checkpoint(self):
        # Todo
        pass

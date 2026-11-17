from __future__ import annotations

import os
import pickle

import matplotlib.pyplot as plt
import numpy as np

from pyevolutionary._enums import StatisticsEnum

__all__ = ["Visualizer"]


class Visualizer:
    def __init__(self):
        super().__init__()

    @staticmethod
    def plot_diagrams(
        statistics: list[str],
        statistic_sampling_period: int,
        iterations_number: int,
        avg_fitness_list: list[float],
        var_fitness_list: list[float],
        best_fitness_list: list[float],
        pruning_count_list_in_each_iteration: list[list],
        pruning_methods: list[str],
        results_directory: str,
    ):
        if statistics is None:
            return

        rows_number = len(statistics)
        if pruning_methods is not None:
            rows_number = rows_number - 1 + len(pruning_methods)

        if rows_number == 0:
            raise ValueError()

        plt.figure(figsize=(1.75 * rows_number, 6))

        column_index = 1
        row_index = 1

        if StatisticsEnum.AVG_FITNESS in statistics:
            plt.subplot(rows_number, column_index, row_index)
            plt.plot([statistic_sampling_period * i for i in range(int(iterations_number / statistic_sampling_period))], avg_fitness_list)
            plt.xlabel("iteration")
            plt.ylabel("avg fitness")
            plt.title("avg fitness in each iteration")

            row_index += 1

        if StatisticsEnum.VAR_FITNESS in statistics:
            plt.subplot(rows_number, column_index, row_index)
            plt.plot([statistic_sampling_period * i for i in range(int(iterations_number / statistic_sampling_period))], var_fitness_list)
            plt.xlabel("iteration")
            plt.ylabel("var fitness")
            plt.title("var fitness in each iteration")

            row_index += 1

        if StatisticsEnum.BEST_FITNESS in statistics:
            plt.subplot(rows_number, column_index, row_index)
            plt.plot([statistic_sampling_period * i for i in range(int(iterations_number / statistic_sampling_period))], best_fitness_list)
            plt.xlabel("iteration")
            plt.ylabel("best fitness")
            plt.title("best fitness in each iteration")

            row_index += 1

        if StatisticsEnum.PRUNINGS in statistics:
            pruning_count_list = np.array(pruning_count_list_in_each_iteration)
            pruning_count_list = pruning_count_list.T
            for pruning_method_index in range(len(pruning_methods)):
                plt.subplot(rows_number, column_index, row_index)
                plt.plot(
                    [statistic_sampling_period * i for i in range(int(iterations_number / statistic_sampling_period))],
                    pruning_count_list[pruning_method_index],
                )
                plt.xlabel("iteration")
                plt.ylabel(f"{pruning_methods[pruning_method_index].replace('_', ' ')}")
                plt.title(f"{pruning_methods[pruning_method_index].replace('_', ' ')} in each iteration")

                row_index += 1

        plt.tight_layout()
        plt.savefig(os.path.join(results_directory, "diagrams.png"))
        plt.close()

    @staticmethod
    def plot_results_diagrams(output_directory: str):
        with open(os.path.join(output_directory, "results", "results.pkl"), "rb") as file_to_read:
            avg_fitness_list, var_fitness_list, best_fitness_list, pruning_count_list = pickle.load(file_to_read)
            statistics = pickle.load(file_to_read)
            statistic_sampling_period = pickle.load(file_to_read)
            pruning_methods = pickle.load(file_to_read)
            current_iteration_number = pickle.load(file_to_read)
            Visualizer.plot_diagrams(
                statistics,
                statistic_sampling_period,
                current_iteration_number,
                avg_fitness_list,
                var_fitness_list,
                best_fitness_list,
                pruning_count_list,
                pruning_methods,
                os.path.join(output_directory, "results"),
            )

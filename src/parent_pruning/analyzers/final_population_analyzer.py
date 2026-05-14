import os
import sys
import pickle
import logging
import numpy as np
import matplotlib.pyplot as plt

from collections import Counter
from parent_pruning.individuals._base_individual import BaseIndividual
from parent_pruning._configs.directories import LOG_DIRECTORY_DEFAULT, ANALYZE_DIRECOTRY_DEFAULT


class FinalPopulationAnalyzer:
    def __create_log_folders(self, base_directory):
        self.log_directory = os.path.join(base_directory, LOG_DIRECTORY_DEFAULT)
        os.makedirs(self.log_directory, exist_ok=True)

        self.analyze_directory = os.path.join(base_directory, ANALYZE_DIRECOTRY_DEFAULT)
        os.makedirs(self.analyze_directory, exist_ok=True)

    def __init_logger(self, show_in_console):
        self._logger = logging.getLogger("analyzer_logger")
        self._logger.setLevel(logging.INFO)
        handler = logging.FileHandler(os.path.join(self.log_directory, "analyze.log"))
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)
        if show_in_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            self._logger.addHandler(console_handler)

    def __init__(self, base_directory:str, chromosome_list:list[BaseIndividual]=None, show_in_console:bool=False):
        self.chromosome_list = chromosome_list
        self.base_directory = base_directory
        self.genome_dict = {}
        self.__create_log_folders(self.base_directory)
        self.__init_logger(show_in_console)

    def load_chromosome_list(self, chromosome_list_pkl_path:str):
        with open(chromosome_list_pkl_path, "rb") as file_to_read:
            self.chromosome_list = pickle.load(file_to_read)

    def load_final_population_from_result_directory(self):
        with open(os.path.join(self.base_directory, "results", "final_population.pkl"), "rb") as file_to_read:
            self.chromosome_list = pickle.load(file_to_read)

    def run_full_analyzer(self):
        self.genotypic_diversity_equivalence()
        self.score_analyzer()
        self.age_analyzer()
    
    def __hamming_static(self, first_genome, second_genome):
        return np.sum(np.array(first_genome) != np.array(second_genome))

    def __hamming_circular(self, first_genome, second_genome):
        n = len(first_genome)

        pos_a = {x: i for i, x in enumerate(first_genome)}
        pos_b = {x: i for i, x in enumerate(second_genome)}

        matches = [0] * n

        for x in pos_a:
            k = (pos_a[x] - pos_b[x]) % n
            matches[k] += 1

        return max(matches)

    def __hamming(self, unique_genome_list, unique_genome_count, use_circular_hamming=True):
        if len(self.chromosome_list) < 2:
            return 0.0
        
        choosen_hamming_func= None
        if use_circular_hamming:
            choosen_hamming_func= self.__hamming_circular
        else:
            choosen_hamming_func= self.__hamming_static

        N = len(unique_genome_list)
        dists = []
        for i in range(N):
            for j in range(i + 1, N):
                dists.append(unique_genome_count[i] * choosen_hamming_func(unique_genome_list[i], unique_genome_list[j]))
        final_answer= np.mean(dists)
        self._logger.info("Hamming diversity calculated")
        return final_answer
    
    def __entropy(self, unique_genome_count):
        counts= np.array(unique_genome_count)
        probs = counts / counts.sum()
        final_answer=-np.sum(probs * np.log2(probs))
        self._logger.info("Hamming diversity entropy")
        return final_answer
    
    def __gini(self, unique_genome_count):
        counts= np.array(unique_genome_count)
        probs = counts / counts.sum()
        final_answer= 1 - np.sum(probs ** 2)
        self._logger.info("Hamming diversity gini")
        return final_answer
    
    def genotypic_diversity_equivalence(self):
        for chromosome in self.chromosome_list:
            if chromosome.genome in self.genome_dict:
                self.genome_dict[chromosome.genome] += 1
            else:
                self.genome_dict[chromosome.genome] = 1
        
        unique_genome_list = self.genome_dict.keys()
        unique_genome_count = self.genome_dict.values()
        
        self._logger.info("Number of unique genoume counted")
        
        with open(os.path.join(self.analyze_directory, "analyze_result.txt"), "a", encoding="utf-8") as file_to_write:
            file_to_write.write("##########################")
            file_to_write.write("Genotypic Diversity")
            file_to_write.write("##########################")
            for key, value in self.genome_dict.items():
                file_to_write.write(f"{key}: {value}\n")
            file_to_write.write(f"Genotypic Diversity Rate - genome scale: {len(self.genome_dict) / self.chromosome_list}")
            file_to_write.write(f"Genotypic Diversity Entropy - genome scale: {self.__entropy(unique_genome_count)}")
            file_to_write.write(f"Genotypic Diversity GINI - genome scale: {self.__gini(unique_genome_count)}")
            file_to_write.write(f"Genotypic Diversity Hamming (Circular) - gen scale: {self.__hamming(unique_genome_list, unique_genome_count)}")

    def __attribute_analyzer(self, attribute_name):
        att_value_list = [getattr(chromosome, attribute_name) for chromosome in self.chromosome_list]

        att_value_max = max(att_value_list)
        att_value_min = min(att_value_list)
        att_value_avg = sum(att_value_list) / len(att_value_list)
        att_value_counts = Counter(att_value_list)

        with open(os.path.join(self.analyze_directory, "analyze_result.txt"), "a", encoding="utf-8") as file_to_write:
            file_to_write.write("##########################")
            file_to_write.write(f"Analyze {attribute_name.capitalize()}")
            file_to_write.write("##########################")
            file_to_write.write(f"Max Value: {att_value_max}")
            file_to_write.write(f"Min Value: {att_value_min}")
            file_to_write.write(f"Avg Value: {att_value_avg}")
            file_to_write.write(f"Count by {attribute_name}:")
            for key, count in sorted(att_value_counts.items()):
                file_to_write.write(f"{attribute_name}={key}: {count}")

        # 2) Plot the score distribution (histogram / empirical distribution)
        plt.figure(figsize=(8, 5))
        plt.hist(att_value_list, bins="auto", edgecolor="black", alpha=0.7)
        plt.xlabel(f"{attribute_name.capitalize()}")
        plt.ylabel("Number of Chromosome")
        plt.title(f"{attribute_name.capitalize()} Distribution")
        plt.grid(axis="y", alpha=0.3)
        plt.savefig(os.path.join(self.analyze_directory, f"{attribute_name}_distribution.png"))

        # 3) Optional: plot the empirical CDF (distribution function)
        sorted_value = np.sort(att_value_list)
        cdf = np.arange(1, len(sorted_value) + 1) / len(sorted_value)

        plt.figure(figsize=(8, 5))
        plt.step(sorted_value, cdf, where="post")
        plt.xlabel(f"{attribute_name.capitalize()}")
        plt.ylabel("F(x)")
        plt.title("Empirical Distribution Function (CDF)")
        plt.ylim(0, 1.05)
        plt.grid(alpha=0.3)
        plt.savefig(os.path.join(self.analyze_directory, f"{attribute_name}_cdf.png"))

    def score_analyzer(self):
        self.__attribute_analyzer("parent_score")

    def age_analyzer(self):
        self.__attribute_analyzer("age")
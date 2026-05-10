import numpy as np


class FinalPopulationAnalyzer:
    def __init__(self, chromosome_list, results_directory):
        self.chromosome_list= chromosome_list
        self.results_directory= results_directory
        
        self.genome_dict= {}
        
    def run_full_analyzer(self):
        pass
    
    def genotypic_diversity_equivalence(self):
        for chromosome in self.chromosome_list:
            if chromosome.genome in self.genome_dict:
                self.genome_dict[chromosome.genome]+= 1
            else:
                self.genome_dict[chromosome.genome]= 1
        return self.genome_dict, len(self.genome_dict)/self.chromosome_list


    def __hamming(self, first_genome, second_genome):
        return np.sum(np.array(first_genome) != np.array(second_genome))

    def genotypic_diversity_hamming(self):
        if len(self.chromosome_list) < 2:
            return 0.0
        
        if len(self.genome_dict)==0:
            self.genotypic_diversity_equivalence(self.chromosome_list)
        
        genome_list= self.genome_dict.keys()
        genome_count= self.genome_dict.values()
        
        N=len(genome_list)
        dists = []
        for i in range(N):
            for j in range(i+1, N):
                dists.append(genome_count[i] * self.__hamming(genome_list[i], genome_list[j]))
        return np.mean(dists)
    
    def score_analyzer(self):
        # distribution
        # count
        # store in file
        pass
    
    def age_analyzer(self):
        pass

    
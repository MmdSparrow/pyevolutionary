import random


def random_uniform(chromosome_list, remaining_size):
    return random.choices(chromosome_list, k=remaining_size)


def rank_based(chromosome_list, remaining_size):
    weights = [-1 / (x.fitness + 1) for x in chromosome_list]
    return random.choices(chromosome_list, weights, k=remaining_size)


def q_tournoment(chromosome_list, q, remaining_size):
    return [max(random.choices(chromosome_list, k=q), key=lambda x: x.fitness) for _ in range(remaining_size)]


def same(chromosome_list, _):
    return chromosome_list


def rank(chromosome_list, remaining_size):
    chromosome_list.sort(key=lambda x: x.fitness, reverse=True)
    winners_list = chromosome_list[:remaining_size]
    return winners_list

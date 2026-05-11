# TODO: do_replace option
def age_pruning(choromosome_list, current_iteration_number, age_thereshold, scheduler_func=None, scheduler_start=None, scheduler_end=None):
    prune_count = 0
    new_age_thereshold = age_thereshold
    if scheduler_func is not None:
        new_age_thereshold = scheduler_func(current_iteration_number, scheduler_start, scheduler_end)
    for chromosome_index in range(len(choromosome_list) - 1, -1, -1):
        if choromosome_list[chromosome_index].age > new_age_thereshold:
            prune_count += 1
            choromosome_list.pop(chromosome_index)
    return prune_count


def score_pruning(choromosome_list, current_iteration_number, score_thereshold, scheduler_func=None, scheduler_start=None, scheduler_end=None):
    prune_count = 0
    new_score_thereshold = score_thereshold
    if scheduler_func is not None:
        new_score_thereshold = scheduler_func(current_iteration_number, scheduler_start, scheduler_end)
    for chromosome_index in range(len(choromosome_list) - 1, -1, -1):
        if choromosome_list[chromosome_index].parent_score < new_score_thereshold:
            prune_count += 1
            choromosome_list.pop(chromosome_index)
    return prune_count


# def avg_pruning(choromosome_list, avg_fitness, current_iteration_number=None, scheduler_method=None, scheduler_start=None, scheduler_end=None):
#     pass

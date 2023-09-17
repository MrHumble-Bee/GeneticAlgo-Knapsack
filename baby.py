import random
import numpy as np

class baby:
    def __init__(self, num_items, cost_list, value_list, max_cost) -> None:
        self.dna = np.random.randint(0, 2, num_items, dtype=int) # list of 0 and 1 to denote whether item is in bag
        self.cost_list = np.array(cost_list)
        self.value_list = np.array(value_list)

        self.max_cost = max_cost

    def get_score(self):
        return np.dot(self.dna, self.value_list) if self.get_cost() <= self.max_cost else 0

    def get_cost(self):
        return np.dot(self.dna, self.cost_list)




if __name__ == '__main__':
    children_per_gen = 10
    item_costs = [i for i in range(10)]
    item_values = [10] + [1] * 9
    num_gen = 200
    max_cost = 25
    top_of_gen = [baby(len(item_costs), item_costs, item_values, max_cost) for _ in range(children_per_gen)]
    top_of_gen_total_score = sum([bb.get_score() for bb in top_of_gen])
    parent_pair = np.random.choice(top_of_gen, 2, replace=False, p=[child.get_score() / top_of_gen_total_score for child in top_of_gen])
    print(parent_pair[0].get_score(), parent_pair[1].get_score())


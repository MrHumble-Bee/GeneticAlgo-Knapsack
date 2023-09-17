import numpy as np
from baby import baby
import matplotlib.pyplot as plt


class Optimizer:
    def __init__(self, children_per_gen, item_costs, item_values, num_gen, max_cost) -> None:
        self.children_per_gen = children_per_gen
        self.num_gen = num_gen
        self.max_cost = max_cost
        self.item_costs = np.array(item_costs)
        self.item_values = np.array(item_values)

        self.all_generations = [] 
        self.current_generation = [baby(len(self.item_values), self.item_costs, self.item_values, self.max_cost) for _ in range(self.children_per_gen)]
        self.current_gen_score = self.get_current_gen_avg_score()
        self.growth = []
        self.gen_max_score = None
        self.all_gen_max_scores = []

    def run(self):
        for i in range(num_gen):
            self.rank_current_gen()
            self.growth.append(self.current_gen_score)
            self.all_gen_max_scores.append(self.gen_max_score)
            self.breed_next_gen()


    def breed_next_gen(self):
        self.all_generations.append(self.current_generation) # Log current generation
        new_generation = []

        # NEED TO BREED PARENTS
        self.rank_current_gen()
        top_of_gen = self.get_top_of_gen(percentile:=0.3)
        top_of_gen_total_score = sum([child.get_score() for child in top_of_gen]) 
        top_of_gen_total_score_sq = sum([child.get_score()**2 for child in top_of_gen])
        # print(self.current_generation)
        # print(int(percentile*len(self.current_generation)))
        for i in range(int(0.9*len(self.current_generation))):
            parent_pair = np.random.choice(top_of_gen, 2, replace=False, p=[(child.get_score()**2/top_of_gen_total_score_sq) for child in top_of_gen])
            # print(i, parent_pair[0].get_score(),parent_pair[0].dna, parent_pair[1].get_score(), parent_pair[1].dna)
            # TAKE TWO PARENTS AND BREED
            if parent_pair[0].get_score() >= parent_pair[1].get_score():
                dom_parent = parent_pair[0]
                sub_parent = parent_pair[1]
            else:
                dom_parent = parent_pair[1]
                sub_parent = parent_pair[0]

            RANDOM_GENE_RATE = 0
            dom_parent_gene_select = np.random.choice(list(range(0,len(item_values))), int((1 - RANDOM_GENE_RATE) * dom_parent.get_score() / (parent_pair[0].get_score() + parent_pair[1].get_score()) * len(item_values)), replace=False)
            sub_parent_gene_select = np.random.choice(list(set(range(0,len(item_values))) - set(dom_parent_gene_select)), int((1 - RANDOM_GENE_RATE) * sub_parent.get_score() / (parent_pair[0].get_score() + parent_pair[1].get_score()) * len(item_values)), replace=False)
            # random_gene_select = list(set(range(0,len(item_values))) - set(dom_parent_gene_select) - set(sub_parent_gene_select))
            # print(dom_parent_gene_select)
            # print(sub_parent_gene_select)
            # print(random_gene_select)

            child = baby(len(self.item_values), self.item_costs, self.item_values, self.max_cost)
            for dom_index in dom_parent_gene_select:
                child.dna[dom_index] = dom_parent.dna[dom_index]
            for sub_index in sub_parent_gene_select:
                child.dna[sub_index] = sub_parent.dna[sub_index]
            
            MUTATION_RATE = 0.05
            for i in range(len(child.dna)):
                if np.random.random(1) < MUTATION_RATE:
                    if child.dna[i] == 1:
                        child.dna[i] = 0
                    else:
                        child.dna[i] = 1


            # APPEND THE CHILD
            new_generation.append(child)
            # print(i, child.get_score())
        
        # FILL REMAINING WITH RANDOM CHILDREN
        self.current_generation = new_generation
        num_needed_children = self.children_per_gen - len(self.current_generation)
        self.current_generation += [baby(len(self.item_values), self.item_costs, self.item_values, self.max_cost) for _ in range(num_needed_children)]
        self.current_gen_score = self.get_current_gen_avg_score()

    def get_current_gen_avg_score(self):
        current_sum = 0
        for baby in self.current_generation:
            current_sum += baby.get_score()
        self.current_gen_score = current_sum / len(self.current_generation)
        self.gen_max_score = max([baby.get_score() for baby in self.current_generation])

        return self.current_gen_score
        
    def rank_current_gen(self):
        self.current_generation = sorted(self.current_generation, key=lambda x: x.get_score(), reverse=True)

    def get_top_of_gen(self, percentile: float=0.8):
        return self.current_generation[:int(len(self.current_generation) * percentile)]

    def plot_growth(self):
        plt.plot(list(range(len(self.growth))), self.growth)
        plt.plot(list(range(len(self.growth))), self.all_gen_max_scores)
        plt.show()


if __name__ == '__main__':
    # item_costs = [i for i in range(10)]
    # item_values = [10] + [1] * 9
    # max_cost = 25

    item_costs = [31,10,20,19,4,3,6]
    item_values = [70,20,39,37,7,5,10]
    max_cost = 50

    children_per_gen = 10
    num_gen = 200
    o = Optimizer(children_per_gen, item_costs, item_values, num_gen, max_cost)
    # top = o.get_top_of_gen(.8)
    # for bb in top:
    #     print(f'{bb.get_score():>3}', bb.dna)
    o.run()
    # all_gen = o.all_generations
    # for gen_idx, gen in enumerate(all_gen):
    #     print(f"Generation {gen_idx+1}")
    #     for i, bb in enumerate(gen):
    #         print(f"{bb.get_score():>4}", end=" ")
    #     print()
    #     print("-"*100)
    o.plot_growth()
    
    
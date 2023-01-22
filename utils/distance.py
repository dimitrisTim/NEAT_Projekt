import numpy as np
from genome import Genome

c1 = 1
c2 = 1
c3 = 0.4

def innovations_dict(parent1: Genome, parent2: Genome) -> dict:
    innovations = {}
    for connection in parent1.connections:
        innovations[connection.innovation] = {parent1 : connection}
    for connection in parent2.connections:
        if connection.innovation in innovations.keys():
            innovations[connection.innovation][parent2] = connection
        else:
            innovations[connection.innovation] = {parent2 : connection}
    return dict(sorted(innovations.items()))

def distance(p1, p2):
        inn_dict = innovations_dict(p1, p2)
        n_disjoint_genes = 0
        n_excess_genes = 0
        differences = []
        for _, genes_info in inn_dict.items():
            if len(genes_info) == 1:
                gene = list(genes_info.values())[0]
                owner = list(genes_info.keys())[0]
                not_owner = p1 if owner == p2 else p2
                if gene.innovation > max(not_owner.connections, key=lambda x: x.innovation).innovation:
                    n_excess_genes += 1
                else:
                    n_disjoint_genes += 1
            elif len(genes_info) >1:
                differences.append(abs(genes_info[p1].weight - genes_info[p2].weight))
        avg_weight_diff = np.mean(differences) if len(differences) > 0 else 0
        n_max_genes = max(len(p1.connections), len(p2.connections))
        N = max(len(p1.connections), len(p2.connections)) if n_max_genes > 20 else 1
        return c1 * n_excess_genes / N + c2 * n_disjoint_genes / N + c3 * avg_weight_diff
    

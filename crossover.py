from genome import Genome
from node import Node, NodeType
from connection import Connection
import numpy as np
import utils.distance as distance

def crossover(parent1: Genome, parent2: Genome, num_genomes: int) -> Genome:
    sorted_innovations = distance.innovations_dict(parent1, parent2)
    child_innovations = []
    fittest_parent = parent1 if parent1.fitness > parent2.fitness \
                    else parent2 if parent1.fitness < parent2.fitness \
                    else None
    for _, genes_info in sorted_innovations.items():        
        if len(genes_info) > 1:
            gene_owner = np.random.choice(list(genes_info.keys()))
            gene = genes_info[gene_owner]    
        else:
            gene_owner = list(genes_info.keys())[0]
            if fittest_parent == gene_owner or fittest_parent == None:
                gene = genes_info[gene_owner]
        child_innovations.append(gene)
    
    # Hidden nodes have always id > n_outputs
    n_hidden_nodes = max([connection.output for connection in child_innovations if connection.output >= parent1.n_outputs])
    # Both parent1 and parent2 have the same number of inputs and outputs
    child = Genome(num_genomes, parent1.n_inputs, parent1.n_outputs, init_connections=False)
    id = parent1.n_outputs
    for _ in range(n_hidden_nodes):
        child.nodes.append(Node(id, NodeType.HIDDEN))
        id += 1
    child.connections = child_innovations
    return child
from genome import Genome
from node import Node, NodeType
from connection import Connection

def crossover(parent1: Genome, parent2: Genome, num_genomes: int) -> Genome:
    child_num_inputs = max(parent1.n_inputs, parent2.n_inputs)
    child_num_hidden = max(parent1.n_hidden_nodes, parent2.n_hidden_nodes)
    child_num_outputs = max(parent1.n_outputs, parent2.n_outputs)
    child = Genome(num_genomes, child_num_inputs, child_num_outputs, init_connections=False)
    id = 0
    for _ in range(child_num_hidden):
        id += 1
        child.nodes.append(Node(id, NodeType.HIDDEN))

    for connection in parent1.connections:
        if not connection.enabled and connection in child.connections:
            child.connections.remove(connection)
            child.connections.append(connection)
        elif connection not in child.connections:
            child.connections.append(connection)

    for connection in parent2.connections:
        if not connection.enabled and connection in child.connections:
            child.connections.remove(connection)
            child.connections.append(connection)
        elif connection not in child.connections:
            child.connections.append(connection)

    return child
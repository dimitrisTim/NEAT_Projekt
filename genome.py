from utils import helpers
from node import Node, NodeType
from connection import Connection
import networkx as nx
import numpy as np
import random 

class Genome:
    def __init__(self, id, n_inputs, n_outputs, testmode=False, link_mutr = 0.2, node_mutr = 0.2):
        self.genome_id = id
        self.n_inputs = n_inputs
        self.n_outputs = n_outputs
        self.testmode = testmode
        self.nodes = self.create_nodes()
        self.connections: list[Connection] = self.create_initial_connections()
        self.link_mr = link_mutr
        self.node_mr = node_mutr
        
    def create_nodes(self) -> list:
        nodes = []
        for i in range(-1, -self.n_inputs -1, -1):
            nodes.append(Node(i, NodeType.Input_Sensor))
        nodes.append(Node(nodes[-1].id -1, NodeType.Bias))
        for i in range(self.n_outputs):
            nodes.append(Node(i, NodeType.Output))
        return nodes
    
    def add_connection(self, node_input, node_output):
        newConnection = Connection(node_input, node_output)
        newConnectionReverse = Connection(node_output, node_input)
        #Avoid recurrent connections and duplicates
        if newConnection not in self.connections and newConnectionReverse not in self.connections:
            self.connections.append(Connection(node_input, node_output))

    def nodes_to_dict(self):
        return {obj.id: obj for obj in self.nodes}
    
    def create_initial_connections(self) -> list:
        connections = []
        input_nodes = [node for node in self.nodes if helpers.is_input(node)]
        output_nodes = [node for node in self.nodes if node.nodeType == NodeType.Output]
        for i in input_nodes:
            for j in output_nodes:
                if self.testmode:
                    connections.append(Connection(i.id, j.id, 0.5))
                else:
                    connections.append(Connection(i.id, j.id))
        return connections

    def mutate_connections(self):
        if np.random.uniform(0, 1) <= self.link_mr:
            input_nodes = [node for node in self.nodes if node.nodeType != NodeType.Output] # bias, input, hidden
            output_nodes = [node for node in self.nodes if helpers.is_hidden_or_output(node)] # hidden, output
            while True:
                input_node = random.choice(input_nodes)
                output_node = random.choice(output_nodes)
                if input_node.id == output_node.id:
                    continue
                self.add_connection(input_node.id, output_node.id)                
                break
            
    def mutate_nodes(self):
        if np.random.uniform(0, 1) <= self.node_mr:
            connection_to_break = random.choice(helpers.get_enabled_connections(self.connections))
            connection_to_break.enabled = False
            input_id = connection_to_break.input
            output_id = connection_to_break.output
            new_node = Node(max(self.nodes_to_dict().keys()) + 1, NodeType.Hidden)
            self.nodes.append(new_node)
            self.add_connection(input_id, new_node.id)
            self.add_connection(new_node.id, output_id)
                
    def mutate(self):
        self.mutate_connections()
        self.mutate_nodes()

            
    def visualize(self, show_weights=False):
        # Create a directed graph, add nodes and also the weights of the connections
        G = nx.DiGraph()
        for node in self.nodes:
            G.add_node(node.id)
        for connection in helpers.get_enabled_connections(self.connections):
            G.add_edge(connection.input, connection.output, weight=round(connection.weight, 2))
        # Create a layout for the graph
        pos = nx.circular_layout(G)
        # Draw the nodes
        nx.draw_networkx_nodes(G, pos, node_size=250, node_color='#A0CBE2')
        # Draw the edges
        nx.draw_networkx_edges(G, pos, width=1)
        # Draw the labels
        nx.draw_networkx_labels(G, pos, font_size=14, font_family='sans-serif')
        # Draw the weights
        if show_weights:
            edge_labels = nx.get_edge_attributes(G, 'weight')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    
    def __str__(self) -> str:
        print("===== Nodes: =====")
        for node in self.nodes:
            print(node)
        print("===== Connections: =====")
        for connection in self.connections:
            print(connection)
        return ""

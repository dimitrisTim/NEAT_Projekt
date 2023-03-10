import utils.helpers as helpers
from node import Node, NodeType
from connection import Connection, create_connection
import networkx as nx
import numpy as np
import random


class Genome:
    def __init__(self, id, n_inputs, n_outputs, init_connections:bool = True, testmode=False, link_mutr = 0.2, node_mutr = 0.2):
        self.genome_id = id
        self.n_inputs = n_inputs
        self.n_outputs = n_outputs
        self.testmode = testmode
        self.nodes = self.create_nodes()
        self.connections: list[Connection] = self.create_initial_connections() if init_connections else []
        self.link_mr = link_mutr
        self.node_mr = node_mutr
        self.n_hidden_nodes = 0
        self.fitness = float('-inf')
        self.c1 = 1
        self.c2 = 1
        self.c3 = 0.4
        
    def create_nodes(self) -> list:
        nodes = []
        for i in range(-1, -self.n_inputs -1, -1):
            nodes.append(Node(i, NodeType.INPUT_SENSOR))
        nodes.append(Node(nodes[-1].id -1, NodeType.BIAS))
        for i in range(self.n_outputs):
            nodes.append(Node(i, NodeType.OUTPUT))
        return nodes
    
    def add_connection(self, node_input, node_output):
        newConnection = create_connection(node_input, node_output)
        newConnectionReverse = Connection(node_output, node_input, innovation=newConnection.innovation)
        #Avoid recurrent connections and duplicates
        if newConnection not in self.connections and newConnectionReverse not in self.connections:
            self.connections.append(newConnection)

    def nodes_to_dict(self):
        return {obj.id: obj for obj in self.nodes}
    
    def create_initial_connections(self) -> list:
        connections = []
        input_nodes = [node for node in self.nodes if helpers.is_input(node)]
        output_nodes = [node for node in self.nodes if node.nodeType == NodeType.OUTPUT]
        for i in input_nodes:
            for j in output_nodes:
                if self.testmode:
                    connections.append(Connection(i.id, j.id, 0.5))
                else:
                    connections.append(Connection(i.id, j.id))
        return connections

    def mutate_connections(self):
        if np.random.uniform(0, 1) <= self.link_mr:
            input_nodes = [node for node in self.nodes if node.nodeType != NodeType.OUTPUT] # bias, input, hidden
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
            new_node = Node(max(self.nodes_to_dict().keys()) + 1, NodeType.HIDDEN)
            self.nodes.append(new_node)
            self.add_connection(input_id, new_node.id)
            self.add_connection(new_node.id, output_id)
            self.n_hidden_nodes += 1
                
    def mutate(self):
        self.mutate_connections()
        self.mutate_nodes()

            
    def visualize(self, show_weights=False, show_node_values = False, show_innovations=False):
        G = nx.DiGraph()
        for node in self.nodes:
            G.add_node(node.id, value=round(node.value, 2))
        for connection in helpers.get_enabled_connections(self.connections):
            G.add_edge(connection.input, connection.output, weight=round(connection.weight, 2), innovation=connection.innovation)
        pos = nx.circular_layout(G)
        nx.draw_networkx_nodes(G, pos, node_size=250, node_color='#A0CBE2')
        nx.draw_networkx_edges(G, pos, width=1)
        #nx.draw_networkx_labels(G, pos, font_size=14, font_family='sans-serif')
        if show_node_values:
            node_labels = nx.get_node_attributes(G, 'value')
            nx.draw_networkx_nodes(G, pos, node_size=400, node_color='#A0CBE2')
            nx.draw_networkx_labels(G, pos, labels=node_labels)
        else:
            node_labels = {node: node for node in G.nodes()}
            nx.draw_networkx_labels(G, pos, labels=node_labels)
        if show_weights:
            edge_labels = nx.get_edge_attributes(G, 'weight')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        if show_innovations:
            edge_labels = nx.get_edge_attributes(G, 'innovation')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels) 
        
        
    def __str__(self) -> str:
        print("===== Nodes: =====")
        for node in self.nodes:
            print(node)
        print("===== Connections: =====")
        for connection in self.connections:
            print(connection)
        return ""



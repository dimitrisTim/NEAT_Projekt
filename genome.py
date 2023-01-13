from node import Node, NodeType
from connection import Connection
import networkx as nx

class Genome:
    def __init__(self, id, n_inputs, n_outputs):
        self.genome_id = id
        self.n_inputs = n_inputs
        self.n_outputs = n_outputs
        self.nodes = self.create_nodes()
        self.connections = self.create_connections()
        
    def create_nodes(self) -> list:
        nodes = []
        for i in range(-1, -self.n_inputs -1, -1):
            nodes.append(Node(i, NodeType.Input_Sensor))
        nodes.append(Node(nodes[-1].id -1, NodeType.Bias))
        for i in range(self.n_outputs):
            nodes.append(Node(i, NodeType.Output))
        return nodes
    
    def create_connections(self) -> list:
        connections = []
        input_nodes = [node for node in self.nodes if node.nodeType == NodeType.Input_Sensor or node.nodeType == NodeType.Bias]
        output_nodes = [node for node in self.nodes if node.nodeType == NodeType.Output]
        for i in input_nodes:
            for j in output_nodes:
                connections.append(Connection(i.id, j.id))
        return connections
    
    def visualize(self, show_weights=False):
        # Create a directed graph, add nodes and also the weights of the connections
        G = nx.DiGraph()
        for node in self.nodes:
            G.add_node(node.id)
        for connection in self.connections:
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

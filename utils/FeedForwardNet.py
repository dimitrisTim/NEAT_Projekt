from genome import Genome, Node, NodeType
import unittest    
import math
from connection import Connection

class FFN:    
    def __init__(self, genome: Genome, input_values: list[float]):
        self.genome = genome
        self.input_values = input_values
        self.nodes_dict = self.genome.nodes_to_dict()
        
    def is_input(self, node: Node):
        return node.nodeType == NodeType.Input_Sensor or node.nodeType == NodeType.Bias
    
    def sigmoid(self, x):
        return 1 / (1 + math.exp(-4.9 * x))    
        
    def forward(self):
        sorted_connections = sorted(self.genome.connections, key=lambda x: x.input, reverse=True)
        input_nodes = [node for node in self.genome.nodes if self.is_input(node)]
        output_nodes = [node for node in self.genome.nodes if node.nodeType == NodeType.Output]
        for input_node, input_value in zip(input_nodes, self.input_values):
            input_node.value = input_value                                     
        input_node_connections = [connection for connection in sorted_connections 
                                  if (self.is_input(self.nodes_dict[connection.input])
                                  and connection.enabled)]
        
        temp_outputs, sorted_connections = self.calculate_connection(input_node_connections, sorted_connections)
        
        while(len(temp_outputs) > 0):
            for temp_output in temp_outputs:
                temp_as_input_conn = [connection for connection in sorted_connections
                                if connection.input == temp_output.id                             
                                and connection.enabled]
                temp_as_output_conn = [connection for connection in sorted_connections
                                if connection.output == temp_output.id                             
                                and connection.enabled]
                if len(temp_as_output_conn) > 0:
                    continue
                if len(temp_as_output_conn) or len(temp_as_input_conn) == 0:
                    temp_output.value = self.sigmoid(temp_output.value)
                if len(temp_as_input_conn) == 0 and len(temp_as_output_conn) == 0:
                    temp_outputs.remove(temp_output)
                if len(temp_as_input_conn) > 0:
                    new_temp_outputs, sorted_connections = self.calculate_connection(temp_as_input_conn, sorted_connections)
                    temp_outputs.extend(new_temp_outputs)
                    temp_outputs.remove(temp_output)
                
    
    def calculate_connection(self, connections: list[Connection], rest_connections: list[Connection]):
        temp_outputs = []
        for connection in connections:
            input_node: Node = self.nodes_dict[connection.input]
            output_node: Node = self.nodes_dict[connection.output]
            temp_outputs.append(output_node)
            output_node.value += input_node.value * connection.weight
            rest_connections.remove(connection)
        return temp_outputs, rest_connections    
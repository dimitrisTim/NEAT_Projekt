from genome import Genome, Node, NodeType
import unittest    
import math

class FFN:    
    def __init__(self, genome: Genome, input_values: list[float]):
        self.genome = genome
        self.input_values = input_values
        
    def is_input(self, node: Node):
        return node.nodeType == NodeType.Input_Sensor or node.nodeType == NodeType.Bias
    
    def sigmoid(self, x):
        return 1 / (1 + math.exp(-4.9 * x))
        
    def forward(self):
        sorted_connections = sorted(self.genome.connections, key=lambda x: x.input, reverse=True)
        inputs = [node for node in self.genome.nodes if self.is_input(node)]
        outputs = [node for node in self.genome.nodes if node.nodeType == NodeType.Output]
        for input, input_value in zip(inputs, self.input_values):
            input.value = input_value        
        for connection in sorted_connections:
            nodes = self.genome.nodes_to_dict()
            input_node: Node = nodes[connection.input]
            output_node: Node = nodes[connection.output]
            output_node.value += input_node.value * connection.weight
        for output in outputs:
            output.value = self.sigmoid(output.value)
from node import Node, NodeType
from connection import Connection

def is_input(node: Node):
        return node.nodeType == NodeType.Input_Sensor or node.nodeType == NodeType.Bias
    
def is_hidden_or_output(node: Node):
        return node.nodeType == NodeType.Output or node.nodeType == NodeType.Hidden
    
def get_enabled_connections(connections: list[Connection]):
    return [connection for connection in connections if connection.enabled]
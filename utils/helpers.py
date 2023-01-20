from node import Node, NodeType
from connection import Connection

def is_input(node: Node):
        return node.nodeType == NodeType.INPUT_SENSOR or node.nodeType == NodeType.BIAS
    
def is_hidden_or_output(node: Node):
        return node.nodeType == NodeType.OUTPUT or node.nodeType == NodeType.HIDDEN
    
def get_enabled_connections(connections: list[Connection]):
    return [connection for connection in connections if connection.enabled]
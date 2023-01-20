from enum import Enum

class NodeType(Enum):
    INPUT_SENSOR  = 1
    OUTPUT = 2
    HIDDEN = 3
    BIAS   = 4


class Node:    
    def __init__(self, id, nodeType: NodeType):
        self.id = id
        self.nodeType = nodeType
        self.value = 1 if nodeType == NodeType.BIAS else 0
        
    def __str__(self):
        return "Node: " + str(self.id) + '\n' +  "Type: " + str(self.nodeType) + '\n'
from enum import Enum

class NodeType(Enum):
    Input_Sensor  = 1
    Output = 2
    Hidden = 3
    Bias   = 4


class Node:    
    def __init__(self, id, nodeType: NodeType):
        self.id = id
        self.nodeType = nodeType
        self.value = 1 if nodeType == NodeType.Bias else 0
        
    def __str__(self):
        return "Node: " + str(self.id) + '\n' +  "Type: " + str(self.nodeType) + '\n'
import numpy as np
import utils.innovation_generator as ig

class Connection:
    def __init__(self, input, output, weight=np.random.uniform(-1, 1), innovation=ig.get_new_innovation_number()):
        self.input = input
        self.output = output
        self.weight = weight
        self.innovation = innovation
        self.enabled = True
        
    def __str__(self):
        return "Innovation: " + str(self.innovation) \
        + '\n' + "Input: " + str(self.input) \
        + '\n' + "Output: " + str(self.output) \
        + '\n' + "Weight: " + str(self.weight) \
        + '\n' + "Enabled: " + str(self.enabled) + '\n'
        
    def __eq__(self, other):
        if isinstance(other, self.__class__): 
            return self.input == other.input and self.output == other.output    
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)
    
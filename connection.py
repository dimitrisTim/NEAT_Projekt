import numpy as np
import utils.innovation_generator as ig

class Connection:
    def __init__(self, input, output):
        self.input = input
        self.output = output
        self.weight = np.random.uniform(-1, 1)
        self.innovation = ig.get_new_innovation_number()
        self.enabled = True
        
    def __str__(self):
        return "Innovation: " + str(self.innovation) \
        + '\n' + "Input: " + str(self.input) \
        + '\n' + "Output: " + str(self.output) \
        + '\n' + "Weight: " + str(self.weight) \
        + '\n' + "Enabled: " + str(self.enabled) + '\n'
    
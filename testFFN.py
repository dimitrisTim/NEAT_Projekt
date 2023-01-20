import unittest
from genome import Genome, Node, NodeType
from utils.FeedForwardNet import FFN

class TestFFN(unittest.TestCase):
    def test_forward(self):
        # Create a dummy genome and input values
        genome = Genome(0, 3, 1, testmode=True)
        input_values = [1, 2, 3]

        # Create an instance of the FFN class
        ffn = FFN(genome, input_values)

        # Test that the input values are correctly set
        ffn.forward()
        for i, node in enumerate(genome.nodes):
            if ffn.is_input(node):
                if node.nodeType == NodeType.BIAS:
                    self.assertEqual(node.value, 1)
                else:    
                    self.assertEqual(node.value, input_values[i])
                    
        output_values = [0.999]
        for node in genome.nodes:
            if node.nodeType == NodeType.OUTPUT:
                self.assertAlmostEqual(node.value, output_values[0], 2)

if __name__ == '__main__':
    unittest.main()

import unittest
import networkx as nx
from ullman.ullman_algorithm import UllmanAlgorithm


class TestUllmanAlgorithm(unittest.TestCase):
    
    def test_subgraph1(self):
        g1 = nx.Graph()
        g1.add_edges_from([(0, 1), (1, 2)])

        g2 = nx.Graph()
        g2.add_edges_from([(0, 1), (1, 2), (2, 3)])

        self.assertTrue(UllmanAlgorithm(g1, g2).is_subgraph_isomorphic())
    
    def test_subgraph2(self):
        g1 = nx.Graph()
        g1.add_edges_from([(0, 1), (1, 2)])
        
        g2 = nx.Graph()
        g2.add_edges_from([(3, 4), (4, 5), (5, 6)])

        self.assertTrue(UllmanAlgorithm(g1, g2).is_subgraph_isomorphic())
    
    def test_subgraph3(self):
        g1 = nx.Graph()
        g1.add_edges_from([(0, 1), (0, 2), (1, 2)])
        
        g2 = nx.Graph()
        g2.add_edges_from([(3, 4)])

        self.assertFalse(UllmanAlgorithm(g1, g2).is_subgraph_isomorphic())

if __name__ == '__main__':
    unittest.main()
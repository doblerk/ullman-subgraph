import unittest
import networkx as nx
from ullman import Ullman


class TestUllmanAlgorithm(unittest.TestCase):
    def test_subgraph(self):
        g1 = nx.Graph()
        g1.add_edges_from([(0, 1), (1, 2)])

        g2 = nx.Graph()
        g2.add_edges_from([(0, 1), (1, 2), (2, 3)])

        A1 = nx.adjacency_matrix(g1).todense()
        A2 = nx.adjacency_matrix(g2).todense()

        self.assertTrue(Ullman(g1, g2, A1, A2))

if __name__ == '__main__':
    unittest.main()
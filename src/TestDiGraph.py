from unittest import TestCase
from DiGraph import *


class TestDiGraph(TestCase):
    def test_v_size(self):
        g = DiGraph()
        self.assertEqual(g.v_size(), 0)
        for i in range(10):
            g.add_node(i)
        self.assertEqual(g.v_size(), 10)

    def test_e_size(self):
        g = DiGraph()
        self.assertEqual(g.e_size(), 0)

        for i in range(10):
            g.add_node(i)
        for i in range(10):
            g.add_edge(i, i - 2, 2)
        print(g)
        self.assertEqual(g.e_size(), 8)

    def test_get_all_v(self):
        g = self.simple_graph_generate()
        all_v = g.get_all_v()
        for i in range(10):
            self.assertTrue(i in all_v)

    def test_all_in_edges_of_node(self):
        g = self.simple_graph_generate()
        all_in_e = g.all_in_edges_of_node(6)
        self.assertTrue(4 in all_in_e)
        self.assertTrue(5 in all_in_e)

    def test_all_out_edges_of_node(self):
        g = self.simple_graph_generate()
        all_out_e = g.all_out_edges_of_node(1)
        self.assertTrue(9 in all_out_e)
        self.assertTrue(2 in all_out_e)

    def test_get_mc(self):
        g = DiGraph()
        modeCount = g.mode_count
        for i in range(10):
            g.add_node(i)
        self.assertNotEqual(g.mode_count, modeCount)

    def test_add_edge(self):
        g = DiGraph()
        edgeSize = g.edge_size
        for i in range(10):
            g.add_node(i)

        for i in range(10):
            g.add_edge(i, i - 2, -i)
        # Check Un positive numbers
        self.assertEqual(g.edge_size, edgeSize)

        for i in range(10):
            g.add_edge(i, i - 2, i)
            # Check Un positive numbers
        self.assertNotEqual(g.edge_size, edgeSize)
        edgeSize = g.edge_size

        for i in range(10):
            g.add_edge(i, i - 2, i)
        # self.assertNotEqual(g.edge_size, edgeSize)

    def test_add_node(self):
        g = DiGraph()

        for i in range(10):
            g.add_node(i)

        self.assertEqual(len(g.nodes), 10)

        for i in range(10):
            g.add_node(i)

        self.assertEqual(len(g.nodes), 10)

    def test_remove_node(self):
        g = self.simple_graph_generate()
        edgeSize = g.edge_size
        modeCount = g.mode_count
        removed_edges = len(g.all_in_edges_of_node(1)) + len(g.all_out_edges_of_node(1))
        g.remove_node(1)
        self.assertEqual(edgeSize - removed_edges, g.edge_size)
        self.assertNotEqual(g.mode_count, modeCount)
        self.assertEqual(9, g.v_size())

    def test_remove_edge(self):
        g = self.simple_graph_generate()
        edges_size = g.e_size()
        self.assertFalse(g.remove_edge(0, 0))
        self.assertEqual(edges_size, g.e_size())

        self.assertTrue(g.remove_edge(3, 7))
        self.assertEqual(edges_size - 1, g.e_size())

    @staticmethod
    def simple_graph_generate():
        """
        DiGraph: |V| = 10	|E| = 16
        {0: (0), 1: (1), 2: (2), 3: (3), 4: (4), 5: (5), 6: (6), 7: (7), 8: (8), 9: (9)}
        Edge Data:
        (1) -> {9: 0.5, 2: 0.5}
        (2) -> {8: 1.0, 3: 1.0}
        (3) -> {7: 1.5, 4: 1.5}
        (4) -> {6: 2.0, 5: 2.0}
        (5) -> {6: 2.5}
        (6) -> {4: 3.0, 7: 3.0}
        (7) -> {3: 3.5, 8: 3.5}
        (8) -> {2: 4.0, 9: 4.0}
        (9) -> {1: 4.5}
        """
        g = DiGraph()
        for i in range(10):
            g.add_node(i)

        for i in range(10):
            g.add_edge(i, 10 - i, i * 0.5)
            g.add_edge(i, i + 1, i * 0.5)
        return g

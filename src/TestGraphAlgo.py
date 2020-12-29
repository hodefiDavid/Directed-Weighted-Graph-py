from unittest import TestCase
from GraphAlgo import *
from TestDiGraph import TestDiGraph as tdg


class TestGraphAlgo(TestCase):
    def test_get_graph(self):
        self.fail()

    def test_load_and_save_from_json(self):
        file_path = '../data/A5'
        test_path = "../data/test_save.json"
        ga = GraphAlgo()
        self.assertTrue(ga.load_from_json(file_path))
        g = ga.get_graph()
        ga.save_to_json(test_path)
        ga1 = GraphAlgo()
        self.assertTrue(ga1.load_from_json(test_path))
        g1 = ga1.get_graph()
        self.assertEqual(g, g1)

    def test_shortest_path(self):
        g = tdg.simple_graph_generate()
        ga = GraphAlgo(g)  # 1-7 --3
        expected_lst = [g.nodes[1], g.nodes[2], g.nodes[3], g.nodes[7]]
        self.assertEqual((3.0, expected_lst), ga.shortest_path(1, 7))
        self.assertEqual((-1, None), ga.shortest_path(1, 88))
        expected_lst = [g.nodes[3], g.nodes[7], g.nodes[8], g.nodes[9]]
        self.assertEqual((9, expected_lst), ga.shortest_path(3, 9))

    def test_connected_component(self):
        g = tdg.simple_graph_generate()
        ga = GraphAlgo(g)
        lst = [g.nodes[0]]
        self.assertEqual(lst, ga.connected_component(0))

        lst = [n for n in g.nodes.values() if n.id != 0]
        self.assertEqual(lst, ga.connected_component(1))

        lst.remove(g.nodes[6])
        lst.remove(g.nodes[2])
        lst.remove(g.nodes[4])
        lst.remove(g.nodes[8])
        g.remove_node(8)

        self.assertEqual(lst, ga.connected_component(1))

        lst.remove(g.nodes[5])
        lst.remove(g.nodes[7])
        lst.remove(g.nodes[3])
        g.remove_node(2)
        self.assertEqual(lst, ga.connected_component(1))

    def test_connected_components(self):
        g = tdg.simple_graph_generate()
        ga = GraphAlgo(g)
        lst = [[g.nodes[0]], [n for n in g.nodes.values() if n.id != 0]]
        lst1 = ga.connected_components()

        self.assertEqual(lst, lst1)
        g.remove_node(2)
        lst1 = ga.connected_components()
        self.assertNotEqual(lst, lst1)

        g.add_node(2)
        g.add_edge(2, 3, 4.3)
        g.add_edge(2, 8, 2.3)
        g.add_edge(1, 2, 2.3)
        g.add_edge(8, 2, 2.3)
        lst1 = ga.connected_components()

        self.assertNotEqual(lst, lst1)

    def test_plot_graph(self):
        ga = GraphAlgo()
        ga.load_from_json('../data/A4')
        g = tdg.simple_graph_generate()
        ga.graph = g
        ga.plot_graph()

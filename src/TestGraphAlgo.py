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
        self.fail()

    def test_connected_component(self):
        self.fail()

    def test_connected_components(self):
        self.fail()

    def test_plot_graph(self):
        self.fail()

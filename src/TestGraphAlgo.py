import random
import unittest
from random import randint, uniform
from unittest import TestCase

from GraphAlgo import *
from TestDiGraph import TestDiGraph as tdg

import time


class TestGraphAlgo(TestCase):
    def test_get_graph(self):
        g = tdg.simple_graph_generate()
        ga = GraphAlgo(g)
        self.assertEqual(g, ga.get_graph())

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
        ga = GraphAlgo(g)
        expected_lst = [1, 2, 3, 7]
        self.assertEqual((3.0, expected_lst), ga.shortest_path(1, 7))
        self.assertEqual((-1, []), ga.shortest_path(1, 88))
        expected_lst = [3, 7, 8, 9]
        self.assertEqual((9, expected_lst), ga.shortest_path(3, 9))

    def test_connected_component(self):
        g = tdg.simple_graph_generate()
        ga = GraphAlgo(g)
        lst = [0]
        self.assertEqual(lst, ga.connected_component(0))

        lst = [n for n in g.nodes.keys() if n != 0]
        self.assertEqual(lst, ga.connected_component(1))

        lst.remove(6)
        lst.remove(2)
        lst.remove(4)
        lst.remove(8)
        g.remove_node(8)
        lst.remove(5)
        lst.remove(7)
        lst.remove(3)
        g.remove_node(2)
        self.assertEqual(lst, ga.connected_component(1))

    def test_connected_components(self):
        g = tdg.simple_graph_generate()
        ga = GraphAlgo(g)
        lst = [[0], [n for n in g.nodes.keys() if n != 0]]
        lst1 = ga.connected_components()

        self.assertEqual(set(lst[0]), set(lst1[0]))
        g.remove_node(2)
        lst1 = ga.connected_components()
        self.assertNotEqual(lst, lst1)

        g.add_node(2)
        g.add_edge(2, 3, 4.3)
        g.add_edge(2, 8, 2.3)
        g.add_edge(1, 2, 2.3)
        g.add_edge(8, 2, 2.3)
        lst1 = ga.connected_components()
        for i in lst:
            flag = False
            for j in lst1:
                if GraphAlgo.list_equals(i, j):
                    flag = True
            self.assertTrue(flag)

    @unittest.skip
    def test_plot_graph(self):
        ga = GraphAlgo()
        ga.load_from_json('../data/A2')
        g = tdg.simple_graph_generate()
        # ga.graph = g
        ga.plot_graph()

    def test_transpose_g(self):
        # building a simple graph for testing
        g = DiGraph()
        for i in range(10):
            g.add_node(i)
            g.add_edge(i, i - 1, 1+i)

        ga = GraphAlgo(g)
        dist9_0 = ga.shortest_path(9, 0)
        self.assertEqual(dist9_0[0], 54)

        gt = ga.transpose_graph()
        gta = GraphAlgo(gt)
        # gta_dist9_0 = gta.shortest_path(9, 0)
        # self.assertEqual(gta_dist9_0[0], -1)
        # print(gta_dist9_0[0])
        gta_dist0_9 = gta.shortest_path(0, 9)
        self.assertEqual(dist9_0[0], gta_dist0_9[0])


        self.assertEqual(g.all_out_edges_of_node(1)[0], gt.all_out_edges_of_node(0)[1])

        # print(gta_dist9_0[0])
        ga.plot_graph()
        # print(gta_dist9_0[0])

        gta.plot_graph()

    def test_big_path(self):
        random.seed(1)
        v = 10000
        path_size = 1000
        g = DiGraph()
        for i in range(v):
            g.add_node(i)
        path = {randint(0, v - 1) for _ in range(path_size)}
        expected_weight = 0
        dest = src = prev_n = path.pop()
        expected_path = [src]
        while len(path) > 0:
            next_n = path.pop()
            expected_path.append(next_n)
            weight = uniform(0, 1)
            g.add_edge(prev_n, next_n, weight)
            expected_weight += weight
            dest = prev_n = next_n
        while g.e_size() < v * 10:
            g.add_edge(randint(0, v), randint(0, v), expected_weight * uniform(1, 3))
        ga = GraphAlgo(g)
        ga_shortest_path = ga.shortest_path(src, dest)
        self.assertEqual(expected_path, ga_shortest_path[1])
        self.assertEqual(expected_weight, ga_shortest_path[0])

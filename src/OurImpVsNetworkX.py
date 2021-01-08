import threading
import time
import unittest
import networkx as nx
import GuiNetworkX as gnx
from GraphAlgo import *
import random  # fjgkgbbbbbbbbbbbbbbbb


class MyTestCase(unittest.TestCase):
    """
    This unittest class, contains set of comparison test,
    between our implementation of directed weighted graph, to networkx module implementation.
    The tests checks:
    1. Comparing results- to check correctness.
    2. Comparison of running times - to test efficiency.
    """

    def init(self, data_file_js: str):
        """
        init networkX graph, and our DiGraph from the given json file.
        :param data_file_js: path of JSON file
        """
        self.data_file = data_file_js
        self.ga = GraphAlgo()
        self.ga.load_from_json(data_file_js)
        self.load_nx_from_json(data_file_js)

    def compare_times(self, nxf, gf, args=()):
        """
        This method is aid method for comparing times between the various functions.
        :param nxf: networkx function.
        :param gf: our function.
        :param args: arguments.
        """
        start_time = time.time()
        nx_res = nxf(self.gx, *args)
        end_time = time.time()
        nx_time = end_time - start_time
        print('NX:', nxf.__name__ + str(args), ':', nx_time)

        start_time = time.time()
        g_res = gf(*args)
        end_time = time.time()
        g_time = end_time - start_time
        print('Our:', gf.__name__ + str(args), ':', g_time)

        print('Faster:', 'NX' if nx_time < g_time else 'Our')
        return nx_res, g_res

    def test_built_times(self):
        """
        This test compare building of big graph, and measures running times.
        """
        start_time = time.time()
        graph = GraphAlgo()
        graph.load_from_json("../data/10kG.json")
        end_time = time.time()
        print('Our:', "test_built_times" + "(10kG.json)", ':', end_time - start_time)

        start_time = time.time()
        self.load_nx_from_json("../data/10kG.json")
        end_time = time.time()
        print('NX:', "test_built_times" + "(10kG.json)", ':', end_time - start_time)

    def test_save(self):
        """
        This test compare saving of big graph to Json file, and measures running times.
        """
        self.init("../data/10kG.json")
        start_time = time.time()
        dict_jx = nx.node_link_data(self.gx, dict(source='src', target='dest', name='id', key='key', link='links'))
        with open('../data/gX_saveTestTime.json', 'w') as f:
            json.dump(dict_jx, f)
        end_time = time.time()
        print('NX:', "save_test_time" + "(10kG.json)", ':', end_time - start_time)

        start_time = time.time()
        self.ga.save_to_json("../data/g_saveTestTime.json")
        end_time = time.time()
        print('Our:', "save_test_time" + "(10kG.json)", ':', end_time - start_time)

    def test_shortest_path(self):
        """
        This test compare calculation of the shortest path between 2 nodes
        on big graph, compares the results and measures running times.
        """
        self.init('../data/Graphs_no_pos/G_30000_240000_0.json')
        # self.init('../data/100kG.json')

        # nx_res, g_res = self.compare_times(nx.dijkstra_path_length, self.ga.shortest_path, (0, 100))
        # self.assertEqual(g_res[0], nx_res)
        # nx_res, g_res = self.compare_times(nx.dijkstra_path_length, self.ga.shortest_path, (0, 50000))
        # self.assertEqual(g_res[0], nx_res)
        # nx_res, g_res = self.compare_times(nx.dijkstra_path_length, self.ga.shortest_path, (0, 99999))
        # self.assertEqual(g_res[0], nx_res)

        # nx_res, g_res = self.compare_times(nx.dijkstra_path_length, self.ga.shortest_path, (10, 1))
        # self.assertEqual(g_res[0], nx_res)
        nx_res, g_res = self.compare_times(nx.dijkstra_path_length, self.ga.shortest_path, (0, 10))
        self.assertEqual(g_res[0], nx_res)
        # nx_res, g_res = self.compare_times(nx.dijkstra_path_length, self.ga.shortest_path, (0, 99999))
        # self.assertEqual(g_res[0], nx_res)

    def test_connected_component(self):
        """
        This test compare calculation of the connected component of node,
        compares the results and measures running times.
        """
        self.init('../data/A5')
        # self.init('../data/Graphs_no_pos/G_30000_240000_0.json')

        nx_res, g_res = self.compare_times(self.get_strongly_cc, self.ga.connected_component, (1,))
        self.assertEqual(nx_res, set(g_res))
        print(g_res)
        self.init('../data/A5_edited')
        nx_res, g_res = self.compare_times(self.get_strongly_cc, self.ga.connected_component, (1,))
        self.assertEqual(nx_res, set(g_res))
        print(g_res)

    def test_connected_components(self):
        """
        This test compare calculation of the connected components of given graph,
        compares the results and measures running times.
        """
        # self.init('../data/A5')
        self.init('../data/Graphs_no_pos/G_10000_80000_0.json.')

        nx_res, g_res = self.compare_times(nx.strongly_connected_components, self.ga.connected_components)
        print(g_res)
        for i, s in enumerate(nx_res):
            self.assertEqual(s, set(g_res[i]))

        self.init('../data/A5_edited')
        nx_res, g_res = self.compare_times(nx.strongly_connected_components, self.ga.connected_components)
        print(g_res)

        for i, s in enumerate(nx_res):
            self.assertEqual(s, set(g_res[i]))

    @staticmethod
    def get_strongly_cc(gx, node):
        """
        get strongly connected component of node
        taken from:
        https://stackoverflow.com/questions/47283612/networkx-node-connected-component-not-implemented-for-directed-type
        """
        for cc in nx.strongly_connected_components(gx):
            if node in cc:
                return cc
        else:
            return set()

    @unittest.skip
    def test_plot(self):
        """
        Shows our plot graph, and networkx plot graph together.
        """
        self.init('../data/A5_edited')
        loc_w = self.load_nx_from_json(self.data_file)
        t1 = threading.Thread(target=gnx.plot, args=(self.gx, loc_w))
        t2 = threading.Thread(target=self.ga.plot_graph)
        t1.start()
        t2.start()

    def load_nx_from_json(self, data_file_js):
        """
        Loads and build nx.DiGraph, from json file.
        Init self.gx to be this graph.
        :param data_file_js: path of json file.
        """
        with open(data_file_js, 'r') as file:
            data = json.load(file)
            self.gx = nx.DiGraph()
            loc_w = {}
            for i in data['Nodes']:
                if 'pos' in i.keys():
                    str_lst = i['pos'].split(',')
                    pos = (float(str_lst[0]), float(str_lst[1]))
                    loc_w[i['id']] = pos
                self.gx.add_node(i['id'])
            for i in data['Edges']:
                self.gx.add_edge(i['src'], i['dest'], weight=i['w'])
        return loc_w

    def test_big_path_mil(self):
        # nx1 = nx.DiGraph()
        g = DiGraph()
        for i in range(1000000):
            # nx1.add_node(i)
            g.add_node(i)
            g.add_edge(i - 1, i, random.randint(1, 25))

        # for i in range(500000):
        #     if i % 1500 == 0:
        #         for j in range(1700):
        # nx1.add_edge(i, i - j, lenght=2.3)
        # g.add_edge(i, i - j, 2.3)
        # g.add_edge(i - j, i, 2.3)

        print("end build")
        ga = GraphAlgo(g)
        ga.save_to_json("milll.json")

        # start_time = time.time()

        # time
        # ga = GraphAlgo(g)
        # print((nx.strongly_connected_components(nx1)))
        # for i in nx.strongly_connected_components(nx1):
        #     print(i)
        # print((ga.connected_components()))
        # end_time = time.time()
        # print(end_time - start_time)

        #
        # self.assertEqual(expected_path, ga_shortest_path[1])
        # self.assertEqual(expected_weight, ga_shortest_path[0])


if __name__ == '__main__':
    unittest.main()

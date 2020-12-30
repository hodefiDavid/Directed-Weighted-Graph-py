import datetime
import threading
import time
import unittest
from GraphAlgo import *
import networkx as nx
import GuiNetworkX as gnx


class MyTestCase(unittest.TestCase):

    def test_init(self, data_file_js):
        self.data_file = data_file_js
        self.ga = GraphAlgo()
        self.ga.load_from_json(data_file_js)
        self.load_nx_from_json(data_file_js)

    def compare_times(self, nxf, gf, args=()):
        start_time = time.time()
        nx_res = nxf(self.gx, *args)
        end_time = time.time()
        print('NX:', nxf.__name__ + str(args), ':', end_time - start_time)

        start_time = time.time()
        g_res = gf(*args)
        end_time = time.time()
        print('Our:', nxf.__name__ + str(args), ':', end_time - start_time)
        return nx_res, g_res

    def test_shortest_path(self):  # 0-> 8
        self.test_init('../data/1kG.json')
        nx_res, g_res = self.compare_times(nx.shortest_path, self.ga.shortest_path, (0, 11))
        self.assertEqual(g_res[1], nx_res)
        nx_res, g_res = self.compare_times(nx.shortest_path, self.ga.shortest_path, (0, 500))
        self.assertEqual(g_res[1], nx_res)
        nx_res, g_res = self.compare_times(nx.shortest_path, self.ga.shortest_path, (0, 999))
        self.assertEqual(g_res[1], nx_res)

        # for i in range(5):
        #     self.test_init('../data/A' + str(i))
        #     self.compare(nx.shortest_path, self.ga.shortest_path, (0, 10))
        #     if i > 3:
        #         self.compare(nx.shortest_path, self.ga.shortest_path, (0, 39))

    def test_connected_component(self):
        self.test_init('../data/A5')
        nx_res, g_res = self.compare_times(nx.strongly_connected_components, self.ga.connected_components)
        for i, s in enumerate(nx_res):
            self.assertEqual(s, set(g_res[i]))

        self.test_init('../data/A5_edited')
        nx_res, g_res = self.compare_times(nx.strongly_connected_components, self.ga.connected_components)
        for i, s in enumerate(nx_res):
            self.assertEqual(s, set(g_res[i]))

        # self.test_init('../data/1kG.json')
        # nx_res, g_res = self.compare_times(nx.strongly_connected_components, self.ga.connected_components)
        # for i, s in enumerate(nx_res):
        #     self.assertEqual(s, set(g_res[i]))

    def test_plot(self):
        self.test_init('../data/A5_edited')
        loc_w = self.load_nx_from_json(self.data_file)
        t1 = threading.Thread(target=gnx.plot, args=(self.gx, loc_w))
        t2 = threading.Thread(target=self.ga.plot_graph)
        t1.start()
        t2.start()

    def load_nx_from_json(self, data_file_js):
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
                self.gx.add_edge(i['src'], i['dest'])
        return loc_w


if __name__ == '__main__':
    unittest.main()

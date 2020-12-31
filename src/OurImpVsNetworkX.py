import threading
import time
import unittest
import networkx as nx
import GuiNetworkX as gnx
from GraphAlgo import *


class MyTestCase(unittest.TestCase):

    def init(self, data_file_js):
        self.data_file = data_file_js
        self.ga = GraphAlgo()
        self.ga.load_from_json(data_file_js)
        self.load_nx_from_json(data_file_js)

    def compare_times(self, nxf, gf, args=()):
        """
        This method is aid method for comparing times between the various functions.
        @param nxf: networkx function.
        @param gf: our function.
        @param args: arguments.
        """
        start_time = time.time()
        nx_res = nxf(self.gx, *args)
        end_time = time.time()
        print('NX:', nxf.__name__ + str(args), ':', end_time - start_time)

        start_time = time.time()
        g_res = gf(*args)
        end_time = time.time()
        print('Our:', gf.__name__ + str(args), ':', end_time - start_time)
        return nx_res, g_res

    def test_built_times(self):
        start_time = time.time()
        graphA = GraphAlgo()
        graphA.load_from_json("../data/10kG.json")
        end_time = time.time()
        print('Our:', "test_built_times" + "(10kG.json)", ':', end_time - start_time)

        start_time = time.time()
        self.load_nx_from_json("../data/10kG.json")
        end_time = time.time()
        print('NX:', "test_built_times" + "(10kG.json)", ':', end_time - start_time)

    def test_save(self):
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
        self.init('../data/1kG.json')
        nx_res, g_res = self.compare_times(nx.dijkstra_path, self.ga.shortest_path, (0, 11))
        self.assertEqual(g_res[1], nx_res)
        nx_res, g_res = self.compare_times(nx.dijkstra_path_length, self.ga.shortest_path, (0, 500))
        self.assertEqual(g_res[0], nx_res)
        nx_res, g_res = self.compare_times(nx.dijkstra_path_length, self.ga.shortest_path, (0, 999))
        self.assertEqual(g_res[0], nx_res)

    def test_connected_component(self):
        self.init('../data/A5')
        nx_res, g_res = self.compare_times(self.get_strongly_cc, self.ga.connected_component, (1,))
        self.assertEqual(nx_res, set(g_res))

        self.init('../data/A5_edited')
        nx_res, g_res = self.compare_times(self.get_strongly_cc, self.ga.connected_component, (1,))
        self.assertEqual(nx_res, set(g_res))

    def test_connected_components(self):
        self.init('../data/A5')
        nx_res, g_res = self.compare_times(nx.strongly_connected_components, self.ga.connected_components)
        for i, s in enumerate(nx_res):
            self.assertEqual(s, set(g_res[i]))

        self.init('../data/A5_edited')
        nx_res, g_res = self.compare_times(nx.strongly_connected_components, self.ga.connected_components)
        for i, s in enumerate(nx_res):
            self.assertEqual(s, set(g_res[i]))

    def get_strongly_cc(self, gx, node):
        """ get storngly connected component of node- taken from:
        https: // stackoverflow.com / questions / 47283612 / networkx - node - connected - component -
        not -implemented -for -directed - type"""
        for cc in nx.strongly_connected_components(gx):
            if node in cc:
                return cc
        else:
            return set()

    @unittest.skip
    def test_plot(self):
        self.init('../data/A5_edited')
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
                self.gx.add_edge(i['src'], i['dest'], weight=i['w'])
        return loc_w


if __name__ == '__main__':
    unittest.main()

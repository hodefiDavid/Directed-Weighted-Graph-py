import datetime
import time
import unittest
from GraphAlgo import *
import networkx as nx
import GuiNetworkX as gnx


class MyTestCase(unittest.TestCase):
    data_file_js = '../data/10kG.json'

    def test_init(self):
        self.ga = GraphAlgo()
        self.ga.load_from_json(MyTestCase.data_file_js)
        loc_w = self.load_nx_from_json()
        # gnx.plot(self.gx, loc_w)
        # self.ga.plot_graph()

    def test_shortest_path(self):
        self.test_init()
        start_time = time.time()
        y = nx.shortest_path(self.gx, 0, 8)
        print(y)
        end_time = time.time()
        print('shortest_path() NX:', end_time - start_time)
        start_time = time.time()
        y = self.ga.shortest_path(0, 8)
        print(y)
        end_time = time.time()
        print('shortest_path() Our:', end_time - start_time)


    def load_nx_from_json(self):
        with open(MyTestCase.data_file_js, 'r') as file:
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

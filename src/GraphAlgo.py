from heapq import heappush, heappop

from DiGraph import *
from GraphAlgoInterface import *
import json


class GraphAlgo(GraphAlgoInterface):

    def __init__(self, g: DiGraph = None):
        self.graph = g

    def get_graph(self) -> GraphInterface:
        return self.graph

    def load_from_json(self, file_name: str) -> bool:
        try:
            with open(file_name, 'r') as file:
                data = json.load(file)
                g = DiGraph()
                for i in data['Nodes']:
                    str_lst = i['pos'].split(',')
                    pos = (float(str_lst[0]), float(str_lst[1]))
                    g.add_node(i['id'], pos)
                for i in data['Edges']:
                    g.add_edge(i['src'], i['dest'], i['w'])
                self.graph = g
        except Exception as e:
            print(e)
            return False

        return True

    def save_to_json(self, file_name: str) -> bool:
        j = dict()
        j["Edges"] = list()
        j["Nodes"] = list()
        for i in self.graph.nodes.values():
            if i.position is None:
                pos = '0.0,0.0,0.0'
            else:
                pos = str(str(i.position[0]) + ',' + str(i.position[1]) + ',0.0')
            j["Nodes"].append({"pos": pos, "id": i.id})
            for key, weight in i.node_out.items():
                j["Edges"].append({"src": i.id, "w": weight, "dest": key})
        try:
            with open(file_name, 'w') as json_f:
                json.dump(j, json_f)
                return True
        except IOError:
            return False

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        if id1 not in self.graph.nodes.keys() or id2 not in self.graph.nodes.keys():
            return -1, None
        src = self.graph.nodes[id1]
        dest = self.graph.nodes[id2]

        if id1 == id2:
            return 0, [src]

        self.set_tag_dist(id1)
        if dest.tag == -1:
            return -1, []

        lst = []
        lst.insert(0, dest)
        curr = lst[0]

        while curr != src:
            for i, w in curr.node_in.items():
                n = self.graph.nodes[i]
                if n.tag + w == curr.tag:
                    lst.insert(0, n)
                    curr = lst[0]
                    break

        return dest.tag, lst

    def set_tag_dist(self, id1):
        p_queue = []
        self.init_tags()
        curr = self.graph.nodes[id1]
        curr.tag = 0
        heappush(p_queue, curr)
        while len(p_queue) > 0:
            curr = heappop(p_queue)
            for nodeIn_id, w in curr.node_out.items():
                n = self.graph.nodes[nodeIn_id]
                if n.tag == -1 or n.tag > curr.tag + w:
                    n.tag = curr.tag + w
                    heappush(p_queue, n)

    def init_tags(self):
        for i in self.graph.nodes.values():
            i.tag = -1

    def connected_component(self, id1: int) -> list:
        if id1 not in self.graph.nodes.keys():
            return None

        self.set_tag_dist(id1)
        lst = [n for n in self.graph.nodes.values() if n.tag != -1]
        for n in lst:
            if self.shortest_path(n.id, id1)[0] == -1:
                lst.remove(n)
        lst.sort(key=lambda x: x.id)
        return lst

    def connected_components(self) -> List[list]:
        lst = []
        for n in self.graph.nodes.values():
            temp = self.connected_component(n.id)
            flag = True
            for i in lst:
                if self.list_equals(i, temp):
                    flag = False
            if flag:
                lst.append(temp)
        return lst

    def plot_graph(self) -> None:
        pass

    @staticmethod
    def list_equals(lst1, lst2):
        for j in lst1:
            if j not in lst2:
                return False
        return True

import json
from heapq import heappush, heappop
from DiGraph import *
from GraphAlgoInterface import *
from Gui import Gui


class GraphAlgo(GraphAlgoInterface):
    """This class represents an algorithms class for the class Digraph."""

    def __init__(self, g: DiGraph = None):
        """
        Initialize the graph that this class work on.
        :param g: graph DiGraph
        """
        self.graph = g

    def get_graph(self) -> GraphInterface:
        """
        :return: the directed graph on which the algorithm works on.
        """
        return self.graph

    def load_from_json(self, file_name: str) -> bool:
        """
        Loads a graph from a json file.

        :param: file_name: The path to the json file.
        :return: True if the loading was successful, False o.w.
        """
        try:
            with open(file_name, 'r') as file:
                data = json.load(file)
                g = DiGraph()
                for i in data['Nodes']:
                    if 'pos' in i.keys():
                        str_lst = i['pos'].split(',')
                        pos = (float(str_lst[0]), float(str_lst[1]))
                        g.add_node(i['id'], pos)
                    else:
                        g.add_node(i['id'])
                for i in data['Edges']:
                    g.add_edge(i['src'], i['dest'], i['w'])
                self.graph = g
        except Exception as e:
            print(e)
            return False

        return True

    def save_to_json(self, file_name: str) -> bool:
        """
        Saves the graph in JSON format to a file

        :param self: getting the self of this class
        :param file_name: The path to the out file
        :return: True if the save was successful, False o.w.
        """
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
        """
        Returns the shortest path from node id1 to node id2 using Dijkstra's Algorithm

        :param self: getting the self of this class
        :param id1: The start node id
        :param id2: The end node id
        :return: The distance of the path, the path as a list
        """
        if id1 not in self.graph.nodes.keys() or id2 not in self.graph.nodes.keys():
            return -1, []
        src = self.graph.nodes[id1]
        dest = self.graph.nodes[id2]

        if id1 == id2:
            return 0, [src.id]

        self.set_tag_dist(id1)
        if dest.tag == -1:
            return float("inf"), None

        lst = []
        lst.insert(0, dest.id)
        curr = lst[0]

        while curr != src.id:
            for i, w in self.graph.nodes[curr].node_in.items():
                n = self.graph.nodes[i]
                if n.tag + w == self.graph.nodes[curr].tag:
                    lst.insert(0, n.id)
                    curr = lst[0]
                    if curr == id2:
                        return dest.tag, lst

        return dest.tag, lst

    def set_tag_dist(self, id1):
        """
        "color" all the nosdes that acn be reached from id1
        :param self: getting the self of this class
        :param id1: the source id
        """
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
        """
        Initialize all the tag's nodes in the graph.
        :param self: getting the self of this class.
        """
        for i in self.graph.nodes.values():
            i.tag = -1

    def connected_component(self, id1: int) -> list:
        """
        Finds the Strongly Connected Component(SCC) that node id1 is a part of.

        :param self: getting the self of this class
        :param id1: The node id
        :return: The list of nodes in the SCC
        """
        if id1 not in self.graph.nodes.keys():
            return None

        self.init_tags()
        num = 0
        self.set_connected_tag(self.graph.nodes[id1], num)
        ll = [id1]
        for i in self.graph.nodes.values():
            if i.tag == 0:
                ll.append(i.id)
        res = []
        for i in ll:
            num += 1
            if self.connect_to_src(id1, i, num):
                res.append(i)
        return res

    def set_connected_tag(self, src: DiGraph.NodeData, num):
        pq = []
        src.tag = -2
        heappush(pq, src)
        while len(pq) > 0:
            temp = heappop(pq)
            for i in temp.node_out.keys():
                t_node = self.graph.nodes[i]
                if t_node.tag == -1:
                    t_node.tag = num
                    heappush(pq, t_node)

    def connect_to_src(self, src: int, node: int, num: int):
        if src == node:
            return True
        lst = []
        node_ = self.graph.nodes[node]
        node_.tag = num
        lst.append(node_)

        while len(lst) > 0:
            temp = lst.pop(0)
            for i in temp.node_out.keys():
                t_node = self.graph.nodes[i]
                if t_node.tag != num:
                    if t_node.tag == -2:
                        node_.tag = -2
                        return True
                    t_node.tag = num
                    lst.append(t_node)
        return False

    def connected_components(self) -> List[list]:
        """
        Finds all the Strongly Connected Component(SCC) in the graph.
        :param self: getting the self of this class
        :return: The list all SCC
        """
        set_ = set()
        lst = []
        for n in self.graph.nodes.values():
            temp = self.connected_component(n.id)
            flag = True
            for i in lst:
                if self.list_equals(i, temp):
                    flag = False
            if flag:
                lst.append(temp)

            for i in self.graph.nodes.keys():
                if i not in set_:
                    ll = self.connected_component(i)
                    set_ = set_.union(ll)
                    lst.append(ll)
            return lst

    def plot_graph(self) -> None:
        """
        Plots the graph.
        If the nodes have a position, the nodes will be placed there.
        Otherwise, they will be placed in a random but elegant manner.
        :param self: getting the self of this class
        :return: None
        """
        Gui(self.graph)

    @staticmethod
    def list_equals(lst1, lst2):
        """
        this function checks if all the objects in one list contains in the other list
        :param lst1: list 1
        :param lst2: list 2
        :return: True iff the list are equals
        """
        for j in lst1:
            if j not in lst2:
                return False
        return True

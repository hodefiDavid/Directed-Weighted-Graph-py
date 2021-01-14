import json
from heapq import heappush, heappop
from queue import PriorityQueue

from DiGraph import *
from GraphAlgoInterface import *
from Gui import Gui


class GraphAlgo(GraphAlgoInterface):
    """This class represents an algorithms class for the class Digraph."""

    mark_tag = 0  # used for the algorithms Scc

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
            return float("inf"), None
        src = self.graph.nodes[id1]
        dest = self.graph.nodes[id2]

        if id1 == id2:
            return 0, [src.id]

        path = self.set_tag_dist(id1, id2)
        if dest.tag == -1:
            return float("inf"), None
        curr = id2
        lst = [id2]
        while curr != id1:
            temp = path[curr]
            lst.insert(0, temp)
            curr = temp

        return dest.tag, lst

    def set_tag_dist(self, id1, id2):
        """
        set the distance from id to all the nodes that can be reached from id1 until we reach id2
        :param self: getting the self of this class
        :param id1: the source id
        :param id2: the destination id
        """
        p_queue = PriorityQueue()
        path = {id1: None}
        self.init_tags()
        curr = self.graph.nodes[id1]
        curr.tag = 0
        p_queue.put((curr.tag, curr))
        while not p_queue.empty():
            curr = p_queue.get()[1]
            if curr.id == id2:
                return path
            if self.graph.nodes[id2].tag != -1:
                if curr.tag >= self.graph.nodes[id2].tag:
                    break

            for nodeIn_id, w in curr.node_out.items():
                n = self.graph.nodes[nodeIn_id]
                if n.tag == -1 or n.tag > curr.tag + w:
                    n.tag = curr.tag + w
                    p_queue.put((n.tag, n))
                    path[n.id] = curr.id

        return path

    def connected_component(self, id1: int) -> list:
        """
        Finds the Strongly Connected Component(SCC) that node id1 is a part of.
        To find the well-linked component that contains the vertex v, we need to construct a group of
        vertices accessible from vertex v lets call this group A. Then a new graph G-transpose** is built
        then we will find all the vertices accessible from vertex v in the graph G-transpose lets call this group B
        Group B ∩ A is a group of vertices that consist the well-linked component of Graph G containing the
        Vertex v. The complexity of an algorithm in the worst case is (| V | * | E |)  because each vertex passes
        On all sides of the graph.
        ** instead of creating a new graph G-transpose we use DFS to the IN_NODE vertices

        :param self: getting the self of this class
        :param id1: The node id
        :return: The list of nodes in the SCC
        """
        if id1 not in self.graph.nodes.keys():
            return None
        self.m_t_init()
        self.init_tags()
        tag = self.m_t()
        self.dfs_mark(id1, tag)
        res = self.dfs_collect(id1, tag)
        return list(res)

    def connected_components(self) -> List[list]:
        """
        Finds all the Strongly Connected Component(SCC) in the graph.
        To find the well-linked component that contains the vertex v, we need to construct a group of
        vertices accessible from vertex v lets call this group A. Then a new graph G-transpose** is built
        then we will find all the vertices accessible from vertex v in the graph G-transpose lets call this group B
        Group B ∩ A is a group of vertices that consist the well-linked component of Graph G containing the
        Vertex v. The complexity of an algorithm in the worst case is (| V | * | E |)  because each vertex passes
        On all sides of the graph.
        ** instead of creating a new graph G-transpose we use DFS to the IN_NODE vertices

        :param self: getting the self of this class
        :return: The list all SCC
        """
        gt = GraphAlgo(self.transpose_graph())
        lst = list()
        lst_node_id = list()

        for i in self.graph.nodes.keys():
            lst_node_id.append(i)

        while len(lst_node_id) > 0:
            temp_node = lst_node_id.pop()

            if temp_node in gt.graph.nodes:
                tag = self.m_t()
                gt.dfs_mark(temp_node, tag)
                connected_component = gt.dfs_collect(temp_node, tag)

                # here we remove from the graph the vertices that already belong to SCC
                for i in connected_component:
                    gt.graph.remove_node(i)

                lst.append(list(connected_component))

        return lst

    def dfs_mark(self, src_id, tag):
        """
        using DFS we mark every node that can be reached from the src node
        we mark the nodes by changing their tag (node.tag) to the given tag
        :param src_id:
        :param tag:
        """
        src = self.graph.nodes[src_id]
        pq = []
        src.tag = tag
        heappush(pq, src)
        while len(pq) > 0:
            temp = heappop(pq)
            for i in temp.node_out.keys():
                t_node = self.graph.nodes[i]
                if t_node.tag != tag:
                    t_node.tag = tag
                    heappush(pq, t_node)

    def dfs_collect(self, src_id, tag) -> set:
        """
        using DFS we collect every node that marked by the function dfs_cc
        we use reverse DFS that mean instead of going throw the OUT_NODE vertices we going throw IN_NODE vertices
        we treat the graph as a transpose graph
        :param src_id:
        :param tag:
        """
        src = self.graph.nodes[src_id]
        pq = []
        src.tag = tag
        heappush(pq, src)
        set_of_connected_nodes = set()
        set_of_connected_nodes.add(src.id)
        while len(pq) > 0:
            temp = heappop(pq)
            for i in temp.node_in.keys():
                t_node = self.graph.nodes[i]
                if t_node.tag == tag:
                    if t_node.id not in set_of_connected_nodes:
                        set_of_connected_nodes.add(t_node.id)
                        heappush(pq, t_node)

        return set_of_connected_nodes

    def plot_graph(self) -> None:
        """
        Plots the graph.
        If the nodes have a position, the nodes will be placed there.
        Otherwise, they will be placed in a random but elegant manner.
        :param self: getting the self of this class
        :return: None
        """
        Gui(self.graph)

    def transpose_graph(self) -> DiGraph:
        """
        Transpose of a directed graph G is another directed graph
        on the same set of vertices with all of the edges reversed
        compared to the orientation of the corresponding edges in G.
        That is, if G contains an edge (u, v) then the converse/transpose/reverse
        of G contains an edge (v, u) and vice versa.
        for more information visit https://www.geeksforgeeks.org/transpose-graph/
        we use the transpose_graph function in the connected_components function.
        :return:Transpose graph
        """
        tg = DiGraph()
        graph = self.graph

        for i in graph.get_all_v():
            tg.add_node(i, graph.nodes[i].position)

        for i in graph.get_all_v():
            for j in graph.nodes[i].node_out:
                tg.add_edge(j, i, graph.all_out_edges_of_node(i)[j])

        return tg

    def init_remark(self):
        """
        Initialize all the remark's nodes in the graph.
        :param self: getting the self of this class.
        """
        for i in self.graph.nodes.values():
            i.remark = 0

    def init_tags(self):
        """
        Initialize all the tag's nodes in the graph.
        :param self: getting the self of this class.
        """
        for i in self.graph.nodes.values():
            i.tag = -1

    def m_t(self) -> int:
        """
        changing GraphAlgo.mark_tag to GraphAlgo.mark_tag + 1
        :return: GraphAlgo.mark_tag + 1
        """
        GraphAlgo.mark_tag = GraphAlgo.mark_tag + 1
        return GraphAlgo.mark_tag

    def m_t_init(self) -> int:
        """
        Initialize mark_tag in the GraphAlgo to 0 (mark_tag = 0).
        :return:GraphAlgo.mark_tag
        """
        GraphAlgo.mark_tag = 0
        return GraphAlgo.mark_tag

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

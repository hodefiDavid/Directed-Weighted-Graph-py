from GraphInterface import *


class DiGraph(GraphInterface):

    def __init__(self):
        self.nodes = dict()
        self.mode_count = 0
        self.edge_size = 0

    def v_size(self) -> int:
        return len(self.nodes)

    def e_size(self) -> int:
        return self.edge_size

    def get_all_v(self) -> dict:
        return self.nodes

    def all_in_edges_of_node(self, id1: int) -> dict:
        return self.nodes[id1].node_in

    def all_out_edges_of_node(self, id1: int) -> dict:
        return self.nodes[id1].node_out

    def get_mc(self) -> int:
        return self.mode_count

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        if id1 not in self.nodes or id2 not in self.nodes or id1 == id2:
            return False

        if id2 in self.nodes[id1].node_out:
            return False

        if weight <= 0:
            return False

        self.nodes[id1].add_out(id2, weight)
        self.nodes[id2].add_in(id1, weight)
        self.mode_count += 1
        self.edge_size += 1
        return True

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        if node_id in self.nodes:
            return False
        self.nodes[node_id] = DiGraph.NodeData(node_id, pos)
        self.mode_count += 1
        return True

    def remove_node(self, node_id: int) -> bool:
        if node_id not in self.nodes:
            return False

        for n in self.nodes[node_id].node_in.keys():
            self.nodes[n].node_out.pop(node_id)
            self.edge_size -= 1

        for n in self.nodes[node_id].node_out.keys():
            self.nodes[n].node_in.pop(node_id)
            self.edge_size -= 1

        self.mode_count += 1
        self.nodes.pop(node_id)
        return True

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:

        if node_id1 not in self.nodes or node_id2 not in self.nodes \
                or node_id2 not in self.nodes[node_id1].node_out:
            return False

        self.nodes[node_id1].node_out.pop(node_id2)
        self.nodes[node_id2].node_in.pop(node_id1)
        self.edge_size -= 1
        self.mode_count += 1
        return True

    def __str__(self):
        node_str = ''
        for i in self.nodes.values():
            if len(i.node_out) > 0:
                node_str += '\t\t' + str(i) + ' -> ' + str(i.node_out) + '\n'
        return 'DiGraph: |V| = ' + str(self.v_size()) + '\t|E| = ' + str(self.e_size()) \
               + '\n' + str(self.nodes) + '\n' + "Edge Data:\n" + node_str + '\n'

    def __eq__(self, other):
        return self.edge_size == other.edge_size and self.nodes == other.nodes

    class NodeData:

        def __init__(self, node_id: int, pos: tuple = None):
            self.id = node_id
            self.tag = -1.0
            self.remark = ""
            self.node_out = dict()
            self.node_in = dict()
            self.position = pos

        def add_out(self, node_id: int, weight: float):
            self.node_out[node_id] = weight

        def add_in(self, node_id: int, weight: float):
            self.node_in[node_id] = weight

        def __str__(self):
            return '(' + str(self.id) + ')'

        def __repr__(self):
            return self.__str__()

        def __eq__(self, other):
            return self.id == other.id and self.position == other.position \
                   and self.node_in == other.node_in and self.node_out == other.node_out

        def __lt__(self, other):
            t = self.tag - other.tag
            return t

from GraphInterface import *


class DiGraph(GraphInterface):

    def __init__(self):
        """
        Constructor.
        init dictionary to stores the nodes of the graph.
        also init mode_count and edge_size to 0.
        """
        self.nodes = dict()
        self.mode_count = 0
        self.edge_size = 0

    def v_size(self) -> int:
        """
        Returns the length of nodes field.
        :return: the number of vertices in this graph.
        """
        return len(self.nodes)

    def e_size(self) -> int:
        """
        Returns the number of edges in this graph
        :return: The number of edges in this graph
        """
        return self.edge_size

    def get_all_v(self) -> dict:
        """
        Returns a dictionary of all the nodes in the Graph,
        each node is represented using a pair (key, NodeData)
        :return: dict contains all the nodes in the graph.
        """
        return self.nodes

    def all_in_edges_of_node(self, id1: int) -> dict:
        """
        Return a dictionary of all the nodes connected to (into) node_id,
        each node is represented using a pair (key, weight)
        :param id1: node id
        :return: dictionary contains nodes connected to id1
        """
        return self.nodes[id1].node_in

    def all_out_edges_of_node(self, id1: int) -> dict:
        """
        Return a dictionary of all the nodes connected from node_id,
        each node is represented using a pair (key, weight)
        :param id1: node id
        :return: dictionary contains nodes connected from id1
        """
        return self.nodes[id1].node_out

    def get_mc(self) -> int:
        """
        Returns the current version of this graph,
        on every change in the graph state - the MC should be increased.
        :return: The current version of this graph.
        """
        return self.mode_count

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        """
        Adds an edge to the graph.
        If the edge already exists or one of the nodes dose not exists the functions will do nothing.
        This method adds id2 nodes to node_out of id1, and id1 to node_in of id2.
        :param id1: The start node of the edge.
        :param id2: The end node of the edge.
        :param weight: The weight of the edge.
        :return: True if the edge was added successfully, False o.w.
        """
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
        """
        Adds a node to the graph.
        If the node id already exists the node will not be added.
        This method adds new NodeData to the nodes dictionary.
        :param node_id: The node ID.
        :param pos: The position of the node.
        :return: True if the node was added successfully, False o.w.

        """
        if node_id in self.nodes:
            return False
        self.nodes[node_id] = DiGraph.NodeData(node_id, pos)
        self.mode_count += 1
        return True

    def remove_node(self, node_id: int) -> bool:
        """
        Removes a node from the graph.
        If the node id does not exists the function will do nothing.
        This method remove the node from nodes dictionary,
        and also remove all in and out edges.
        :param node_id: The node ID.
        :return: True if the node was removed successfully, False o.w.
        """
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
        """
        Removes an edge from the graph.
        If such an edge does not exists the function will do nothing.
        :param node_id1: The start node of the edge.
        :param node_id2: The end node of the edge.
        :return: True if the edge was removed successfully, False o.w.

        """
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
        """
        This inner class are represent a node in directed weighted graph - DiGraph.
        Every NodeData has unique id, and also 2D position, and 2 dictionary:
        for edges get out from the nodes, and for edges get in to the node.
        This dictionaries node_id as keys and edge weight as values.
        """

        def __init__(self, node_id: int, pos: tuple = None):
            self.id = node_id
            self.tag = -1.0
            self.remark = ""
            self.node_out = dict()
            self.node_in = dict()
            self.position = pos

        def add_out(self, node_id: int, weight: float):
            """
            Add new edge from this node to node_id, with the given weight.
            :param node_id: The end node of the edge.
            :param weight: The weight of the edge.
            """
            self.node_out[node_id] = weight

        def add_in(self, node_id: int, weight: float):
            """
            Add new edge from node_id to this node, with the given weight.
            :param node_id: The start node of the edge.
            :param weight: The weight of the edge.
            """
            self.node_in[node_id] = weight

        def __str__(self):
            return '(' + str(self.id) + ')'

        def __repr__(self):
            return self.__str__()

        def __eq__(self, other):
            return self.id == other.id and self.position == other.position \
                   and self.node_in == other.node_in and self.node_out == other.node_out

        def __lt__(self, other):
            t = other.tag - self.tag
            return t

        def __hash__(self):
            return self.id

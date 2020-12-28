from xml.parsers import expat

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
        # node_data
        # Src = _g.getNode(src);
        # node_data
        # Dest = _g.getNode(dest);
        # if (Src != null & & Dest != null) {
        # this.initNodeWeight();
        # this.initNodeTag();
        #
        # setDistance(Src);
        #
        # return Dest.getWeight();
        # }

    def connected_component(self, id1: int) -> list:
        pass

    def connected_components(self) -> List[list]:
        pass

    def plot_graph(self) -> None:
        pass

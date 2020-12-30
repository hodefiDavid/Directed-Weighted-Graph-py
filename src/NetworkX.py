import json

import matplotlib.pyplot as plt
import networkx as nx


def graph_range(locations: dict) -> tuple:
    """
    Finds the ranges of the graph, by finding minimum and maximum positions.
    @return: (x_range, y_range)
    """
    x_range = [float('inf'), float('-inf')]
    y_range = [float('inf'), float('-inf')]
    for j in locations.values():
        location = j
        if location[0] < x_range[0]:
            x_range[0] = location[0]
        if location[0] > x_range[1]:
            x_range[1] = location[0]
        if location[1] < y_range[0]:
            y_range[0] = location[1]
        if location[1] > y_range[1]:
            y_range[1] = location[1]

    return x_range, y_range


def w2fx(x_range, position):
    """
    Converts from world position to frame position.
    @param x_range:
    @param position: x node coordinate.
    @return: normalized x location.
    """
    return (position - x_range[0]) / (x_range[1] - x_range[0]) * 20


def w2fy(y_range, position):
    """
    Converts from world position to frame position.
    @param y_range:
    @param position: y node coordinate.
    @return: normalized y location.
    """
    return (position - y_range[0]) / (y_range[1] - y_range[0]) * 10


with open('../data/A5', 'r') as file:
    data = json.load(file)
    g = nx.DiGraph()
    loc_w = {}
    for i in data['Nodes']:
        if 'pos' in i.keys():
            str_lst = i['pos'].split(',')
            pos = (float(str_lst[0]), float(str_lst[1]))
            g.add_node(i['id'])
            loc_w[i['id']] = pos

        else:
            g.add_node(i['id'])
    for i in data['Edges']:
        g.add_edge(i['src'], i['dest'])

x, y = graph_range(loc_w)
loc = {}
for k, l in loc_w.items():
    loc[k] = w2fx(x, l[0]), w2fy(y, l[1])

# g.remove_edge(13, 14)
# print([i for i in nx.connected_components(g)])

nx.draw(g, loc)

# pos = nx.spring_layout(g)
# pos = nx.random_layout(g)
# pos = nx.shell_layout(g)
# pos = nx.planar_layout(g)


nx.draw_networkx_nodes(g, loc, cmap=plt.get_cmap('jet'), node_size=50)
nx.draw_networkx_labels(g, loc)
nx.draw_networkx_edges(g, loc, edge_color='b', arrows=True)
plt.show()

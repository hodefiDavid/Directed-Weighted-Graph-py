import matplotlib.pyplot as plt
import networkx as nx

"""
This file contains a number of functions that aim to make the necessary adjustments,
to display a networkx graph from the given json files
"""


def graph_range(locations: dict) -> tuple:
    """
    Finds the ranges of the graph, by finding minimum and maximum positions.
    :return: (x_range, y_range)
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
    :param x_range:
    :param position: x node coordinate.
    :return: normalized x location.
    """
    return (position - x_range[0]) / (x_range[1] - x_range[0]) * 20


def w2fy(y_range, position):
    """
    Converts from world position to frame position.
    :param y_range:
    :param position: y node coordinate.
    :return: normalized y location.
    """
    return (position - y_range[0]) / (y_range[1] - y_range[0]) * 10


def convert_pos(loc_world):
    """
    Converts loc_world dictionary to loc_frame dictionary, after converts each position.
    :param loc_world: a dictionary contains world position as values, and node id as keys.
    :return: a dictionary with id node as keys and position (x, y) as values.
    """
    x, y = graph_range(loc_world)
    loc_frame = {}
    for k, l in loc_world.items():
        loc_frame[k] = w2fx(x, l[0]), w2fy(y, l[1])
    return loc_frame


def plot(gx, loc_w):
    """
    Plots networkx graph.
    :param gx: nx.DiGraph
    :param loc_w: a dictionary with id node as keys and position (x, y) as values.
    """
    loc = convert_pos(loc_w)
    nx.draw(gx, loc)
    nx.draw_networkx_nodes(gx, loc, cmap=plt.get_cmap('jet'), node_size=50)
    nx.draw_networkx_labels(gx, loc)
    nx.draw_networkx_edges(gx, loc, edge_color='b', arrows=True)
    plt.show()

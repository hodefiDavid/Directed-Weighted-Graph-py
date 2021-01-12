from random import choice, seed

import matplotlib.pyplot as plt


class Gui:

    def __init__(self, g):
        self.graph = g
        self.set_pos()
        self.x_range, self.y_range = self.graph_range()
        self.draw()

    def draw(self):
        """
        Draw and show the graph, nodes and edges.
        """
        fig, ax = plt.subplots()
        fig.tight_layout()
        fig.set_size_inches(10, 5)

        xs = []
        ys = []
        labels = []

        for i in self.graph.nodes.values():
            x_src = self.w2fx(i.position[0])
            y_src = self.w2fy(i.position[1])
            xs.append(x_src)
            ys.append(y_src)
            labels.append(i.id)

            for node_out in i.node_out.keys():
                n = self.graph.nodes[node_out]
                x_dest = self.w2fx(n.position[0])
                y_dest = self.w2fy(n.position[1])



                plt.arrow(x_src, y_src, -(x_src - x_dest), -(y_src - y_dest), head_width=0.28,
                          length_includes_head=True)

        plt.plot(xs, ys, 'ro', markersize=10)

        for i, txt in enumerate(labels):
            ax.annotate(txt, (xs[i] - .2, ys[i] - .1), fontsize=8)

        plt.axis('equal')

        plt.show()

    def w2fx(self, position):
        """
        In order to draw any graph we get to and to keep the size differences
        between the arrows head and width and the vertices
        We decided to normalize the graph
        This means displaying each graph on a grid between 0-10 and 0-5
        and thus the size of the arrows and the thickness of the lines
        remain constant even when changing the graphs

        Converts from world position to frame position.
        :param position: x node coordinate.
        :return: normalized x location.
        """
        return (position - self.x_range[0]) / (self.x_range[1] - self.x_range[0]) * 20

    def w2fy(self, position):
        """
        In order to draw any graph we get to and to keep the size differences
        between the arrows head and width and the vertices
        We decided to normalize the graph
        This means displaying each graph on a grid between 0-10 and 0-5
        and thus the size of the arrows and the thickness of the lines
        remain constant even when changing the graphs

        Converts from world position to frame position.
        :param position: y node coordinate.
        :return: normalized y location.
        """
        return (position - self.y_range[0]) / (self.y_range[1] - self.y_range[0]) * 10

    def graph_range(self) -> tuple:
        """
        Finds the ranges of the graph, by finding minimum and maximum positions.
        :return: (x_range, y_range)
        """
        x_range = [float('inf'), float('-inf')]
        y_range = [float('inf'), float('-inf')]
        for i in self.graph.nodes.values():
            pos = i.position
            if pos[0] < x_range[0]:
                x_range[0] = pos[0]
            if pos[0] > x_range[1]:
                x_range[1] = pos[0]
            if pos[1] < y_range[0]:
                y_range[0] = pos[1]
            if pos[1] > y_range[1]:
                y_range[1] = pos[1]

        return x_range, y_range

    def set_pos(self):
        """
        Sets random position for every node without position.
        This method scatters the positions of the nodes on the screen in a balanced way.
        """
        v = self.graph.v_size()
        seed(1)
        curr_range = [i for i in range(2 * v)]
        for i in self.graph.nodes.values():
            if i.position is None:
                x = choice(curr_range)
                curr_range.remove(x)
                y = choice(curr_range)
                curr_range.remove(y)
                i.position = (x, y)

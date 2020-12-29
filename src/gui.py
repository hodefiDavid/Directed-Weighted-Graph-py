from random import uniform, randrange, random, choice
import numpy as np

import matplotlib.pyplot as plt


class Gui:
    def __init__(self, g):
        self.graph = g
        self.set_pos()
        self.x_range, self.y_range = self.graph_range()
        self.draw()

    def draw(self):
        fig, ax = plt.subplots()
        fig.tight_layout()
        # fig.set_size_inches((14, 7))
        fig.set_size_inches(10, 5)

        xs = []
        ys = []
        labels = []

        for i in self.graph.nodes.values():
            x_src = self.w2fy(i.position[0])
            y_src = self.w2fy(i.position[1])
            xs.append(x_src)
            ys.append(y_src)
            labels.append(i.id)

            for node_out in i.node_out.keys():
                n = self.graph.nodes[node_out]
                x_dest = self.w2fy(n.position[0])
                y_dest = self.w2fy(n.position[1])

                plt.arrow(x_src, y_src, -(x_src - x_dest), -(y_src - y_dest), head_width=0.28,
                          length_includes_head=True)

        plt.plot(xs, ys, 'ro', markersize=10)

        for i, txt in enumerate(labels):
            ax.annotate(txt, (xs[i] - .2, ys[i] - .1), fontsize=8)

        plt.axis('equal')
        # plt.axis('scaled')
        plt.show()

    def w2fx(self, position):
        return (position - self.x_range[0]) / (self.x_range[1] - self.x_range[0]) * 20

    def w2fy(self, position):
        return (position - self.y_range[0]) / (self.y_range[1] - self.y_range[0]) * 10

    def graph_range(self):
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
        v = self.graph.v_size()
        curr_range = [i for i in range(2 * v)]
        for i in self.graph.nodes.values():
            if i.position is None:
                x = choice(curr_range)
                curr_range.remove(x)
                y = choice(curr_range)
                curr_range.remove(y)
                i.position = (x, y)

# x = np.random.rand(1000) * 10
# norm1 = x / np.linalg.norm(x)
# norm2 = normalize(x[:, np.newaxis], axis=0).ravel()
# np.all(norm1 == norm2)
# ax.axis([32, 32, 36, 36])
# xs = [i.position[0] for i in self.graph.nodes.values()]
# xs = [self.w2fx(i.position[0]) for i in self.graph.nodes.values()]
# ys = [i.position[1] for i in self.graph.nodes.values()]
# ys = [self.w2fy(i.position[1]) for i in self.graph.nodes.values()]
# def world2frame(self, position):
#     x = (position[0] - self.x_range[0]) / (self.x_range[1] - self.x_range[0])
#     y = (position[1] - self.y_range[0]) / (self.y_range[1] - self.y_range[0])
#
#     return x, y     # for i in self.graph.nodes.values():
#         #     pos_src = self.world2frame(i.position)
#         #     for j in i.node_out.keys():
#         #         pos_dest = self.world2frame(self.graph.nodes[j].position)
#         #         plt.arrow(pos_src[0], pos_src[1], pos_src[0]-pos_dest[0], pos_src[1]-pos_dest[1], head_width=0.05, length_includes_head=True)
#         # print(i, pos_src, j, pos_dest)
#         # for i in xs:
#         #     for j in ys:
#         #         plt.arrow(i, j, 4, 4, head_width=.3, length_includes_head=True)
#
#         # break  # nx.drawing.draw()

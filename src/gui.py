import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import normalize


class Gui:
    def __init__(self, g):
        self.graph = g
        self.x_range, self.y_range = self.graph_range(g)
        self.draw()

    def draw(self):
        x = np.random.rand(1000) * 10
        norm1 = x / np.linalg.norm(x)
        norm2 = normalize(x[:, np.newaxis], axis=0).ravel()
        np.all(norm1 == norm2)

        plt.figure(figsize=(4, 3), dpi=70)
        fig, ax = plt.subplots()
        ax.axis([32, 32, 36, 36])
        for i in self.graph.nodes.values():
            pos_src = self.world2frame(i.position)
            for j in i.node_out.keys():
                pos_dest = self.world2frame(self.graph.nodes[j].position)
                plt.arrow(pos_src[0], pos_src[1], pos_dest[0], pos_dest[1], head_width=3, length_includes_head=True)
                print(i, pos_src, j, pos_dest)

        plt.axis('equal')
        plt.show()

    def world2frame(self, position):
        x = (position[0] - self.x_range[0]) / (self.x_range[1] - self.x_range[0])
        y = (position[1] - self.y_range[0]) / (self.y_range[1] - self.y_range[0])
        x *= 100
        y *= 100

        return x, y

    def graph_range(self, g):
        x_range = [float('inf'), float('-inf')]
        y_range = [float('inf'), float('-inf')]
        for i in g.nodes.values():
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

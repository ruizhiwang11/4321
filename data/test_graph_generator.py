import os
import random
import string

import networkx as nx


class TestGraphGenerator:
    NUM_NODES = 1000

    def _get_random_string(self):
        letters = string.ascii_letters
        return "".join(random.choice(letters) for i in range(6))

    def generate(self):
        filename = f"./test_graphs/test_graph_{self._get_random_string()}.txt"
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))

        G = nx.connected_watts_strogatz_graph(self.NUM_NODES, 10, 0)
        edges = G.edges()

        with open(filename, "w") as f:
            for edge in edges:
                f.write(f"{str(edge[0])}\t{str(edge[1])}\n")
                if edge[1] == self.NUM_NODES - 1:
                    f.write(f"{str(edge[1])}\t{str(edge[0])}\n")

        print(f"generated random test graph - {filename}")
        return filename

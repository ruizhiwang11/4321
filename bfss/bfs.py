"""
    Use an immutable dict to represent nodes in the network
    g is an simple exmaple of an unweighted, undirected graph

    [0] - node id (string)
    [1] - is_hospital (bool)
"""
g = {
    ("1", False): [("2", False), ("3", True)],
    ("2", False): [("1", False), ("4", False), ("5", True)],
    ("3", True): [("1", False), ("6", False), ("7", True)],
    ("4", False): [("2", False)],
    ("5", True): [("2", False), ("6", False), ("7", True)],
    ("6", False): [("3", True), ("5", True), ("7", True)],
    ("7", True): [("3", True), ("5", True), ("6", False)],
}


class BfsShortest(object):
    g = []

    def __init__(self, g):
        self.g = g

    def get_path(self, s, k=1):
        dist = {s: 0}  # distance from source to each node
        queue = [s]  # queue
        path = {}  # path from source to each node
        hospital_nodes = []

        while queue:
            current = queue.pop(0)
            for neighbour in g.get(current, []):
                if neighbour not in dist:
                    dist[neighbour] = dist[current] + 1
                    path[neighbour] = current
                    queue.append(neighbour)
                    if neighbour[1]:
                        hospital_nodes.append(neighbour)
                if len(hospital_nodes) >= k:
                    break

        if not hospital_nodes:
            print("There is no path to travel from source node to any hospital.")
            return

        # now we have a list of hospital nodes sorted ascendingly in terms of distance
        for i in range(k):
            if not hospital_nodes:
                break
            h = hospital_nodes.pop(0)
            print(f">>>>>>>>>> { i + 1 }. Hospital Node {h[0]} <<<<<<<<<<<")
            print("Distance: ", dist[h])
            self._print_path(path, h)

    def _print_path(self, path, node):
        """trace back the previous node in each node
            to construct the full path
        """
        path_stack, queue = [], [node]
        while queue:
            current = queue.pop(0)
            path_stack.insert(0, current)
            if path.get(current):
                queue.append(path[current])

        print("Path:", end=" ")
        for node in path_stack:
            print(node[0], end=" ")
        print()


if __name__ == "__main__":
    # prepare the graph
    bfs_shortest = BfsShortest(g)
    # prepare the source node and value k
    s, k = ("4", False), 2
    # find hospital(s)
    bfs_shortest.get_path(s, k)

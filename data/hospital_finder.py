class HospitalFinder:
    def __init__(self, graph_path):
        # TODO: use HospitalGenerator class to fill up hospitals
        self.__hospitals = [7,3,6,9,7878,7979,12121,12222,55569,123,3535,213123,223232,154564,89898,45545,98852,654511,58787,21232,8878,212312,8788,21212,54545,87,87,6332,87897,54642,121,3,545645,138,78,213,21,5,]
        self.__graph = self._init_graph(graph_path, self.__hospitals)

    def _init_graph(self, graph_path, hospital_list):
        graph = {}
        with open(graph_path, "r") as f:
            last_node_id = -1
            temp_list = []

            for row in f:
                x = row.split()
                if x[0] == "#":
                    continue
                node_id = int(x[0])
                neighbor_node_id = int(x[1])
                neighbor_node = ()
                if node_id != last_node_id:
                    temp_list = []
                if neighbor_node_id in hospital_list:
                    neighbor_node = (neighbor_node_id, True)
                else:
                    neighbor_node = (neighbor_node_id, False)
                temp_list.append(neighbor_node)
                graph[node_id] = temp_list
                last_node_id = node_id
        return graph

    def search(self, start, k):
        """search for k hospitals from any node"""
        flag = k
        path_k = []
        explored = []
        queue = [[start]]
        founded_hospital = []
        # TODO: find out why its so slow to search
        if start in self.__hospitals:
            k-=1
            path_k.append(start)
            founded_hospital.append(start)
        while queue and k > 0:
            path = queue.pop(0)
            node = path[-1]
            if node not in explored:
                neighbours = self.__graph[node]
                for neighbour in neighbours:
                    if neighbour[1] is False:
                        if neighbour[0] in explored:
                            continue
                        else:
                            new_path = list(path)
                            new_path.append(neighbour[0])
                            queue.append(new_path)

                    else:
                        if neighbour[0] not in founded_hospital:
                            new_path = list(path)
                            new_path.append(neighbour[0])
                            path_k.append(new_path)
                            founded_hospital.append(neighbour[0])
                            queue.append(new_path)
                            k -= 1
                            print(new_path)

                explored.append(node)
        if not path_k:
            return "no hospital can be found on this starting point"
        if k > 0:
            return f"We can only find {flag - k} hospitals from this starting point"
        else:
            return path_k


hospital_finder = HospitalFinder("./roadNet-CA.txt")
print(hospital_finder.search(213155, 3))

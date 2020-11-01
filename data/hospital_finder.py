from hospital_generator import HospitalGenerator


class HospitalFinder:
    NUM_HOSPITAL = 340

    def __init__(self, graph_path):
        self.__graph, self.__hospitals = self._init_graph(graph_path)
        print(f"> generated {len(self.__hospitals)} hospitals")

    def _init_graph(self, graph_path):
        # generating hospital list
        hospital_list = set()
        hospitals_path = HospitalGenerator(graph_path).generate(self.NUM_HOSPITAL)
        with open(hospitals_path, "r") as f:
            for row in f:
                id = row.split()[0]
                if id == "#":
                    continue
                hospital_list.add(int(id))

        # generating graph
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

        return graph, hospital_list

    def search(self, start, k):
        """search for k hospitals from any node"""
        flag = k
        path_k = []
        explored = set()
        queue = [[start]]
        founded_hospital = set()
        if start in self.__hospitals:
            k-=1
            path_k.append(start)
            founded_hospital.add(start)
        while queue and k > 0:
            path = queue.pop(0)
            node = path[-1]
            if node not in explored:
                neighbours = self.__graph[node]
                for neighbour in neighbours:
                    if not neighbour[1]:
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
                            founded_hospital.add(neighbour[0])
                            queue.append(new_path)
                            k -= 1
                            print(new_path)

                explored.add(node)
        if not path_k:
            return "no hospital can be found on this starting point"
        if k > 0:
            return f"We can only find {flag - k} hospitals from this starting point"
        else:
            return path_k


hospital_finder = HospitalFinder("./roadNet-CA.txt")
print(hospital_finder.search(539695, 20))

import os

from hospital_generator import HospitalGenerator


class HospitalFinder:
    NUM_HOSPITAL = 340

    def __init__(self, graph_path):
        self.__graph_path = graph_path
        self.__graph, self.__hospitals = self._init_graph()
        print(f"> generated {len(self.__hospitals)} hospitals")

    def _init_graph(self):
        # generating hospital list
        hospital_list = set()
        hospitals_path = HospitalGenerator(self.__graph_path).generate(
            self.NUM_HOSPITAL
        )
        with open(hospitals_path, "r") as f:
            for row in f:
                id = row.split()[0]
                if id == "#":
                    continue
                hospital_list.add(int(id))

        # generating graph
        graph = {}
        with open(self.__graph_path, "r") as f:
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

    def _search(self, **kwargs):
        """search for k hospitals from any node"""
        start, k = kwargs.get("start"), kwargs.get("k")
        path_k = []
        explored = set()
        queue = [[start]]
        founded_hospital = set()
        if start in self.__hospitals:
            k -= 1
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

                explored.add(node)
        return path_k

    def print_result(self, **kwargs):
        """print search result"""
        result = self._search(**kwargs)
        num_hospital = kwargs.get("k")

        if not result:
            return "no hospital can be found on this starting point"
        if len(result) < num_hospital:
            return f"We can only find {num_hospital - len(result)} hospitals from this starting point"

        for path in result:
            print(path)

    def save_result(self, **kwargs):
        """save search result into a text file"""
        result = self._search(**kwargs)
        num_hospital = kwargs.get("k")

        filename = (
            f"./result_txts/{self.__graph_path.split('/')[-1].split('.')[0]}_result.txt"
        )
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))

        with open(filename, "w") as f:
            f.write(f">>>>>>> Path for {num_hospital} hospital(s) <<<<<<<\n\n")
            for path in result:
                index = 1
                f.write(
                    f"[Distance(Edges): {len(path)}, Destination: Hospital {path[-1]}]\n"
                )
                for node in path:
                    f.write(str(node))
                    if index != len(path):
                        f.write(" -> ")
                    else:
                        f.write("\n\n")
                    index += 1

        print(f"> generated result text file - {filename}")


hospital_finder = HospitalFinder("./roadNet-CA.txt")
hospital_finder.save_result(start=539695, k=3)

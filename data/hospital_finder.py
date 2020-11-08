import os
import time

from hospital_generator import HospitalGenerator


class HospitalFinder:
    def __init__(self, graph_path, total_hospital=340):
        self.__graph_path = graph_path
        self.__graph, self.__hospitals = self._init_graph(total_hospital)
        print(f"generated {len(self.__hospitals)} hospitals")

    def _init_graph(self, total_hospital):
        print(f"preparing graph...")
        # generating hospital list
        hospital_list = set()
        hospitals_path = HospitalGenerator(self.__graph_path).generate(total_hospital)
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

    @property
    def graph(self):
        return self.__graph

    @property
    def hospitals(self):
        return self.__hospitals

    @hospitals.setter
    def hospitals(self, hospitals_list):
        self.__hospitals = hospitals_list

    def _search(self, **kwargs):
        # record start time
        start_time = time.time()

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

        return path_k, time.time() - start_time

    def print_result(self, **kwargs):
        """print search result"""
        result, time_taken = self._search(**kwargs)
        num_hospital = kwargs.get("k")

        if not result:
            return "no hospital can be found on this starting point"
        if len(result) < num_hospital:
            return f"We can only find {num_hospital - len(result)} hospitals from this starting point"

        print(f"\n\n>>>>>>> Path for {num_hospital} hospital(s) <<<<<<<\n")
        for path in result:
            print(f"[Distance(Edges): {len(path)}, Destination: Hospital {path[-1]}]")
            for index, node in enumerate(path, start=1):
                print(str(node), end="")
                if index != len(path):
                    print(" -> ", end="")
                else:
                    print("\n")

        print(
            f"TIME TAKEN to find {num_hospital} closest hospital(s) {time_taken} seconds."
        )

    def save_result(self, **kwargs):
        """save search result into a text file"""
        result, time_taken = self._search(**kwargs)
        num_hospital = kwargs.get("k")

        filename = (
            f"./result_txts/{self.__graph_path.split('/')[-1].split('.')[0]}_result.txt"
        )
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))

        with open(filename, "w") as f:
            f.write(f">>>>>>> Path for {num_hospital} hospital(s) <<<<<<<\n\n")
            for path in result:
                f.write(
                    f"[Distance(Edges): {len(path)}, Destination: Hospital {path[-1]}]\n"
                )
                for index, node in enumerate(path, start=1):
                    f.write(str(node))
                    if index != len(path):
                        f.write(" -> ")
                    else:
                        f.write("\n\n")
        print(f"search result has been stored into text file - {filename}")
        print(
            f"TIME TAKEN to find {num_hospital} closest hospital(s) {time_taken} seconds."
        )

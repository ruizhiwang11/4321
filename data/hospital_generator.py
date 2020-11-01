import math
import os
import random


class HospitalGenerator:
    def __init__(self, graph_path):
        """[graph_path] should be the abs/relative path to the graph txt file"""

        if not os.path.isfile(graph_path):
            raise Exception("Please input correct graph file path")

        self.__graph_path = graph_path
        with open(graph_path, "r") as f:
            nodes_set = set()
            for row in f:
                node_id = row.split()[0]
                if node_id == "#":
                    continue
                nodes_set.add(int(node_id))
            self.__nodes = list(nodes_set)

    def generate(self, hospital_number=None, hospital_ratio=None):
        """
        refer to test cases in the end of the file for function input
        [hospital_number] any number less than number of nodes
        [hospital_ratio] should be from 0(exclusive) to 10 as the accurate hospital ratio
        """
        if hospital_ratio and (hospital_ratio <= 0 or hospital_ratio > 10):
            raise Exception("Please input hospital ratio from 0(exclusive) to 10.")

        if hospital_number and hospital_number > len(self.__nodes):
            raise Exception("number of hospitals exceeds number of nodes.")

        num_hospital = (
            int(math.floor(len(self.__nodes) * hospital_ratio / 100))
            if hospital_ratio
            else hospital_number
        ) or 1
        hospital_nodes = sorted(random.choices(self.__nodes, k=num_hospital))

        filename = f"./hospital_txts/{self.__graph_path.split('/')[-1].split('.')[0]}_hospitals.txt"
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))

        with open(filename, "w") as f:
            f.write(f"# {len(hospital_nodes)}\n")
            for node in hospital_nodes:
                f.write(f"{node}\n")

        print(f"> generated hospital text file - {filename}")
        return filename


if __name__ == "__main__":
    # test cases
    hg = HospitalGenerator("./roadNet-CA.txt")
    # hg.generate(hospital_ratio=0)
    # hg.generate(hospital_ratio=11)
    # hg.generate(hospital_ratio=-2)
    # hg.generate(hospital_ratio="asdq")
    # hg.generate(99999999999999)
    # hg.generate(99999999999999, 5)
    # hg.generate(5, 500)

    # VALID input tests
    # hg.generate(5, 2)
    # hg.generate(hospital_ratio=5.5)
    # hg.generate(5)
    print(hg.generate(340))

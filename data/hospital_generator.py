import math
import os
import random


class HospitalGenerator:
    def __init__(self, graph_path):
        """[graph_path] should be the abs/relative path to the graph txt file"""

        if not os.path.isfile(graph_path):
            raise Exception("Please input correct graph file path")

        self.__nodes = []
        self.__graph_path = graph_path
        with open(graph_path, "r") as f:
            for row in f:
                node_id = row.split()[0]
                if node_id not in self.__nodes:
                    self.__nodes.append(node_id)

    def _get_hospitals(self, hospital_ratio):
        """create a list of random hospital nodes"""
        num_hospital = int(math.floor(len(self.__nodes) * hospital_ratio / 100))
        return sorted(random.choices(self.__nodes, k=num_hospital))  # need python3

    def generate(self, hospital_ratio=3):
        """[hospital_ratio] should be from 1 to 10 as the accurate hospital ratio"""

        if (
            not (isinstance(hospital_ratio, int) or isinstance(hospital_ratio, float))
            or hospital_ratio < 1
            or hospital_ratio > 10
        ):
            raise Exception("Please input hospital ratio from 1 to 10.")

        hospital_nodes = self._get_hospitals(hospital_ratio)

        filename = f"./hospital_txts/{self.__graph_path.split('/')[-1].split('.')[0]}_hospitals.txt"
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))

        with open(filename, "w") as f:
            f.write(f"# {len(hospital_nodes)}\n")
            for node in hospital_nodes:
                f.write(f"{node}\n")


# test cases
hg = HospitalGenerator("./testGraphs/testfile1.txt")
# hg.generate(0)
# hg.generate(11)
# hg.generate(-2)
# hg.generate("asdq")
# hg.generate(0.5)
# hg.generate(10.5)
# hg.generate(5.5)
hg.generate()
# hg.generate(5)
# hg.generate(10)

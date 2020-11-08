import random

from hospital_finder import HospitalFinder
from test_graph_generator import TestGraphGenerator


class Menu:
    REAL = 1
    SMALL = 2
    EXIT = 3
    PRINT = 1
    FILE = 2

    MENU_OPTIONS = (REAL, SMALL, EXIT)
    OUTPUT_OPTIONS = (PRINT, FILE)

    def _print_menu(self):
        print(
            """
            \n
            ********************************************
            |          Demo of hospital finder         |
            ********************************************
            |                                          |
            |   1. Real road network(LA)               |
            |   2. Small random graph(1000 Nodes)      |
            |   3. End                                 |
            |                                          |
            ********************************************
            """
        )

    def _request_type(self):
        self._print_menu()
        selection = int(input("> Please enter number for selection: "))
        return self._validate_input(
            "> Please enter correct number for selection: ",
            selection,
            self.MENU_OPTIONS,
        )

    def _request_hospital_number(self):
        message = "> Please enter total number of hospital: "
        num_hospital = int(input(message))
        return self._validate_input(message, num_hospital, range(1000000))

    def _request_start_node(self, graph):
        nodes = set(graph.keys())
        random_options = random.sample(nodes, 10)

        print("Some randon nodes for your selection: ", random_options)
        message = "> Please enter id of start node: "
        start_node = int(input(message))
        return self._validate_input(
            "> Please enter id of existing node: ", start_node, nodes
        )

    def _request_k_hospital(self, hospital_list):
        message = "> Please enter k value(number of hospital to search): "
        k = int(input(message))
        return self._validate_input(message, k, range(len(hospital_list) + 1))

    def _request_ouput(self):
        message = "> Please select output type(1 - print, 2 - file): "
        output_type = int(input(message))
        return self._validate_input(message, output_type, self.OUTPUT_OPTIONS)

    def _validate_input(self, message, selection, options):
        """reprompt user to enter valid input"""
        current_selection = selection
        while current_selection not in options:
            current_selection = int(input(message))
        return current_selection

    def _option_process(self, graph_path):
        num_hospital = self._request_hospital_number()
        hospital_finder = HospitalFinder(graph_path, num_hospital)
        start_node = self._request_start_node(hospital_finder.graph)
        k = self._request_k_hospital(hospital_finder.hospitals)
        output_type = self._request_ouput()

        if output_type == self.PRINT:
            hospital_finder.print_result(start=start_node, k=k)
        elif output_type == self.FILE:
            hospital_finder.save_result(start=start_node, k=k)
        return self._request_type()

    def _real_option(self):
        print("\nstart testing on LA road network graph...")
        graph_path = "./roadNet-CA.txt"
        return self._option_process(graph_path)

    def _small_option(self):
        print("\nstart testing on small random graph(1000 nodes)...")
        graph_path = TestGraphGenerator().generate()
        return self._option_process(graph_path)

    def start(self):
        selection = self._request_type()
        while selection != 3:
            if selection == self.REAL:
                selection = self._real_option()
            elif selection == self.SMALL:
                selection = self._small_option()

        print("END...")

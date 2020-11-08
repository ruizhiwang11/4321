import random

from hospital_finder import HospitalFinder
from hospital_generator import HospitalGenerator
from test_graph_generator import TestGraphGenerator


class Menu:
    REAL = 1
    SMALL = 2
    TEST = 3
    EXIT = 4
    H_TEST = 1
    K_TEST = 2
    PRINT = 1
    FILE = 2

    MENU_OPTIONS = (REAL, SMALL, TEST, EXIT)
    TEST_MENU_OPTIONS = (H_TEST, K_TEST)
    OUTPUT_OPTIONS = (PRINT, FILE)

    REAL_GRAPH_PATH = "./roadNet-CA.txt"

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
            |   3. Test cases                          |
            |   4. End                                 |
            |                                          |
            ********************************************
            """
        )

    def _print_test_menu(self):
        print(
            """
            \n
            ********************************************
            |            Demo of test cases            |
            ********************************************
            |                                          |
            |   1. K is unchanged, H increases         |
            |   2. H is unchanged, K increases         |
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

    def _request_test_type(self):
        self._print_test_menu()
        selection = int(input("> Please select test to run: "))
        return self._validate_input(
            "> Please enter correct number for selection: ",
            selection,
            self.TEST_MENU_OPTIONS,
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
        return self._option_process(self.REAL_GRAPH_PATH)

    def _small_option(self):
        print("\nstart testing on small random graph(1000 nodes)...")
        graph_path = TestGraphGenerator().generate()
        return self._option_process(graph_path)

    def _h_test_option(self):
        # generate a file with 100000 hispitals
        hospital_list = []
        hospitals_path = HospitalGenerator(self.REAL_GRAPH_PATH).generate(100000)
        with open(hospitals_path, "r") as f:
            for row in f:
                id = row.split()[0]
                if id == "#":
                    continue
                hospital_list.append(int(id))

        hospital_small_list = set(hospital_list[0:100])  # 100
        hospital_large_list = set(hospital_list)  # 100000
        num_hospital_to_search = 3  # k
        start_node = 0
        hospital_finder = HospitalFinder(self.REAL_GRAPH_PATH)

        print("\n\n---------------------------------------------------")
        print(f"\nTest result for {len(hospital_small_list)} hospitals with k=3")
        hospital_finder.hospitals = hospital_small_list
        hospital_finder.print_result(start=start_node, k=num_hospital_to_search)

        print("\n\n---------------------------------------------------")
        print(f"\nTest result for {len(hospital_large_list)} hospitals with k=3")
        hospital_finder.hospitals = hospital_large_list
        hospital_finder.print_result(start=start_node, k=num_hospital_to_search)

    def _k_test_option(self):
        hospital_finder = HospitalFinder(self.REAL_GRAPH_PATH)
        start_node = 0

        print("\n\n---------------------------------------------------")
        print(f"\nTest result for {len(hospital_finder.hospitals)} hospitals with k=3")
        hospital_finder.print_result(start=start_node, k=3)

        print("\n\n---------------------------------------------------")
        print(f"\nTest result for {len(hospital_finder.hospitals)} hospitals with k=50")
        hospital_finder.print_result(start=start_node, k=50)

    def _test_option(self):
        test_selection = self._request_test_type()
        if test_selection == self.H_TEST:
            self._h_test_option()
        elif test_selection == self.K_TEST:
            self._k_test_option()

        return self._request_type()

    def start(self):
        selection = self._request_type()
        while selection != self.EXIT:
            if selection == self.REAL:
                selection = self._real_option()
            elif selection == self.SMALL:
                selection = self._small_option()
            elif selection == self.TEST:
                selection = self._test_option()

        print("END...")

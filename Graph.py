class Node:
    # records edges that are already created
    taken = []
    def __init__(self, id,is_hospital):
        if id not in Node.taken:
            self.edges = []
            self.id = id
            self.is_hospital = is_hospital
            Node.taken.append(id)
            
        else:
            pass

    def __eq__(self, node):
        if self.id == node.id:
            return True
        else:
            return False

    # make Node objects hashable
    # (Act as dict keys)
    def __hash__(self):
        return self.id

    def __str__(self):
        return 'Node {} {}'.format(self.id, self.is_hospital)

    def __repr__(self):
        return 'Node {} {}'.format(self.id, self.is_hospital)

    def get_id(self):
        return self.id

    def copy(self):
        return Node(self.id,self.is_hospital)
    
    def add_edge(self, node2):
        self.edges.append(node2)
class RoadGraph:
    def __init__(self):
        self.nodes = []

    def add_node(self, new_node):
        self.nodes.append(new_node)

graph = RoadGraph()
with open("./data/roadNet-CA.txt") as f:
    previous_line_str = []
    for line in f:
        line_str = line.split()
        if line_str[0] == '#':
            continue
        print(line_str)
        node1 = Node(line_str[0],False)
        node2 = Node(line_str[1], False)
        node1.add_edge(node2)
        graph.add_node(node1)
        

        


# with open("./data/roadNet-CA.txt") as f:
#     while True:
#         data = f.read(1024)
#         if not data:
#             break
#         print(data)
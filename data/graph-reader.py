
graph = {}
hospital = [7,3,6,9,7878,7979,12121,12222,55569,123,3535,213123,223232,154564,89898,45545,98852,654511,58787,21232,8878,212312,8788,21212,54545,87,87,6332,87897,54642,121,3,545645,138,78,213,21,5,]

class Node(object):
    taken = []
    def __init__(self, id, is_hosptal):
        if id not in Node.taken:
            self.id = id
            self.is_hospital = is_hosptal
            self.taken.append(id)
        def __eq__(self,node):
            if self.id == node.id:
                return True
            else:
                return False
        def __hash__(self):
            return self.id

with open("./roadNet-CA.txt", 'r') as f:
    last_node_id = -1
    temp_list = []
    for row in f:
        x = row.split()
        if x[0] == '#':
            continue
        node_id = int(x[0])
        # print("node: " +  str(node_id))
        if node_id == last_node_id:
            neighbor_node_id = int(x[1])
            neighbor_node = ()
            if neighbor_node_id in hospital:
                neighbor_node = (neighbor_node_id, True)
            else:
                neighbor_node = (neighbor_node_id, False)
            temp_list.append(neighbor_node)
            graph[node_id] = temp_list
            last_node_id = node_id
        else:
            temp_list = []
            neighbor_node_id = int(x[1])
            neighbor_node = ()
            if neighbor_node_id in hospital:
                neighbor_node = (neighbor_node_id, True)
            else:
                neighbor_node = (neighbor_node_id, False)
            temp_list.append(neighbor_node)
            graph[node_id] = temp_list
            last_node_id = node_id

def find_hospitals(graph,start, k):
    flag = k
    path_k = []
    explored = []
    queue = [[start]]
    founded_hospital = []

    if start in hospital:
        k-=1
        path_k.append(start)
        founded_hospital.append(start)
        print("lol")
    while queue and k > 0:
        path = queue.pop(0)
        node = path[-1]
        if node not in explored:
            neighbours = graph[node]
            for neighbour in neighbours:
                if neighbour[1] == False:
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
    if len(path_k) == 0:
        return "no hospital can be found on this starting point"
    if k > 0:
        return "We can only find {} hospitals from this starting point".format(flag - k)
    else:
        return path_k

print(find_hospitals(graph,213155,3))
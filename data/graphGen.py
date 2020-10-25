import networkx as nx
FILENAME = "testGraphs/testfile6.txt"

G = nx.connected_watts_strogatz_graph(1001, 10, 0, )

print("nodes() ============================================")
print(G.nodes())
print("\nedges() ============================================")
edge = G.edges()
print(edge)

open(FILENAME, 'w').close()
for m in edge:
    f = open(FILENAME, 'a')
#    print(m[0], "\t", m[1])
    f.write(str(m[0]))
    f.write("\t")
    f.write(str(m[1]))
    f.write("\n")
    f.close()
print("\nGraph File Created")

f = open(FILENAME, 'r')
i = 1
y = [False] * 1001
for row in f:
    x = row.split()
#    print(x[0])
    if x[0].isdigit() == True:
        if y[int(x[0])] == False:
            y[int(x[0])] = True
for i in range(1000):
    if y[i] == False:
        print(i, "does not have edge")
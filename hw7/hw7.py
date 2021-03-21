inf = float('inf')

def makequeue(V):

    return [[v, inf] for v in V]


def deletemin(Q):
    
    i = Q.index(min(Q, key=lambda x: x[1]))

    return Q.pop(i)[0]


def decreasekey(Q, v):

    # find v in Q and decrease value by 1
    for key_value in Q:
        if key_value[0] == v:
            Q[Q.index(key_value)][1] -= 1
            break


# DPV Figure 4.8 Dijkstra's Shortest Path
# Input: G is a graph (V, E) undirected, 
#        l is a dict of positive edge lengths 
#        s is the source node in V to start from
# Output: for all vertices u reachable from s, dist(u) is set to the distance fro s to u
def dijkstra(G, l, s):
    
    V = G[0]
    E = G[1]

    dist = dict()
    prev = dict()

    for u in V:
        dist[u] = inf
        prev[u] = None
    dist[s] = 0

    H = makequeue(V)
    while len(H): # while H is not empty

        u = deletemin(H)

        for edge in E:

            # only do operations on neighbors of u
            if edge[0] == u:
 
                v = edge[1]

                if dist[v] > dist[u] + l[edge]:
                
                    dist[v] = dist[u] + l[edge]
                    prev[v] = u
                    decreasekey(H, v)

    return dist, prev


# g1_file = input("Graph Data File: ")
# s = input("Source Vertex: ")

output_file = "hw7_out.txt"
g1_file = "dijk_graph20.txt"
test_file = "test_graph.txt"

f_in = open(test_file, "r")
f_out = open(output_file, "w")

# initialize variables
V = set()   # verticies
E = set()   # edges
l = dict()  # positive edge lengths
s = 0       # source vertex

# parse edge data from each line in file
# graph is undirected but src and dst are used for convenience
for edge_data in f_in:

    src, dst, wgt = [ int(x) for x in edge_data.split() ] # source, destination, weight
    edge = (src, dst)
    E.add(edge)
    V.update(edge)
    l[edge] = wgt

G = (V, E) # pack graph data

# run dijkstra's shortest path on generated graph
distances, path = dijkstra(G, l, s)
print(path)
for d in distances:
    
    print("{} {}".format(d, distances[d]))
    
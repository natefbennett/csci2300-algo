import time

# maintain forest of trees
class UnionFind():

    def __init__(self, c):
        self.node_list = []
        self.pi = dict() # store parents
        self.rank = dict()
        self.compressed = c

    # initialize vertex in datastructure
    def makeset(self, x):
        self.node_list.append(x)
        self.pi[x] = x    # initialize parent
        self.rank[x] = 0  # initialize rank

    def find(self, x):

        while x != self.pi[x]: # root check
            x = self.pi[x]

        return x

    # find that uses compression, recursive
    def find_c(self, x):
        
        if x != self.pi[x]: # root check
            self.pi[x] = self.find_c(self.pi[x])

        return self.pi[x]

    # merge x and y
    def union(self, x, y):
        
        if self.compressed:
            r_x = self.find_c(x)
            r_y = self.find_c(y)
        else: 
            r_x = self.find(x)
            r_y = self.find(y)

        if r_x == r_y: return # x and y roots are the same, ignore
        # check which tree is taller and
        # point root of the shorter tree to root of the taller tree
        if self.rank[r_x] > self.rank[r_y]:
            self.pi[r_y] = r_x
        else:
            self.pi[r_x] = r_y
            # increment rank of root if needed
            if self.rank[r_x] == self.rank[r_y]:
                self.rank[r_y] += 1

    def getRootRank(self):
        root = self.find(self.node_list[0]) # pick a node and traverse parents
        return self.rank[root]

    def getHeight(self):
        
        max_height = 0

        # record distance from all nodes to root
        for node in self.node_list:
            
            height = 0
            
            while node != self.pi[node]: # root check
                node = self.pi[node]
                height += 1
            
            if height > max_height: 
                max_height = height
        
        return max_height


# DPV Figure 5.4 Kruskal's Minimum Spanning Tree Algorithm
# Input: G=(V, E) graph connected undirected with edge weights
#        w is a dict of positive edge lengths 
#        c is a boolean to turn path compression on, default off
# Output: A minimum spanning tree defined by the edges X
def kruskal(G, w, c=False):
    
    V, E = G # break graph into vertices and edges
    uf = UnionFind(c) # initialize mst as union find datastructure

    # make singleton sets out of all verticies
    for vertex in V:
        uf.makeset(vertex)
    
    X = dict() # edges of MST with weights

    # sort the edges by weight
    sorted_w = sorted(w.items(), key=lambda item: item[1])

    # loop through edges in increasing order
    for edge, weight in sorted_w:
        
        u, v = edge
        
        # check if compressed
        if c:
            r_u = uf.find_c(u)
            r_v = uf.find_c(v)
        else:
            r_u = uf.find(u)
            r_v = uf.find(v)

        # if root not the same
        if r_u != r_v:
            X[edge] = weight  # add edge to list
            uf.union(u, v) # merge associated trees

    return X, uf


def run(file_name):

    f_in = open(file_name, "r")

    # initialize variables
    V = set()   # verticies
    E = set()   # edges
    w = dict()  # positive edge lengths

    # parse edge data from each line in file
    # graph is undirected but src and dst are used for convenience
    for edge_data in f_in:

        src, dst, wgt = [ int(x) for x in edge_data.split() ] # source, destination, weight
        edge = (src, dst)
        E.add(edge)
        V.update(edge)
        w[edge] = wgt

    G = (V, E) # pack graph data

    # run kruskal to find a MST (minimum spanning tree)
    # without compression
    start_time = time.process_time()
    mst_edges, mst = kruskal(G, w)
    run_time = round(time.process_time() - start_time, 4)
    mst_cost = sum(mst_edges.values())

    # with compression
    start_time = time.process_time()
    mst_edges_c, mst_c = kruskal(G, w, True)
    run_time_c = round(time.process_time() - start_time, 4)
    mst_cost_c = sum(mst_edges_c.values())   

    print("Testing Graph: {}".format(file_name))

    # print results without compression
    print("-Without Compression-")
    print("MST Cost: {} Root Rank: {} Height: {}".format(mst_cost, mst.getRootRank(), mst.getHeight()))
    print("Time: {}\n".format(run_time))

    # print results with compression
    print("-With Compression-")
    print("MST Cost: {} Root Rank: {} Height: {}".format(mst_cost_c, mst_c.getRootRank(), mst_c.getHeight()))
    print("Time: {}\n".format(run_time_c))


print('\n-- Lab 8: Kruskal\'s Algorithm and Union-Find Data Structure --\n')

files = [ "kruskal_graph100.txt",     
          "kruskal_graph1000.txt",    
          "kruskal_graph10000.txt" ]

# test all input files
for file in files:
    run(file)

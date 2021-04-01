import time

class TreeNode():

    def __init__(self, v):
        self.id = v
        self.rank = 0
        self.parent = self

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return "<TreeNode id:{} rank:{} parent:{}>".format(self.id, self.rank, self.parent)

# maintain forest of trees
class UnionFind():

    def __init__(self, c):
        self.node_list = []
        self.compressed = c

    # initialize vertex in datastructure
    def makeset(self, x):
        node = TreeNode(x)
        self.node_list.append(node)

    def find(self, x):

        while x != x.parent: # root check
            x = x.parent

        return x

    # find that uses compression, recursive
    def find_c(self, x):
        
        if x != x.parent: # root check
            x.parent = self.find_c(x.parent)

        return x.parent

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
        if r_x.rank > r_y.rank:
            r_y.parent = r_x
        else:
            r_x.parent = r_y
            # increment rank of root if needed
            if r_x.rank == r_y.rank:
                r_y.rank += 1

    def lookup(self, id):
        return self.node_list[self.node_list.index(TreeNode(id))]

    def getRootRank(self):
        root = self.find(self.node_list[0])
        return root.rank

    def getHeight(self):
        
        height_list = []

        # record distance from all nodes to root
        for node in self.node_list:
            height = 0
            while node != node.parent: # root check
                node = node.parent
                height += 1
            height_list.append(height)
        
        return max(height_list)


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
        # since u and v are just ids we need to look up in node list
        node_u = uf.lookup(u)
        node_v = uf.lookup(v)
        
        # check if compressed
        if c:
            r_u = uf.find_c(node_u)
            r_v = uf.find_c(node_v)
        else:
            r_u = uf.find(node_u)
            r_v = uf.find(node_v)

        # if root not the same
        if r_u != r_v:
            X[edge] = weight  # add edge to list
            uf.union(node_u, node_v) # merge associated trees

    return X, uf

file_name = "kruskal_graph100.txt"
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

print('\n-- Lab 8: Kruskal\'s Algorithm and Union-Find Data Structure --\n')

# print results without compression
print("Without Compression")
print("MST Cost: {} Root Rank: {} Height: {}".format(mst_cost, mst.getRootRank(), mst.getHeight()))
print("Time: {}\n".format(run_time))

# print results with compression
print("With Compression")
print("MST Cost: {} Root Rank: {} Height: {}".format(mst_cost_c, mst_c.getRootRank(), mst_c.getHeight()))
print("Time: {}\n".format(run_time_c))

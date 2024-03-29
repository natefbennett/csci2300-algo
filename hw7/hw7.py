inf = float('inf')

class HeapNode():

    def __init__(self, id, value):
        self.id = id
        self.value = value

    def __lt__(self, other):
        return self.value < other.value

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return "[ {} ]".format(self.value)

    def __repr__(self):
        return "<HeapNode id:{} value:{}>".format(self.id, self.value)


# Implementation of Min Heap using a list to represent a binary tree
# Use as priority queue for Dijkstras shortest path
class MinHeap():

    def __init__(self, v_dict):

        self.b_tree_list = []
        self.size = 0

        for vertex_key in v_dict:
            self.insert( HeapNode(vertex_key, v_dict[vertex_key]) )


    def __str__(self):

        buffer = ""
        for node in self.b_tree_list:
            buffer += str(node)

        return buffer


    # place new node at bottom of tree and let bubble up
    def insert(self, n):

        self.b_tree_list.append(n)
        self.size += 1
        self.bubbleup(n, self.size-1)


    # return the index of the smaller child of node at location: i
    def minchild(self, i):

        left_index = (2*i)+1
        right_index = (2*i)+2 

        # case no children
        if left_index > self.size-1:
            return None
        
        # case one child
        elif right_index > self.size-1:
            return left_index
        
        # case both children
        else:
        
            left_node = self.b_tree_list[left_index]
            right_node = self.b_tree_list[right_index]

            if left_node < right_node:
                return left_index
            else:
                return right_index


    # place HeapNode: x in position: i of heap and let it trickle down
    def siftdown(self, x, i):
    
        child_index = self.minchild(i)
        
        # find position for x by checking if child value smaller than x
        while child_index != None and self.b_tree_list[child_index] < x:
            
            self.b_tree_list[i] = self.b_tree_list[child_index]
            i = child_index
            child_index = self.minchild(i)

        self.b_tree_list[i] = x # insert x in cleared spot


    # place HeapNode: x in position: i of heap and let it bubble up
    def bubbleup(self, x, i):
       
        parent_index = (i-1) // 2

        # while not at root and the parent index larger value than x value
        while i != 0 and self.b_tree_list[parent_index] > x:

            self.b_tree_list[i] = self.b_tree_list[parent_index]
            i = parent_index
            parent_index = (i-1) // 2

        self.b_tree_list[i] = x


    def decreasekey(self, x):

        # locate vertex data in heap
        index = self.b_tree_list.index(x)

        # trickle value up, always assumes decrese in value
        self.bubbleup(x, index)


    # retrun the value and node id at the root
    def deletemin(self):

        if self.size == 0:
            return None
        else:
            id_value = self.b_tree_list[0] # save data for return
            last_node = self.b_tree_list.pop()
            self.size -= 1 # decrease size of heap by one

            # replace root node with rightmost leaf node
            # check if there are still nodes in the heap
            if self.size > 0:
                # put last node in root
                self.b_tree_list[0] = last_node
                # trickle new root down to correct position
                self.siftdown(self.b_tree_list[0], 0)

            return id_value
    

# DPV Figure 4.8 Dijkstra's Shortest Path
# Input: G is a graph (V, E) undirected, 
#        l is a dict of positive edge lengths 
#        s is the source node in V to start from
# Output: for all vertices u reachable from s, dist(u) is set to the distance fro s to u
def dijkstra(G, l, s):
    
    V, E = G # break graph into vertices and edges

    dist = dict() # distance form s
    prev = dict() # previous, for retracing shortest path
    
    # initialize values for distance and previous dicts
    for vertex_id in V:
        dist[vertex_id] = inf
        prev[vertex_id] = None
    dist[s] = 0 # set distance form source to 0

    heap = MinHeap(dist)

    while heap.size > 0: # while heap is not empty

        u = heap.deletemin().id # pop smallest emlement from heap (root)

        for edge in E:

            # only for neighbors of u, v
            if edge[0] == u:
 
                v = edge[1]

                # check if newly found distance less than current set distance
                if dist[v] > dist[u] + l[edge]:
        
                    dist[v] = dist[u] + l[edge]             # update distance dict
                    prev[v] = u                             # 
                    heap.decreasekey(HeapNode(v, dist[v]))  # update distance in heap
                    
    return dist, prev


# returns a list of the graph verticies traversed from the source to vertex v
def getPathList(path, v):
    
    path_list = []
    path_list.append(v)
    next_val = path[v]

    while next_val != None:

        path_list.append(next_val)
        temp = next_val
        next_val = path[temp]
        
    path_list.reverse()

    return path_list


file_name = input("Graph Data File: ")
s = int(input("Source Vertex: "))

f_in = open(file_name, "r")

# initialize variables
V = set()   # verticies
E = set()   # edges
l = dict()  # positive edge lengths

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

for d in distances:
    
    print("path {} {} {}".format(d, distances[d], getPathList(path, d)))

    
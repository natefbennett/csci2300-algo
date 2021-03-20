import sys

sys.setrecursionlimit(10**9)

# Directed Graph Object
class Graph:
	
	# Constructor: takes a set of tuples containg two values, source and destination -> {(v,u),...}
	def __init__(self, E):
		
		# tmp stores to collect edge data
		A = dict()
		V = set()

		# process all edge data
		for edge in E:
			A.setdefault(edge[0], []).append(edge[1]) # create new list if key not exist
			A[edge[0]] = sorted(A[edge[0]]) # maintain order
			V.add(edge[0])
			V.add(edge[1])

		# basic graph data
		self.edges = E
		self.verticies = sorted(list(V))
		self.a_list = A # adjacency list
		
		# dfs data
		self.visited = dict(zip(self.verticies, [False]*len(self.verticies))) # check if node visited for explore()
		self.pre = dict(zip(self.verticies, [-1]*len(self.verticies)))
		self.post = dict(zip(self.verticies, [-1]*len(self.verticies)))
		self.clock = 1

		# scc data
		self.scc_dict_by_vertex = dict(zip(self.verticies, [-1]*len(self.verticies))) # store nodes with scc number
		self.scc_dict_by_id = dict()
		self.scc_list = []
		self.scc_count = 0 # connected component counter
		
		# dag data
		self.dag_edges_list = []

	def previsit(self, v):
		
		# save ordering to pre dict and label connected component
		self.scc_dict_by_vertex[v] = self.scc_count
		self.scc_dict_by_id.setdefault(self.scc_count, []).append(v)
		self.pre[v] = self.clock
		self.clock += 1
		

	def postvisit(self, v):
		
		# save ordering to post dict
		self.post[v] = self.clock
		self.clock += 1


	# DPV Figure 3.3 explore(G,v)
	# Input: G is a graph, v is a node
	# Output: visited[u] is set true for all nodes u reachable from v
	def explore(self, v):

		if not self.visited[v]:
		
			self.visited[v] = True
			self.previsit(v)
			
			# loop over out-edges from this node
			for u in self.a_list[v]:
				self.explore(u)

			self.postvisit(v)


	# DPV Figure 3.5 dfs(G)
	# Depth First Search, explore all nodes in graph
	def dfs(self):

		# reset visited tracker
		for v in self.verticies:
			self.visited[v] = False

		# move through every node in the graph
		for v in self.verticies:
			if not self.visited[v]:
				self.explore(v)
				self.scc_count += 1


	# return SCCs in sorted list form
	def buildSCCList(self):
		scc_list = []
		for scc in self.scc_dict_by_id:
			scc_list.append(sorted(self.scc_dict_by_id[scc]))

		self.scc_list = sorted(scc_list, key=len, reverse=True)


	def updateSCCIDs(self):

		self.buildSCCList() # get sorted order

		updated_scc_dict_by_vertex = dict()
		updated_scc_dict_by_id = dict(zip(range(len(self.scc_list)), self.scc_list))

		# assign new ids by sorted order
		for i, scc in enumerate(self.scc_list):
			# f_out.write("{} {} {}\n".format(i, len(scc), scc))

			for v in scc:
				updated_scc_dict_by_vertex.setdefault(v, i)

		# update graph with new scc numbering
		self.scc_dict_by_vertex = updated_scc_dict_by_vertex
		self.scc_dict_by_id = updated_scc_dict_by_id

	
	def buildDAGEdgeList(self):

		# find all dag edges between SCCs
		for edge in self.edges:

			edge_src_scc = self.scc_dict_by_vertex[edge[0]]
			edge_dst_scc =  self.scc_dict_by_vertex[edge[1]]

			# check if edge destination points to a different scc
			if edge_src_scc != edge_dst_scc:
				scc_edge = (edge_src_scc, edge_dst_scc)
				if scc_edge not in self.dag_edges_list:
					self.dag_edges_list.append(scc_edge)


output_file = "hw6_out.txt"
test_file = "scc_graph20.txt"	
g1_file = "scc_graph100.txt"
g2_file = "scc_graph1000.txt"
g3_file = "scc_graph10000.txt"

f_in = open(g1_file, "r")
f_out = open(output_file, "w")

# initialize edge sets
E = set()
E_reversed = set()

# parse edge data from line in file
for edge_data in f_in:

	src, dst = edge_data.split()
	E.add((int(src), int(dst))) # pack tuple with ints and add to set of edges
	E_reversed.add((int(dst), int(src)))


G = Graph(E)
G_reversed = Graph(E_reversed)

# DPV Section 3.4.2
# Efficient algorithm for decomposing a directed graph into its strongly connected components.
# Step 1: run depth first search on reversed G to find post numbers
G_reversed.dfs()

# Step 2: run depth first search on G, processing the nodes in decreasing order of their post numbers
# print(sorted(G_reversed.post, key=G_reversed.post.get, reverse=True))
G.verticies = sorted(G_reversed.post, key=G_reversed.post.get, reverse=True)
G.dfs()

# prepare data
G.updateSCCIDs() # format data to conform to submission standards
G.buildDAGEdgeList() # find edges connecting sccs
num_sccs = len(G.scc_list)
num_dag_nodes = num_sccs

# ouput results
f_out.write("Number of SCCs: {}\n".format(num_sccs))

for id in G.scc_dict_by_id:
	scc = G.scc_dict_by_id[id]
	f_out.write("{} {} {}\n".format(id, len(scc), scc))

f_out.write("DAG Stats -> nodes: {}; edges: {}\n".format(num_dag_nodes, len(G.dag_edges_list)))
for edge in sorted(G.dag_edges_list):
	f_out.write("SCC edge {} {}\n".format(edge[0], edge[1]))
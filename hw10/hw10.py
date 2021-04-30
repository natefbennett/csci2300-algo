from collections import deque
import sys 

def bfs(s, t, G, R, V):

    V_r, E_r = R
    V_g, E_g = G

    visited = dict()
    prev = dict()

    # initialize visited tracker
    for vertex in V:
        visited[vertex] = False
        prev[vertex] = None

    queue = deque(s) # initialize a queue with source
    visited[s] = True

    while len(queue) > 0:

        u = queue.popleft() # from
        
        # check if vertex is the sink
        if u == t:
            break

        # u -> v   loop through verticies adjacent to u
        for v in V_r[u]:

            edge = (u, v)
            capacity = E_r[edge] # get remaining capacity from residual graph

            # check if vertex where edge is pointing has not been vistited
            # also check if capacity is full
            if not visited[v] and capacity > 0:

                queue.append(v)
                visited[v] = True
                prev[v] = u

    # check if we made it to the sink
    if prev[t] == None: return 0, []

    # get the augmented path and bottle neck value
    bottle_neck = float("inf")
    prev_vertex = t
    path_edges = []

    # stop when source is reached
    while prev_vertex != s:
        v = prev_vertex        # dst
        u = prev[prev_vertex]  # src
        edge = (u, v)
        path_edges.append(edge)
        bottle_neck = min(bottle_neck, E_r[edge])
        prev_vertex = u

    return [ bottle_neck, path_edges ]


def EdmondsKarp(source, sink, G, R, V):

    max_flow = 0
    flow = float('inf')

    while flow != 0:

        flow, path_edges = bfs(source, sink, G, R, V)
        max_flow += flow

        # augment flow along path
        # E_r = R[1]
        for edge in path_edges:
            R[1][edge] -= flow
            R[1][(edge[1], edge[0])] += flow # add flow to residual edge

    return max_flow, R

    
if len(sys.argv) != 4:
    raise ValueError('Incorrect number of command line arguments!')

f, s, t = sys.argv[1:] # exclude name of python file
f_open = open(f, "r")

# initialize variables
V_g = dict()    # Original Graph -> verticie: [adjacent verticies]
E_g = dict()    # Original Graph -> edge: capacity
V_r = dict()    # Residual Graph
E_r = dict()    # Residual Graph
V = set()       # verticies alone

# parse edge data from each line in file
for edge_data in f_open:

    src, dst, capacity = edge_data.split()
    edge = (src, dst)
    capacity = int(capacity)

    V.update(edge) # add src and dst to verticies set

    # set data for original graph
    E_g[edge] = capacity
    V_g.setdefault(src, []).append(dst)
    V_g.setdefault(dst, [])

    # set data for residual graph
    E_r[edge] = capacity
    residual_edge = (edge[1], edge[0])
    E_r[residual_edge] = 0
    V_r.setdefault(src, []).append(dst)
    V_r.setdefault(dst, []).append(src)

G = (V_g, E_g)  # pack graph data
R = [V_r, E_r]  # pack residual graph data

max_flow, R = EdmondsKarp(s, t, G, R, V)

# loop though adjacent verticies to source
flow_from_source = "flow "
all_data = []
for i, v in enumerate(R[0][s]):
    
    edge = (s, v)
    remaining_capacity = R[1][edge]
    base_capacity = G[1][edge]
    edge_flow = base_capacity-remaining_capacity
    data = (s, v, edge_flow)

    # check if edge was used
    if edge_flow == 0: continue

    all_data.append(data)


print(flow_from_source+str(sorted(all_data)).strip('[]'))
print(f"maxflow value {max_flow}")
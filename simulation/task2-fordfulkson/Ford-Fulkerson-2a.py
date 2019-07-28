#
# Ford and Fulkerson Algorithm implemented in Python.
#
import csv
class Edge(object):
    def __init__(self, source, sink, capacity):
        self.source = source
        self. sink = sink
        self.capacity = capacity

    def __repr__(self):
        return "%s -> %s : %d" % (self.source, self.sink, self.capacity)

class Flow(object):

    def __init__(self):
        self.edges = {}
        self.adjacents = {}

    def add_edges(self, source, sink, capacity):
        if source ==sink:
            raise ValueError("Source can not be the Sink.")
        edge = Edge(source, sink, capacity)
        redge = Edge(source, sink, capacity)
        self.edges[edge] = 0
        self.edges[redge] = 0

        if source not in self.adjacents:
            self.adjacents[source] = []
        if sink not in self.adjacents:
            self.adjacents[sink] = []

        self.adjacents[source].append(edge)
        self.adjacents[sink].append(redge)

    def valid_path(self, source, sink, path):
        """ Returns the list of the edges from source to sink """

        if source == sink:
            return path
        for edge in self.adjacents[source]:
            if edge not in path:
                if edge.capacity - self.edges[edge] > 0:
                    return self.valid_path(edge.sink, sink, path + [edge])

        # In case there is no more possible path:
        return None

    def max_flow(self, source, sink):
        """" Update the flow for edges and returns the max_flow """

        path = self.valid_path(source, sink, [])

        while (path):
            # get the maximum possible flow that can be taken from this path:
            max_flow = min([edge.capacity for edge in path])
            for edge in path:
                self.edges[edge] += max_flow
            path = self.valid_path(source, sink, [])

        # Compute all the flows from the neighbors of source:
        return  sum([self.edges[edge] for edge in self.adjacents[source]])


station_capacity = [14,15,9,19,19,8,17,20,16,13,4,5,8,8,19,1,12,16,5,5,15,18,14,15,18,3,7,0,19,8]#the amount of passengers aim at Station(i)
tail_station = {}
K = 35
edges = {}
csv_r = csv.reader(open("buslines.csv","r"))
for line in csv_r:
    t = ("0",line[1])
    if edges.has_key(t):
        edges[t]+=K
    else:
        edges[t] = K

    for i in range(1,len(line)-1):
        t = (str(line[i]),str(line[i+1]))
        if edges.has_key(t):
            edges[t]+=K
        else:
            edges[t] = K

    tail = str(line[len(line)-1])
    if not tail_station.has_key(tail):
        tail_station[tail] = []

    for i in range(1,len(line)-1):
        if str(line[i]) not in tail_station[tail]:
            tail_station[tail].append(str(line[i]))

for k,v in tail_station.items():
    c = 0
    for i in v:
        c+=station_capacity[int(i)-1]
    edges[(k,"31")] = c

edges[("31","32")] = 350
#print(edges)
#print(tail_station)

t1 = Flow()
for k,v in edges.items():
    t1.add_edges(k[0],k[1],v)
print(t1.max_flow("0","32"))

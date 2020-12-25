import sys
import heapq
from collections import defaultdict

class Graph:
    def __init__(self, n):
        self.nodes = set(range(n))
        self.roadmap = defaultdict(dict)

    def add_edge(self, from_node, to_node, duration):

        # [destination city][departure city]
        if duration > 0:
            self.roadmap[(from_node, 'g')][(to_node, 'g')] = duration
            self.roadmap[(from_node, 'o')][(to_node, 'o')] = duration
            self.roadmap[(to_node, 'g')][(from_node, 'g')] = duration
            self.roadmap[(to_node, 'o')][(from_node, 'o')] = duration
        else:
            duration = abs(duration)
            self.roadmap[(from_node, 'o')][(to_node, 'g')] = duration
            self.roadmap[(from_node, 'r')][(to_node, 'o')] = duration
            self.roadmap[(to_node, 'o')][(from_node, 'g')] = duration
            self.roadmap[(to_node, 'r')][(from_node, 'o')] = duration

    def add_quarantine(self, node, red, orange):

        # scenarios where travellers get quarantine at the current node
        self.roadmap[(node, 'g')][(node, 'o')] = orange
        self.roadmap[(node, 'o')][(node, 'r')] = red


def escape(n, graph):
    global spaceship
    visited, travel = defaultdict(int), []

    for city in spaceship:
        # (weight, (city, health code))
        heapq.heappush(travel, (0, (city, 'g')))
        visited[city, 'g'] = 0

    while travel:
        current_weight, min_node = heapq.heappop(travel)
        # optimisation: the visited node already had smaller travelling time
        while travel and (min_node in visited) and (visited[min_node] < current_weight):
            current_weight, min_node = heapq.heappop(travel)

        print('parent', min_node, current_weight)
        for v in graph.roadmap[min_node].keys():
            weight = current_weight + graph.roadmap[min_node][v]

            if v not in visited or weight < visited[v]:
                print('push child', v, weight)
                heapq.heappush(travel, (weight, v))
                visited[v] = weight

    # get the travelling time from 'green city with a space station' to 'green city i'
    return ' '.join([str(visited[i, 'g']) for i in range(n)])

# total number of cities
n = int(sys.stdin.readline())
temapura = Graph(n)

# get travelling duration between cities
s = sys.stdin.readline().split()
for t in s:
    u = t.split(':')
    temapura.add_edge(int(u[0])-1, int(u[1])-1, int(u[2]))

# get quarantine duration for each city
s = sys.stdin.readline().split()
i = 0
for t in s:
    u = t.split(':')
    temapura.add_quarantine(i, int(u[0]), int(u[1]))
    i += 1
    
# get list of cities with spaceship stations
spaceship = []
for t in sys.stdin.readline().split():
    spaceship.append(int(t)-1)

print(escape(n, temapura))
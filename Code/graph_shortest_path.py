import numpy as np

class Graph:

    def __init__(self, vertices):
        self.M = vertices   # Total number of vertices in the graph
        self.graph = []     # Array of edges

    # Add edges
    def add_edge(self, node1, node2, edge):
        self.graph.append([node1, node2, edge])


    # Print the solution
    def print_solution(self, distance, goal=range[self.M]):
        print("Vertex Distance from Source")
        for k in goal:
            print("{0}\t\t{1}".format(k, distance[k]))

    
    def bellman_ford(self, src):
        distance = [float("Inf")] * self.M
        distance[src] = 0

        for _ in range(self.M - 1):
            for node1, node2, edge in self.graph:
                if distance[node1] != float("Inf") and distance[node1] + edge < distance[node2]:
                    distance[node2] = distance[node1] + edge
        for node1, node2, edge in self.graph:
            if distance[node1] != float("Inf") and distance[node1] + edge < distance[node2]:
                print("Graph contains negative weight cycle")
                return

        self.print_solution(distance)
    

    def bellman_ford2(self, src, goal, top_distances=1):
        distance = np.full((top_distances, self.M), float('Inf'))
        distance[:,src] = 0

        for _ in range(self.M - 1):
            for node1, node2, edge in self.graph:
                if np.min(distance[:,node1]) != float("Inf") and np.min(distance[:,node1]) + edge < np.max(distance[:,node2]):
                    index = np.argmax(distance[:,node2])
                    distance[index,node2] = np.min(distance[:,node1]) + edge

        self.print_solution(distance, goal)
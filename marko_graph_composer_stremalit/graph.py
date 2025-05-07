import random

class Vertex:
    def __init__(self, value):
        self.value = value
        self.adjacent = {}  # Dictionary of connected vertices and their weights
        self.neighbors = []  # List of adjacent vertices
        self.neighbors_weights = []  # Corresponding weights for adjacent vertices

    def __str__(self):
        return self.value + ' '.join([node.value for node in self.adjacent.keys()])

    def add_edge_to(self, vertex, weight=0):
        self.adjacent[vertex] = weight

    def increment_edge(self, vertex):
        self.adjacent[vertex] = self.adjacent.get(vertex, 0) + 1

    def get_adjacent_nodes(self):
        return self.adjacent.keys()

    def get_probability_map(self):
        if self.adjacent:
            for vertex, weight in self.adjacent.items():
                self.neighbors.append(vertex)
                self.neighbors_weights.append(weight)

    def next_word(self):
        if not self.neighbors:
            return None  # Return None if no neighbors exist
        return random.choices(self.neighbors, weights=self.neighbors_weights)[0]

class Graph:
    def __init__(self):
        self.vertices = {}  # Dictionary of vertices by value

    def get_vertex_values(self):
        return set(self.vertices.keys())

    def add_vertex(self, value):
        self.vertices[value] = Vertex(value)

    def get_vertex(self, value):
        if value not in self.vertices:
            self.add_vertex(value)
        return self.vertices[value]

    def get_next_word(self, current_vertex):
        next_vertex = self.vertices[current_vertex.value].next_word()
        if next_vertex is None:
            # Fallback: Randomly choose a word from the graph
            all_vertices = list(self.vertices.values())
            return random.choice(all_vertices)  # Choose a random word as a fallback
        return next_vertex

    def generate_probability_mappings(self):
        for vertex in self.vertices.values():
            vertex.get_probability_map()

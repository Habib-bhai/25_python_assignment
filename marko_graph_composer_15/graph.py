import random

class Vertex(object):
    def __init__(self, value):
        self.value = value
        self.adjacent = {}  # nodes that it points to, i.e. keeping record of which vertices(words) area connected with this particular vertex (word), where the keys will be the those words, and their value will be the weight i.e. the frequency with which the word points to that particular vertex.
        self.neighbors = []
        self.neighbors_weights = []

    def __str__(self):
        return self.value + ' '.join([node.value for node in self.adjacent.keys()])


    def add_edge_to(self, vertex, weight=0):
        # adds the particular vertex in the adjacent dictionary with its frequency 
        self.adjacent[vertex] = weight

    def increment_edge(self, vertex):
        # increases the weight, if the vertex is pointing to other one more than once. if it has some frequency that will be incremented if not then it will be defaulted to 0. 
        self.adjacent[vertex] = self.adjacent.get(vertex, 0) + 1

    def get_adjacent_nodes(self):
        return self.adjacent.keys()

    # initializes probability map
    def get_probability_map(self):

        for (vertex, weight) in self.adjacent.items():
            self.neighbors.append(vertex)
            self.neighbors_weights.append(weight)

    def next_word(self):
        return random.choices(self.neighbors, weights=self.neighbors_weights)[0]



class Graph(object):
    def __init__(self):
        # making it empty dictionary, so that we can look up each vertex first in this dictionary
        self.vertices = {}

    def get_vertex_values(self):
        # get all the vertices(words) in the graph.
        return set(self.vertices.keys())

    def add_vertex(self, value):
        self.vertices[value] = Vertex(value)

    def get_vertex(self, value):
        if value not in self.vertices:
            self.add_vertex(value)
        return self.vertices[value]

    def get_next_word(self, current_vertex):
        return self.vertices[current_vertex.value].next_word()

    def generate_probability_mappings(self):
        for vertex in self.vertices.values():
            vertex.get_probability_map()

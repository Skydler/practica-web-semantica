from rdflib import Graph
from constant import NAMESPACES


class OwlMovieRepository():
    @classmethod
    def read(cls, graph_location, namespaces=NAMESPACES):
        graph = Graph()

        graph.parse(str(graph_location), format="turtle")

        return graph

    @classmethod
    def write(self, path_file, graph):
        with open(path_file, "w") as file:
            serialized_graph = graph.serialize(format="turtle").decode("utf-8")
            file.write(serialized_graph)

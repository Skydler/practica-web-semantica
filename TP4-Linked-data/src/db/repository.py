from rdflib import Graph
from constant import NAMESPACES


class OwlMovieRepository():
    @classmethod
    def read(cls, graph_location, namespaces=None, file_format="turtle"):
        graph = Graph()

        if namespaces is not None:
            cls.__bind_namespaces(graph, namespaces)

        graph.parse(str(graph_location), format=file_format)

        return graph

    @classmethod
    def write(cls, path_file, graph, namespaces=None, file_format="turtle"):
        if namespaces is not None:
            cls.__bind_namespaces(graph, namespaces)

        with open(path_file, "w") as file:
            serialized_graph = graph.serialize(
                format=file_format).decode("utf-8")

            file.write(serialized_graph)

    @classmethod
    def __bind_namespaces(cls, graph, namespaces):
        for prefix, uri in NAMESPACES.items():
            graph.bind(prefix, uri)

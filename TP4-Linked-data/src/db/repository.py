from rdflib import Graph


class OwlMovieRepository:
    @classmethod
    def read(cls, source, namespaces=None, file_format="turtle"):
        graph = Graph()

        if namespaces is not None:
            cls.__bind_namespaces(graph, namespaces)

        graph.parse(source, format=file_format)

        return graph

    @classmethod
    def write(cls, path_file, graph, namespaces=None, file_format="turtle"):
        if namespaces is not None:
            cls.__bind_namespaces(graph, namespaces)

        with open(path_file, "w") as file:
            serialized_graph = graph.serialize(format=file_format)

            file.write(serialized_graph.decode("utf-8"))

    @classmethod
    def __bind_namespaces(cls, graph, namespaces):
        for prefix, uri in namespaces.items():
            graph.bind(prefix, uri)

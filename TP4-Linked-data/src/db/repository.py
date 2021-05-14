from rdflib import Graph


class OwlMovieRepository():
    @classmethod
    def read(cls, path_file):
        graph = Graph()
        graph.parse(str(path_file), format="turtle")

        return graph

    @classmethod
    def write(self, path_file, graph):
        with open(path_file, "w") as file:
            serialized_graph = graph.serialize(format="turtle").decode("utf-8")
            file.write(serialized_graph)

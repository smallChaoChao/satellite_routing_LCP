import networkx as nx
import matplotlib.pyplot as plt


class Network:
    def __init__(self, graph_filepath):
        self.graph_filepath = graph_filepath
        self.graph = nx.Graph()
        # for i in range(66):
        #     self.graph.add_node(i, contents=set())

        with open(self.graph_filepath, 'r') as f:
            lines = f.readlines()

        for line in lines:
            line = line.rstrip().split(" ")
            if int(line[0]) not in self.graph.nodes:
                self.graph.add_node(int(line[0]))
            if int(line[1]) not in self.graph.nodes:
                self.graph.add_node(int(line[1]))
            # self.graph.add_edge(int(line[2]), int(line[3]), delay=round(float(line[4]) / 100, 1), width=100)
            self.graph.add_edge(int(line[0]), int(line[1]), width=100)


if __name__ == '__main__':
    G_Iridium = Network('../data_in/slice-1-0-10')
    plt.figure(3, figsize=(25, 15))
    plt.subplot(111)
    pos = nx.spring_layout(G_Iridium.graph)
    nx.draw(G_Iridium.graph, pos, node_color="lightgrey", node_size=2500, font_size=20, with_labels=True)
    edge_labels = nx.get_edge_attributes(G_Iridium.graph, 'delay')
    # edge_labels = nx.get_edge_attributes(G_Iridium.graph)
    nx.draw_networkx_edge_labels(G_Iridium.graph, pos, edge_labels=edge_labels, font_size=15)
    # nx.draw_networkx_edge_labels(G_Iridium.graph, pos, font_size=15)
    plt.show()

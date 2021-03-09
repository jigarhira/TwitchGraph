import itertools
import pandas as pd
import networkx as nx

import matplotlib.pyplot as plt


class TwitchGraph:
    DATA_DIR = './data/twitch_data.csv'
    GRAPH_DIR = './data/twitch_graph.gexf'


    def __init__(self):
        # raw csv data
        self.raw_data = None
        # graph
        self.G = None

    def load_csv_data(self, path=None) -> None:
        """Load Twitch data from CSV file.

        Args:
            path (str, optional): Path to CSV file. Defaults to './data/twitch_data.csv'.
        """
        # default value
        if path is None:
            path = self.DATA_DIR

        # read csv as dictionary of lists
        raw_data = pd.read_csv(path, dtype=str).to_dict(orient='list')

        # remove nan values
        for channel in raw_data:
            raw_data[channel] = [x for x in raw_data[channel] if pd.isna(x) == False]

        self.raw_data = raw_data

    def generate_multigraph(self) -> None:
        """Generates multigraph from raw Twitch data.
        """
        # create MultiGraph
        G = nx.MultiGraph()

        # add channels as nodes to graph
        print('found ' + str(len(self.raw_data.keys())) + ' channels')
        for channel in self.raw_data:
            G.add_node(channel, viewers=len(self.raw_data[channel]))

        # add edges to graph
        pair_count = 0
        pairs = itertools.combinations(self.raw_data, 2)
        total_pairs = int(len(self.raw_data) * (len(self.raw_data) - 1) / 2)
        print('generated ' + str(total_pairs) + ' channel pairs')
        # iterate through channel pairs
        for ch1, ch2 in pairs:                   
            # get the common users in both channels
            common = set(self.raw_data[ch1]).intersection(self.raw_data[ch2])
            # add each edge to graph
            for user in common:
                G.add_edge(ch1, ch2, user=user)
            
            pair_count += 1
            if pair_count % 100 == 0:
                print('added edges for pairing {}/{} ({:.1f}%)'.format(
                    pair_count,
                    total_pairs,
                    100*pair_count/total_pairs
                ))

        self.G = G

    def generate_graph(self) -> None:
        """Generates graph from raw Twitch data.
        """
        # create MultiGraph
        G = nx.Graph()

        # add channels as nodes to graph
        print('found ' + str(len(self.raw_data.keys())) + ' channels')
        for channel in self.raw_data:
            G.add_node(channel, viewers=len(self.raw_data[channel]))

        # add edges to graph
        pair_count = 0
        pairs = itertools.combinations(self.raw_data, 2)
        total_pairs = int(len(self.raw_data) * (len(self.raw_data) - 1) / 2)
        print('generated ' + str(total_pairs) + ' channel pairs')
        # iterate through channel pairs
        for ch1, ch2 in pairs:                   
            # get the number of common users in both channels
            common_users = len(set(self.raw_data[ch1]).intersection(self.raw_data[ch2]))
            # add each edge with weight to graph
            if common_users > 0:
                G.add_edge(ch1, ch2, weight=common_users)            
            
            pair_count += 1
            if pair_count % 100 == 0:
                print('added edges for pairing {}/{} ({:.1f}%)'.format(
                    pair_count,
                    total_pairs,
                    100*pair_count/total_pairs
                ))

        self.G = G

    def save_graph(self, path=None) -> None:
        """Saves graph to GEXF file.

        Args:
            path (str, optional): Path to GEXF file. Defaults to './data/twitch_graph.gexf'.
        """
        # default value
        if path is None:
            path = self.GRAPH_DIR

        # save graph
        nx.write_gexf(self.G, path)

    def load_graph(self, path=None) -> None:
        """Loads graph from GEXF file.

        Args:
            path (str, optional): Path to GEXF file. Defaults to './data/twitch_graph.gexf'.
        """
        # default value
        if path is None:
            path = self.GRAPH_DIR

        # load graph
        self.G = nx.read_gexf(path)

    def plot_graph(self, with_labels=True) -> None:
        """Plot graph using MatplotLib.

        Args:
            with_labels (bool, optional): Plot graph with labels. Defaults to True.
        """
        plt.plot(1)
        nx.draw(self.G, with_labels=with_labels)
        plt.show()



if __name__ == '__main__':
    pass

    # graph = TwitchGraph()

    # print('loading csv')
    # graph.load_csv_data()
    # print('loaded csv')

    # print('generating graph')
    # graph.generate_graph()
    # print('graph generation complete')

    # print('saving graph')
    # graph.save_graph()
    # print('saved graph')

    # graph.plot_graph()
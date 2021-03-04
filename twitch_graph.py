import networkx as nx
import csv
import matplotlib.pyplot as plt


class TwitchGraph:
    DATA_DIR = './data/twitch_data.csv'


    def generate_graph(self):

        G = nx.Graph()
        data = pd.read_csv(self.DATA_DIR, dtype=str).to_dict(orient='list')
        G.add_nodes_from(data)
        plt.plot(1)
        nx.draw(G, with_labels=True)
        plt.show()

    def generate_dict(self) -> dict:     
        """generates dict for corresponding csv
        Args:
            csv ([str]): csv of twitch streamers and their corresponding viewers
        Returns:
            dict: 'streamer': ['viewer_1',..,'viewer_n']
        """        
        data = pd.read_csv(self.DATA_DIR, dtype=str).to_dict(orient='list')
        # remove nan values
        data = self.remove_nan(data)
        return data

    def count_overlap(self, data: dict, min_overlap=300):
        """creates dict 'streamer1': {'streamer2': int, 'streamer3': int}}
        int is number of viewers who watch streamer1 and streamer2 ... 
        Args:
            data (dict): streamer: [viewers1,..,viewern]
            min_overlap (int): minimum number of shared viewers between two streamers
        Returns:
            [type]: returns overlap_data dict
        """        
        overlap_data = {}
        visited_streamers = []
        # organize viewers in set
        for key in data:
            data[key] = set(data[key])

        for key in data:
            templist = {}
            for comparisonKey in data:
                if (comparisonKey != key and comparisonKey not in visited_streamers):
                    # find number of shared viewers between streamer1 and streamer 2
                    overlap_size = len(data[key] & data[comparisonKey])
                    if (overlap_size > min_overlap):
                        templist[comparisonKey] = overlap_size
            overlap_data[key] = templist
            visited_streamers.append(key)
        return overlap_data


if __name__ == '__main__':
    pass
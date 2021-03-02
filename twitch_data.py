import requests
import json
import pandas as pd
import numpy as np

import credentials as cr


class TwitchData:
    DATA_DIR = './data/twitch_data.csv'

    
    def __init__(self):
        self.twitch_data = None

    def get_top_streamers(self, count=100):
        """Uses Twitch API to get the current top streamers

        Args:
            count (int, optional): Number of streamers to get (max 100). Defaults to 100.
        """
        # twitch api endpoint
        endpoint = 'https://api.twitch.tv/helix/streams'
        
        # header for auth
        headers = {
            'Client-ID': cr.client_id,
            'Authorization': 'Bearer ' + cr.app_token
        }
        
        # parameters
        payload = {
            'first': str(count)
        }

        # GET request
        r = requests.get(endpoint, params=payload, headers=headers)

        # convert to UTF-8 (foreign characters)
        # extract streamer channel name
        #json_data = json.loads(r.text.encode('utf-8'))
        #return [x['user_name'] for x in json_data['data']]
        return [x['user_name'] for x in r.json()['data']]

    def get_viewers(self, channel:str) -> list:
        """Get list of viewers for a channel.

        Args:
            channel (str): Channel name.

        Returns:
            list: List of channel viewers.
        """
        # channel chat endpoint
        endpoint = 'http://tmi.twitch.tv/group/user/'+ channel.lower() +'/chatters'

        # GET request
        r = requests.get(endpoint)
        
        # check for response (foreign channels can fail)
        if r.text != '':
            print('retrieved viewers for: ' + channel)
            return r.json()['chatters']['viewers']
        else:
            return None

    def generate_twitch_data(self, channels:list):
        """Generate channel viewers data from list of channel names.

        Args:
            channels (list): List of channel names.
        """
        self.twitch_data = {}
        
        # iterate over channels
        for channel in channels:
            # get channel viewers
            viewers = self.get_viewers(channel)
            # check if viewers were returned
            if viewers is None:
                continue

            # append to dictionary
            self.twitch_data[channel] = viewers
    
    def remove_nan(self, data:dict) -> dict:
        """Removes nan values from dictionary of lists.

        Args:
            data (dict): Dictionary of lists.

        Returns:
            (dict): Dictionary of lists.
        """
        for key in data:
            data[key] = [x for x in data[key] if pd.isna(x) == False]

        return data
    
    def append_data(self, new_data:dict):
        """Adds new Twitch data to csv file.

        Args:
            new_data (dict): New Twitch data.
        """
        # load data file
        try:
            data = pd.read_csv(self.DATA_DIR, dtype=str).to_dict(orient='list')
        # create file if it does not exist
        except FileNotFoundError:
            open(self.DATA_DIR, 'x')
            data = {}
        # create empty DataFrame if file is empty
        except pd.errors.EmptyDataError:
            data = {}

        # remove nan values from data
        data = self.remove_nan(data)

        # append new data
        for channel in new_data:
            # check if channel already exists
            if channel in data:
                # combine lists without duplicates
                data[channel] = list(set(data[channel]) | set(new_data[channel]))
            else:
                # create new channel entry
                data[channel] = new_data[channel]

        # convert dict to DataFrame
        data = pd.DataFrame(dict([(x, pd.Series(y)) for x, y in new_data.items()]))

        # save to file
        data.to_csv(self.DATA_DIR, index=False)


if __name__ == '__main__':
    pass
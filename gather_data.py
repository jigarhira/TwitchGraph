from twitch_data import TwitchData


def main():
    data = TwitchData()

    # get current top streamers
    print('getting top streamers')
    channels = data.get_top_streamers()
    print('retrieved top ' + str(len(channels)) + ' streamers')

    # get the channel viewers
    data.generate_twitch_data(channels)

    # add data to csv
    print('adding new data to csv')
    data.append_data(data.twitch_data)
    print('done')

    # clean_data = data.generate_dict()
    # overlap_data = data.count_overlap(clean_data)
    # print(overlap_data)

if __name__ == '__main__':
    main()
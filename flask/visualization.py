# from crypt import methods
from itertools import count
from itertools import islice
import collections



# 총 플레이 시간, 구매한 게임 수
def show_total_playtime_count(played_games):

    total_playtime = 0
    for i in played_games:
        total_playtime += played_games[i]['playtime_forever']

    game_count = len(played_games)

    return str(total_playtime), str(game_count)




# 게임별 플레이 시간
def show_playtime_chart(played_games):

    game_by_time = {}

    for i in played_games:
        game_by_time[i] = [played_games[i]['name'],
                           played_games[i]['playtime_forever']]

    game_by_time = dict(sorted(game_by_time.items(),
                        key=lambda x: x[1][1], reverse=True))
    game_by_time = dict(islice(game_by_time.items(), 10))

    playtime_label = []
    playtime_data = []

    for key, value in game_by_time.items():
        playtime_label.append(value[0])
        playtime_data.append(value[1])

    return playtime_label, playtime_data


# 구매한 게임의 장르 비율
def show_genre_chart(played_games):
    genre_json = {}
    genre_list = []
    for i in played_games:
        genre_json[i] = played_games[i]['genres']

    for i in genre_json:
        for j in range(len(genre_json[i])):
            genre_list.append(genre_json[i][j]['description'])

    genre_count = dict(collections.Counter(genre_list))
    genre_count = dict(
        islice(sorted(genre_count.items(), key=lambda x: x[1], reverse=True), 10))

    label = []
    data = []

    for key, value in genre_count.items():
        label.append(key)
        data.append(value)

    return label, data


# 구매한 게임의 게임회사 비율
def show_publisher_chart(played_games):

    publishers = {}

    temp_publishers = {}
    for game in played_games:
        for p in played_games[game]['publishers']:
            if p in temp_publishers.keys():
                temp_publishers[p] += 1
            else:
                temp_publishers[p] = 1

    temp_publishers = sorted(temp_publishers.items(),
                             key=lambda item: item[1], reverse=True)

    publishers_label = []
    publishers_data = []

    for publisher in temp_publishers:
        publishers_label.append(publisher[0])
        publishers_data.append(publisher[1])

    publishers = {
        "label": publishers_label[:10],
        "data": publishers_data[:10]
    }

    return publishers


# 게임 태그의 워드클라우드
def show_wordcloud(played_games):

    worddata = {}
    description = []
    for i in played_games:
        for j in range(len(played_games[i]['categories'])):
            description.append(played_games[i]['categories'][j]['description'])

    description = dict(collections.Counter(description))
    word = []

    for key, value in description.items():
        word.append({'x': key, 'value': value})

    worddata['wordarray'] = word

    return worddata

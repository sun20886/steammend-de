import json
from urllib.request import urlopen
from http.client import HTTPResponse
from flask import Flask, render_template, request, jsonify
from itertools import islice

app = Flask(__name__)

KEY = "04BED6808829E729BD9E495AB1EBBD8C"
steamid64 = 76561198073180731


# user id로 profile에서 game_list 받아오기
# get_playedgame_details에서 중첩 함수로 사용
def get_playedgames_by_steamid(steamid64):
    steamid = str(steamid64)
    url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key=" + \
        KEY+"&steamid="+steamid+"&l=english"
    HTTPResponse = urlopen(url)
    played_games = json.load(HTTPResponse)['response']['games']

    app_list = {}

    for game in played_games:
        app_list[game['appid']] = game['playtime_forever']

    # print(app_list)
    return app_list


# game인 것들만 app detail 받아오기 
# get_playedgame_details에서 중첩 함수로 사용
def get_appdetail_by_appid(appid):

    appid = str(appid)
    url = "https://store.steampowered.com/api/appdetails?appids="
    HTTPResponse = urlopen(url+appid)
    # if json.load(HTTPResponse)[appid]['success']==True:
    detail_data = json.load(HTTPResponse)[appid]
    # print(appid, detail_data.keys())

    if detail_data['success'] == True:
        if detail_data['data']['type'] == 'game':
            return detail_data['data']
        else:
            return "not game"


def get_playedgame_details(steamid64):
    played_games = get_playedgames_by_steamid(steamid64)
    played_games_detail = {}

    if len(played_games) >= 1:
        for appid in played_games.keys():
            app_detail = get_appdetail_by_appid(appid)

            try:
                played_games_detail[appid] = {
                    "name": app_detail['name'],
                    "steam_appid": app_detail['steam_appid'],
                    "playtime":played_games[appid],
                    "publishers": app_detail['publishers'],
                    "categories": app_detail['categories'],
                    "genres": app_detail['genres'],
                    }
            except:
                pass

    return played_games_detail

@app.route('/playtime', methods = ['GET', 'POST'])
def game_by_time():
    played_games_detail = get_playedgame_details(steamid64)
    game_by_time = {}
    for i in  played_games_detail:
        game_by_time[i] = [played_games_detail[i]['name'],played_games_detail[i]['playtime']]


    game_by_time = dict(sorted(game_by_time.items(), key = lambda x: x[1][1], reverse = True))
    game_by_time = dict(islice(game_by_time.items(),10))

    label = []
    data = []
    
    for key, value in game_by_time.items():
        label.append(value[0])
        data.append(value[1])

#     return jsonify(game_by_time)
    return render_template('piechart.html', label = label, data = data)

if __name__ == '__main__':
    app.run()

# test용
# played_games_detail = get_playedgame_details(76561198073180731)
# game_by_time()
# get_playedgame_details(76561197960297794)

# print(type(get_appdetail_by_appid(49520)))
# get_playedgames_by_steamid(76561198073180731)
# get_playedgame_details(76561198073180731)
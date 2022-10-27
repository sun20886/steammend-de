import json
from urllib.request import urlopen
from http.client import HTTPResponse
from flask import Flask, render_template, request, jsonify
from itertools import islice
import collections

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

@app.route('/playtime2', methods = ['GET', 'POST'])
def genre_count():
    played_games_detail = get_playedgame_details(steamid64)
    genre_json = {}
    genre_list = []
    for i in  played_games_detail:
      genre_json[i] = played_games_detail[i]['genres']
      for i in genre_json:
          for j in range(len(genre_json[i])):
              genre_list.append(genre_json[i][j]['description'])

    genre_count = dict(collections.Counter(genre_list))
    genre_count = dict(islice(sorted(genre_count.items(), key = lambda x: x[1], reverse = True),10))

    label = []
    data = []

    for key, value in genre_count.items():
        label.append(key)
        data.append(value)

#     return jsonify(game_by_time)
    return render_template('radarchart.html', label = label, data = data)

if __name__ == '__main__':
    app.run()

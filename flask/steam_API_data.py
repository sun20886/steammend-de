import json
from urllib.request import urlopen
from http.client import HTTPResponse


# KEY = API키 입력


def get_playedgames_by_steamid(steamid64):
    steamid = str(steamid64)
    url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key=" + \
        KEY+"&steamid="+steamid+"&l=english"
    HTTPResponse = urlopen(url)
    played_games = json.load(HTTPResponse)['response']['games']

    app_list = {}

    for game in played_games:
        app_list[game['appid']] = game['playtime_forever']

    return app_list


def get_appdetail_by_appid(appid):

    appid = str(appid)
    url = "https://store.steampowered.com/api/appdetails?appids="
    HTTPResponse = urlopen(url+appid)
    detail_data = json.load(HTTPResponse)[appid]

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
                app_detail['playtime_forever'] = played_games[appid]
                played_games_detail[appid] = app_detail
            except:
                pass

    return played_games_detail

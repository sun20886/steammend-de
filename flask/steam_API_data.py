import json
from urllib.request import urlopen
from http.client import HTTPResponse

# steamid = 76561198073180731 # test1용
# steamid = 76561197960297794 # test2용

KEY = "04BED6808829E729BD9E495AB1EBBD8C"


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
    # steamid = str(user_steamid)
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


# print(type(get_appdetail_by_appid(49520)))
# get_playedgames_by_steamid(76561198073180731)
# get_playedgame_details(76561198073180731)

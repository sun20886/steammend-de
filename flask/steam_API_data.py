import json
from urllib.request import urlopen
from http.client import HTTPResponse


# KEY = API키 입력
KEY = "04BED6808829E729BD9E495AB1EBBD8C"


def get_play_times_by_steamid(steamid64):
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
    HTTPResponse = urlopen(url+appid+"&l=english")
    detail_data = json.load(HTTPResponse)[appid]

    if detail_data['success'] == True:
        if detail_data['data']['type'] == 'game':
            return detail_data['data']
        else:
            return {"detail_data":"type of this app is not game"}


def get_all_played_games(steamid64):
    played_games = get_play_times_by_steamid(steamid64)
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


def get_top5_playtime_games(steamid64):
    played_games = get_play_times_by_steamid(steamid64)

    sorted_list=sorted(played_games.items(), key=lambda item: item[1], reverse=True )
    top_playtime_games={}

    count_of_played_games=len(sorted_list)

    if count_of_played_games>=5:

        count=0
        while len(top_playtime_games)<5:
            appid=sorted_list[count][0]
            app_detail = get_appdetail_by_appid(appid)

            try:
                app_detail['playtime_forever'] = played_games[appid]
                top_playtime_games[appid] = app_detail
            except:
                pass
            
            count+=1
                
    
    elif count_of_played_games==0:
        return None

    else :
        count=1
        for i in sorted_list:
            appid=i[0]
            app_detail = get_appdetail_by_appid(appid)

            try:
                app_detail['playtime_forever'] = played_games[appid]
                top_playtime_games[appid] = app_detail
            except:
                pass

    return top_playtime_games

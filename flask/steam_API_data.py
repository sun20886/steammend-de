import requests

import config


# KEY = API키 입력
KEY = config.STEAM_API_KEY


def get_play_times_by_steamid(steamid64):
    steamid = str(steamid64)
    url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key=" + \
        KEY+"&steamid="+steamid+"&l=english"

    r = requests.get(url)
    
    if len(r.json()['response'])==0:
        return False
    
    played_games = r.json()['response']['games']
    app_list = {}

    for game in played_games:
        app_list[game['appid']] = game['playtime_forever']

    return app_list


def get_appdetail_by_appid(appid):

    appid = str(appid)
    url = "https://store.steampowered.com/api/appdetails?appids="
    response = requests.get(url+appid+"&l=english")


    try:
        detail_data = response.json()[appid]
        if detail_data['success'] == True:
            if detail_data['data']['type'] == 'game':
                return detail_data['data']
    except:
        print("get_appdetail_by_appid exception : exception", appid)

    


def get_all_played_games(steamid64):
    played_games = get_play_times_by_steamid(steamid64)

    played_games_detail = {}

    failed=[]

    if len(played_games) >= 1:
        for appid in played_games.keys():

            try:
                app_detail = get_appdetail_by_appid(appid)
                app_detail['playtime_forever'] = played_games.get(appid)
                played_games_detail[appid] = app_detail
            
            except:
                print("get_all_played_games : exception", appid)

    return played_games_detail


def get_top5_playtime_games(steamid64):
    played_games = get_play_times_by_steamid(steamid64)

    not_top5 = list(played_games.keys())

    playtime_sorted_list = sorted(
        played_games.items(), key=lambda item: item[1], reverse=True)

    top5_playtime_games = {}

    failed=[]

    count_of_played_games = len(playtime_sorted_list)
    

    if count_of_played_games >= 5:
        
        count = 0
        while True:
            if len(top5_playtime_games)==5:
                break
            
            appid = playtime_sorted_list[count][0]

            try: 
                app_detail = get_appdetail_by_appid(appid)
                app_detail['playtime_forever'] = played_games.get(appid)
                top5_playtime_games[appid] = app_detail
                not_top5.remove(appid)
            except:
                print("count_of_played_games : exception", appid)
                
            count += 1  
                
    
            

    else:
        
        for playtime_data in playtime_sorted_list:
            appid = playtime_data[0]

            try: 
                app_detail = get_appdetail_by_appid(appid)  
                app_detail['playtime_forever'] = played_games.get(appid)
                top5_playtime_games[appid] = app_detail
            except:
                print("count_of_played_games : exception", appid)
                

    return top5_playtime_games, not_top5

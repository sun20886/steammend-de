import recommend
import steam_API_data
import dao 


def get_main_recomm(games):
    return recommend.get_main_recomm(games)


def get_my_recomm(games):
    return recommend.get_my_recomm(games)


def get_top5_playtime_games(steamid64):
    return steam_API_data.get_top5_playtime_games(steamid64)


def get_all_played_games(steamid64):
    return steam_API_data.get_all_played_games(steamid64)


def get_all_games(start):
    return dao.get_all_games(start)


def get_free_games(start):
    return dao.get_free_games(start)


def get_sale_games(start):
    return dao.get_sale_games(start)


def get_new_games(start):
    return dao.get_new_games(start)


def search_games_by_keyword(keyword, start):
    return dao.search_games_by_keyword(keyword, start)
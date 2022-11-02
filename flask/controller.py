import recommend
import steam_API_data
import dao


def get_recommendations(appid):
    return recommend.get_recommendations(appid)


def get_played_games(steamid64):
    return steam_API_data.get_playedgame_details(steamid64)


def get_all_games():
    return dao.get_all_games()


def get_free_games():
    return dao.get_new_games()


def get_sale_games():
    return dao.get_sale_games()


def get_new_games():
    return dao.get_new_games()


def search_games_by_keyword(keyword):
    return dao.search_games_by_keyword(keyword)

import recommend
import steam_API_data
import elk


def get_recommendations(appid):
    return recommend.get_recommendations(appid)


def get_played_games(steamid64):
    return steam_API_data.get_playedgame_details(steamid64)


def get_all_top_seller_games():
    return elk.get_all_top_seller_games()


def search_games_by_keyword(keyword):
    return elk.search_games_by_keyword(keyword)

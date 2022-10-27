from elasticsearch import Elasticsearch
# from pandasticsearch import Select

es = Elasticsearch(
    hosts=["http://127.0.0.1:9200"],

)


def get_all_top_seller_games():

    doc = {"query": {"match_all": {}}}

    res = es.search(index='game_list01', body=doc, size=2226)

    return res


def search_games_by_keyword(keyword):

    doc = {"query": {"match": {"name": keyword}}}

    res = es.search(index='game_list01', body=doc, size=2226)

    return res

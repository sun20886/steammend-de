from elasticsearch import Elasticsearch
import json
# from pandasticsearch import Select

es = Elasticsearch(
    hosts=["http://127.0.0.1:9200"],
)


# 모든 게임 받아오기
def get_all_games():

    doc = {"query": {"match_all": {}}}
    res = es.search(index='top_seller_games_02', body=doc, size=2226)

    return res


# 무료 게임 받아오기
def get_free_games():

    doc = {"query": {"term": {"is_free": {"value": "true"}}}}
    res = es.search(index="top_seller_games_02", body=doc, size=2226)

    list = []
    for hit in res['hits']['hits']:
        list.append(hit["_source"])

    freegame = json.dumps(list, ensure_ascii=True)

    return freegame


# sale 중인 게임 받아오기
def get_sale_games():
    doc = {"query": {"range": {"price_overview.discount_percent": {"gt": 0}}}}
    res = es.search(index="top_seller_games_02", body=doc, size=2226)

    list = []
    for hit in res['hits']['hits']:
        list.append(hit["_source"])

    salegame = json.dumps(list, ensure_ascii=True)

    return salegame


# new game 받아오기(2022년 10월 출시된 게임)
def get_new_games():
    doc = {"query": {"bool": {"must": [{"wildcard": {"release_date.date": {
        "value": "Oct"}}}, {"term": {"release_date.date": {"value": "2022"}}}]}}}
    res = es.search(index="top_seller_games_02", body=doc, size=2226)

    list = []

    for hit in res['hits']['hits']:
        list.append(hit["_source"])

    newgame = json.dumps(list, ensure_ascii=True)
    return newgame


# 게임 이름으로 검색
def search_games_by_keyword(keyword):

    doc = {"query": {"match": {"name": keyword}}}
    res = es.search(index='top_seller_games_02', body=doc, size=2226)

    list = []
    for hit in res['hits']['hits']:
        list.append(hit["_source"])

    keywordgame = json.dumps(list, ensure_ascii=True)

    return keywordgame

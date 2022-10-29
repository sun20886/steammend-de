from flask import Flask, request, jsonify, render_template
from elasticsearch import Elasticsearch
import json

es = Elasticsearch()
app = Flask(__name__)

# 모든 게임 받아오기
@app.route('/all', methods = ['GET','POST'])
def get_all_top_seller_games():

    doc = {"query": {"match_all": {}}}

    res = es.search(index='top_seller_games', body=doc, size=2226)

    list = []
    for hit in res['hits']['hits']:
        list.append(hit["_source"])
    
    allgame = json.dumps(list, ensure_ascii=True)
    
    return allgame

# keyword 받아서 받아오기
@app.route('/keyword', methods = ['GET','POST'])
def search_games_by_keyword():

    keyword = request.form.get("keyword")
    doc = {"query": {"match": {"name": keyword}}}

    res = es.search(index='top_seller_games', body=doc, size=2226)

    list = []
    for hit in res['hits']['hits']:
        list.append(hit["_source"])
    
    keywordgame = json.dumps(list, ensure_ascii=True)

    return keywordgame

# 무료 게임 받아오기
@app.route('/free', methods = ['GET','POST'])
def get_free_game():
    doc = {"query":{"term":{"is_free":{"value":"true"}}}}
    res = es.search(index="top_seller_games", body=doc, size=2226)
    
    list = []
    for hit in res['hits']['hits']:
        list.append(hit["_source"])
    
    freegame = json.dumps(list, ensure_ascii=True)
    
    return freegame
#    return render_template("test.html", freegame = freegame) # html 렌더링 테스트용

# sale 중인 게임 받아오기
@app.route('/sale', methods = ['GET','POST'])
def get_sale_game():
    doc = {"query":{"range":{"price_overview.discount_percent":{"gt":0}}}}
    res = es.search(index="top_seller_games", body=doc, size=2226)
    
    list = []
    for hit in res['hits']['hits']:
        list.append(hit["_source"])
    
    salegame = json.dumps(list, ensure_ascii=True)
            
    return salegame
#    return render_template("test.html", salegame = salegame) # html 렌더링 테스트용

# new game 받아오기(2022년 10월 출시된 게임)
@app.route('/new', methods = ['GET','POST'])
def get_new_game():
    doc = {"query":{"bool":{"must":[{"wildcard":{"release_date.date":{"value":"Oct"}}},{"term":{"release_date.date":{"value":"2022"}}}]}}}
    res = es.search(index="top_seller_games", body=doc, size=2226)
    
    list = []
    
    for hit in res['hits']['hits']:
        list.append(hit["_source"])
    
    newgame = json.dumps(list, ensure_ascii=True)
    return newgame 

#    return render_template("test.html", newgame = newgame) # html 렌더링 테스트용

if __name__ == "__main__":
    app.run()
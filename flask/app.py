from flask import Flask, make_response, request, render_template
from flask_restx import Resource, Api, reqparse, fields

import controller
import visualization as vs
import json
import redis


# Flask 객체 생성
app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False
api = Api(app, version='1.0', title='steammend-swagger',
          description='steammend-swagger', doc='/api-docs')

'''
# Swagger
http://127.0.0.1:5000/api-docs
'''

recomm_api = api.namespace('recomm', description='recomm-API')
played_game_api = api.namespace('played', description='played-API')
filter_game_api = api.namespace('filter', description='filter-API')
search_game_api = api.namespace('search', description='search-API')


@app.route("/tospring")
def spring():
    return "test"


@app.route("/login-check/<id>", methods=['GET', 'POST'])
def login_check(id):
    '''
    redis routing
    '''
    # password는 설정
    conn = redis.StrictRedis(
        host='localhost', password='abcd1234', port=6379, db=0)
    # 세션 존재하는 경우 판별
    # return login 상태면 steam id, 아닌 경우 no login
    if len(conn.keys()) != 0:
        # 세션이 존재하는 경우 key 가져옴
        for i in conn.keys(pattern='*spring:session:sessions:*'):
            if "expires" not in str(i):
                sessionId = str(i)
                sessionId = sessionId[2:len(sessionId)-1]
                break

        if str(conn.hget(name=sessionId, key="sessionAttr:"+id)) != "b''":
            steamId = str(conn.hget(name=sessionId, key="sessionAttr:"+id))
            steamId = steamId[3:len(steamId)-2]

            return steamId
        else:
            return 'no login'
    else:
        return 'no login'


@recomm_api.route("/<int:appid>", methods=["get", "post"])
@recomm_api.param('appid', '비슷한 게임들을 추천받으려는 기준 게임 appid')
class Recomm(Resource):
    '''
    게임 추천 api 
    http://127.0.0.1:5000/recomm/<appid>
    '''

    def get(self, appid):
        result = controller.get_recommendations(appid)
        result = result.to_json(orient='records')
        result = json.dumps(result, ensure_ascii=False)
        res = make_response(result)
        return res


@played_game_api.route("/<string:steamid64>", methods=["get"])
@played_game_api.param('steamid64', "플레이한 게임 데이터를 가져오고자 하는 유저의 steam id.")
class PlayedGames(Resource):
    '''
    steam user가 플레이한 게임 데이터 반환 api
    http://127.0.0.1:5000/played/<user_steamid>
    '''

    def get(self, steamid64):
        result = controller.get_played_games(steamid64)
        res = make_response(result)
        return res


@filter_game_api.route("/", methods=["get"])
class AllGames(Resource):
    '''
    전체 top seller games 반환 api
    http://127.0.0.1:5000/filter
    '''

    def get(self):
        result = controller.get_all_games()

        list = []
        for hit in result['hits']['hits']:
            list.append(hit["_source"])

        allgames = json.dumps(list, ensure_ascii=False)

        res = make_response(allgames)
        return res


@filter_game_api.route("/free", methods=["get"])
class FreeGames(Resource):
    '''
    top seller games 중 무료인 게임 반환 api
    http://127.0.0.1:5000/filter/free
    '''

    def get(self):
        result = controller.get_free_games()
        res = make_response(result)
        return res


@filter_game_api.route("/sale", methods=["get"])
class SaleGames(Resource):
    '''
    top seller games 중 세일중인 게임 반환 api
    http://127.0.0.1:5000/filter/sale
    '''

    def get(self):
        result = controller.get_sale_games()
        res = make_response(result)
        return res


@filter_game_api.route("/new", methods=["get"])
class NewGames(Resource):
    '''
    top seller games 중 새로 출시된 게임(2022년 10월 출시된 게임) 반환 api
    http://127.0.0.1:5000/filter/new
    '''

    def get(self):
        result = controller.get_new_games()
        res = make_response(result)
        return res


@search_game_api.route("/", methods=["get"])
class SearchGame(Resource):
    '''
    게임 이름 검색 api
    http://127.0.0.1:5000/search/<keyword>
    '''

    def get(self):
        keyword = request.form.get("keyword")
        result = controller.search_games_by_keyword(keyword)
        res = make_response(result)
        return res


@app.route('/charts/<string:steamid64>', methods=['get', 'post'])
def show_charts(steamid64):
    '''
    대시보드 시각화 api
    http://127.0.0.1:5000/charts/76561198073180731 
    '''
    played_games = controller.get_played_games(steamid64)

    total_playtime, total_count = vs.show_total_playtime_count(played_games)
    playtime_label, playtime_data = vs.show_playtime_chart(played_games)
    genre_label, genre_data = vs.show_genre_chart(played_games)
    publishers = vs.show_publisher_chart(played_games)
    wordcloud_data = vs.show_wordcloud(played_games)

    return render_template('index.html', total_playtime=total_playtime, total_count=total_count, check="check test", playtime_label=playtime_label, playtime_data=playtime_data, genre_label=genre_label, genre_data=genre_data, publishers=publishers, wordcloud_data=wordcloud_data)


if __name__ == '__main__':
    app.run(debug=True)

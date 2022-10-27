from flask import Flask, make_response, request
from flask_restx import Resource, Api, reqparse, fields

# import recommend
import controller
import json

# Flask 객체 생성
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
api = Api(app, version='1.0', title='steammend-swagger',
          description='steammend-swagger', doc='/api-docs')

recomm_api = api.namespace('recomm', description='recomm-API')
played_game_api = api.namespace('played', description='played-API')
filter_game_api = api.namespace('filter', description='filter-API')
search_game_api = api.namespace('search', description='search-API')
# Swagger
# http://127.0.0.1:5000/api-docs


# http://127.0.0.1:5000/recomm/<appid>
# @app.route("/recomm/<appid>", methods=["get", "post"])
@recomm_api.route("/<int:appid>", methods=["get", "post"])
@recomm_api.param('appid', '비슷한 게임들을 추천받으려는 기준 게임 appid')
class Recomm(Resource):
    # @recomm_api.response(200, "success", fields.List())
    def get(self, appid):
        result = controller.get_recommendations(appid)
        result = result.to_json(orient='records')
        result = json.dumps(result, ensure_ascii=False)
        res = make_response(result)
        return res

# http://127.0.0.1:5000/played/<user_steamid>


@played_game_api.route("/<string:steamid64>", methods=["get"])
@played_game_api.param('steamid64', "플레이한 게임 데이터를 가져오고자 하는 유저의 steam id.")
class PlayedGame(Resource):
    def get(self, steamid64):
        result = controller.get_played_games(steamid64)
        res = make_response(result)
        return res


@filter_game_api.route("/", methods=["get"])
class GameFilter(Resource):
    # http://127.0.0.1:5000/filter
    def get(self):
        result = controller.get_all_top_seller_games()
        print(len(result))
        res = make_response(result)
        return res

# @search_game_api.route("/<string:keyword>", methods=["get"])

# http://127.0.0.1:5000/search?keyword=


@search_game_api.route("/", methods=["get"])
class SearchGame(Resource):
    def get(self):
        keyword = request.args.get('keyword', type=str)
        result = controller.search_games_by_keyword(keyword)
        print(len(result))
        res = make_response(result)
        return res


if __name__ == '__main__':
    app.run(debug=True)

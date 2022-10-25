from dataclasses import field, fields
from distutils.log import debug
from flask import Flask, make_response
from flask_restx import Resource, Api, reqparse, fields
# from flask_restplus import Resource, Api

import recommend
import json

# Flask 객체 생성
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
api = Api(app, version='1.0', title='recomm-swagger',
          description='recomm-swagger', doc='/api-docs')

recomm_api = api.namespace('recomm', description='recomm-API')

# Swagger
# http://127.0.0.1:5000/api-docs

# http://127.0.0.1:5000/recomm/<appid>


# @app.route("/recomm/<appid>", methods=["get", "post"])
@recomm_api.route("/<int:appid>", methods=["get", "post"])
@recomm_api.param('appid', '비슷한 게임들을 추천받으려는 기준 게임 appid')
class Recomm(Resource):
    # @recomm_api.response(200, "success", fields.List())
    def get(self, appid):
        result = recommend.get_recommendations(appid)
        result = result.to_json(orient='records')
        result = json.dumps(result, ensure_ascii=False)
        res = make_response(result)
        return res


if __name__ == '__main__':
    app.run(debug=True)

from distutils.log import debug
from flask import Flask, make_response
# from flask_restx import Resource, Api, reqparse
# from flask_restplus import Resource, Api

import recommend
import json

# Flask 객체 생성
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
# api = Api(app, version='1.0')

# test_api = api.namespace('test')

# http://127.0.0.1:5000/test/appid


@app.route("/test/<appid>", methods=["get", "post"])
# class Test(Resource):
def test(appid):
    print("intro 실행 -------")
    result = recommend.get_recommendations(int(appid))

    result = result.to_json(orient='records')
    print(result)
    result = json.dumps(result, ensure_ascii=False)
    res = make_response(result)
    return res


if __name__ == '__main__':
    app.run(debug=True)

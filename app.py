from flask import Flask
from flask_restful import Api, Resource
from flasgger import Swagger
from flasgger.utils import swag_from
from flask_restful_swagger import swagger
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
api = Api(app)

# limiter decorater willm help to limit the hits to api as we are exposing to internet
limiter = Limiter(app, key_func=get_remote_address)
limiter.init_app(app)

# Simple swager
api = swagger.docs(Api(app), apiVersion='1.1', api_spec_url='/main')


class sumten(Resource):
    decorators = [limiter.limit("10/day")]

    @swagger.model
    @swagger.operation(notes="add 10 to the given number")
    def get(self, num):
        if type(num) is int:
            return {'sum': num+10}
        else:
            return "user error"


api.add_resource(sumten, '/<int:num>')


if __name__ == '__main__':
    app.run(debug=True, port=5000)

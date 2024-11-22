from flask import Flask
from routers.route import routes
from flask_jwt_extended import JWTManager
from flasgger import Swagger


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
jwt = JWTManager(app)
swagger = Swagger(app)
routes(app)


if __name__ == '__main__':
    app.run(debug=True, port=5000)

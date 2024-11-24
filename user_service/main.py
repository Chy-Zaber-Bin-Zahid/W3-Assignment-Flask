import os
from flask import Flask
from routers.route import routes
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from dotenv import load_dotenv


def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    Swagger(app)
    JWTManager(app)
    routes(app)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=os.getenv('PORT_USER'))

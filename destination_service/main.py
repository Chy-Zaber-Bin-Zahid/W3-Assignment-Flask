import os
from flask import Flask
from routers.route import routes
from flasgger import Swagger
from dotenv import load_dotenv


def create_app():
    load_dotenv()
    app = Flask(__name__)
    Swagger(app)
    routes(app)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=os.getenv('PORT_DESTINATION'))

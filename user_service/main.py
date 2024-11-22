import os
from flask import Flask
from routers.route import routes
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)
swagger = Swagger(app)
routes(app)


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv('PORT_USER'))

from flask import Flask
from routers.route import routes
from flask_jwt_extended import JWTManager

app = Flask(__name__)

routes(app)

if __name__ == '__main__':
    app.run(debug = True, port = 5001)
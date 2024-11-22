from flask import Flask
from routers.route import routes
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)
routes(app)


if __name__ == '__main__':
    app.run(debug=True, port=5001)

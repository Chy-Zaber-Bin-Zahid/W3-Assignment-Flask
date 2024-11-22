import os
from flask import Flask
from routers.route import routes
from flasgger import Swagger
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)
swagger = Swagger(app)
routes(app)


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv('PORT_DESTINATION'))

from controllers.auth import login_route
from controllers.destination import destination_route


def routes(app):
    login_route(app)
    destination_route(app)

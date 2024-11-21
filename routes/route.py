from controllers.login import login_route
from controllers.register import register_route
from controllers.allDestination import destination_route
from controllers.deleteDestination import delete_route


def routes(app):
    login_route(app)
    register_route(app)
    destination_route(app)
    delete_route(app)

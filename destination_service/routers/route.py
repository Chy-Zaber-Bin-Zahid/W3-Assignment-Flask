from controllers.allDestination import destination_route
from controllers.deleteDestination import delete_route


def routes(app):
    destination_route(app)
    delete_route(app)

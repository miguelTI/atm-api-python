from controllers.reset import ResetController
from controllers.balance import BalanceController
from controllers.event import EventController


class Router:
    def __init__(self, server):
        self.server = server

    def mount_routes(self):
        self.post('/reset', ResetController.create)
        self.get('/balance', BalanceController.show)
        self.post('/event', EventController.create)

    def get(self, route_path, function):
        self.server.add_url_rule(route_path, endpoint=self._build_route_name(route_path, 'get'), view_func=function, methods=['GET'])

    def post(self, route_path, function):
        self.server.add_url_rule(route_path, endpoint=self._build_route_name(route_path, 'post'), view_func=function, methods=['POST'])

    @staticmethod
    def _build_route_name(route_path: str, method):
        underlined_route_path = route_path.replace('/', '_')
        return f"{method}{underlined_route_path}"

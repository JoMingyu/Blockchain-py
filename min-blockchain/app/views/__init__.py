from flask_restful import Api


class ViewInjector:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        from app.views.blockchain import Node, Chain, Mine, Transaction

        api = Api(app)

        api.add_resource(Node, '/node')
        api.add_resource(Chain, '/chain')
        api.add_resource(Mine, '/mine')
        api.add_resource(Transaction, '/transaction')

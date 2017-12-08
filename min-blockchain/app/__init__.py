from uuid import uuid4

from flask import Flask

from app.views import ViewInjector

node_id = str(uuid4()).replace('-', '')
# Generate a node id for this node

view_injector = ViewInjector()


def create_app():
    app = Flask(__name__)

    view_injector.init_app(app)

    return app

app_ = create_app()

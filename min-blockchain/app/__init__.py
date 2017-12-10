from flask import Flask

from app.views import ViewInjector


view_injector = ViewInjector()


def create_app():
    app = Flask(__name__)

    view_injector.init_app(app)

    return app

app_ = create_app()

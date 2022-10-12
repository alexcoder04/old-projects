from flask import Flask
import os

def create_app():
    app = Flask(__name__)

    from .config import config

    app.config["SECRET_KEY"] = os.getenv("MAGNAN_SECRET_KEY")
    app.config["MAX_CONTENT_LENGTH"] = config.get("MAX_CONTENT_LENGTH")

    from .api import create_api
    from .auth import create_auth
    from .magnan import create_magnan
    from .storage import create_storage
    from .views import create_views

    from .plugins import registered_plugins
    for plugin in registered_plugins:
        if plugin.ok:
            if not plugin.login_required:
                print(f"WARNING: Plugin '{plugin.name}' does not require a login")
                print("That means that everybody can access the information that plugin provides")
            app.register_blueprint(plugin.app, url_prefix=f"/plugin/{plugin.name}")

    api = create_api()
    auth = create_auth()
    magnan = create_magnan()
    storage = create_storage()
    views = create_views()

    app.register_blueprint(api, url_prefix="/api")
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(magnan, url_prefix="/magnan")
    app.register_blueprint(storage, url_prefix="/storage")
    app.register_blueprint(views, url_prefix="/")

    return app


from .magnan_login_manager import LoginManager

login_manager = LoginManager()

def create_auth():
    from .views import app
    return app

from flask import Blueprint, redirect, render_template, url_for, request, send_from_directory
import os
from ...config import config
from ...auth import login_manager
from ...database import OpenDB
from ...utils import get_server_ip, message_error
from ...config import config

static_server = f"http://{get_server_ip()}:{config.get('STATIC_SERVER_PORT')}/magnan/"

class MagnanPlugin:
    def __init__(self, name, login_required=True, fa_icon="gears", display_name=None):
        self.ok = True
        self.name = name
        if not display_name: display_name = self.name
        self.display_name = display_name
        self.fa_icon = fa_icon
        self.login_required = login_required
        self.pages = {}
        self.api_endpoints = {}
        self.fs_root = os.path.join(config.get("PLUGINS_DIR"), self.name)
        self.app = Blueprint(name, __name__, template_folder=self.fs_root)
        self.databases = {}

        @self.app.route("/")
        def index():
            if self.login_required and not login_manager.is_logged_in():
                return redirect(url_for("views.login", next=request.url))
            return redirect("index")

        @self.app.route("/<path:route>", methods=["GET"])
        def pages(route):
            if self.login_required and not login_manager.is_logged_in():
                return redirect(url_for("views.login", next=request.url))
            if route not in self.pages:
                return "Page not found", 404
            return render_template(self.pages[route], static_server=static_server)
        
        @self.app.route("/static/<path:route>")
        def static(route):
            if self.login_required and not login_manager.is_logged_in():
                return redirect(url_for("views.login", next=request.url))
            
            if "/" in route:
                filename = route.rsplit("/", 1)[1]
                directory = os.path.join(self.fs_root, route.rsplit("/", 1)[0])
                return send_from_directory(directory, filename)
            return send_from_directory(self.fs_root, route)
        
        @self.app.route("/api/<path:route>", methods=["POST"])
        def api(route):
            if self.login_required and not login_manager.is_logged_in():
                return message_error("not authorized", 401)
            if route not in self.api_endpoints:
                return message_error("api endpoint does not exist", 404)
            try:
                return self.api_endpoints[route](self, **request.get_json())
            except TypeError:
                return message_error("invalid request data", 400)

    
    def add_page(self, route, template):
        self.pages[route] = template
    
    def add_api_endpoint(self, route, handler):
        self.api_endpoints[route] = handler
    
    def add_database(self, name, columns):
        if not columns:
            self.error("no db columns were specified")
            return
        self.databases[name] = OpenDB(f"plugin_{self.name}_{name}", columns)
    
    def get_current_user(self):
        return login_manager.get_username()
    
    def error(self, message):
        print(f"AN ERROR OCURRED IN PLUGIN {self.name.upper()}:")
        print(f"====={message}=====")
        self.ok = False

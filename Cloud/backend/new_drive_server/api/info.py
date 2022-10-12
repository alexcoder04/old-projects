from flask import jsonify
from ..plugins import registered_plugins

def initialize_info(app):
    @app.route("/info/<action>", methods=["POST"])
    def info(action):
        if action == "plugins-list":
            return jsonify([
                { "name": i.name, "fa_icon": i.fa_icon, "display_name": i.display_name } for i in registered_plugins
            ])

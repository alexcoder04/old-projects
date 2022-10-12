from flask import jsonify

def json_resp(pydict):
    return jsonify(pydict)

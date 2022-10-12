from flask import Blueprint

app =Blueprint("magnan", __name__)

@app.route("/new")
def new():
    return "<h1>Sorry, this is still in development</h1><a href='javascript:history.back()'>Go Back</a>"


import os
from new_drive_server import create_app

app = create_app()

if __name__== "__main__":
    if os.getenv("MAGNAN_PROD") == "true":
        app.run(debug=False, host="0.0.0.0")
    else:
        app.run(debug=True)

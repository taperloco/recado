from src import create_app
from flask_cors import CORS

import os

if __name__ == '__main__':

    # Create and run Flask-Restful
    app = create_app()

    # Enable CORS with Authorization header exposed
    CORS(app, supports_credentials=True, expose_headers=["Authorization"])
    
    port = int(os.environ.get("PORT", 5000))  # fallback to 5000 for local dev
    app.run(host="0.0.0.0", port=port, debug=True)


    

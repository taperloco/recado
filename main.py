from src import create_app
from flask_cors import CORS

import os


app = create_app()   
if __name__ == '__main__':

    # Create and run Flask-Restful

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


    

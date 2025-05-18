from src import create_app


if __name__ == '__main__':

    # Create and run Flask-Restful
    app = create_app()
    app.run(
        host="0.0.0.0", 
        port=5000, 
        debug=True,
        # Ssl self cerfificate for testing
        ssl_context='adhoc'
    )


    

from src import create_app


if __name__ == '__main__':

    # Create and run Flask-Restful
    app = create_app()
    port = int(os.environ.get("PORT", 5000))  # fallback to 5000 for local dev
    app.run(host="0.0.0.0", port=port, debug=True)


    

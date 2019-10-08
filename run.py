from reanalysis.app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host=app.config.get("FLASK_HOST", "127.0.0.1"),
            port=app.config.get("FLASK_PORT", 5000))

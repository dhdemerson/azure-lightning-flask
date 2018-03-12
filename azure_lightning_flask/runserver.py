from azure_lightning_flask.application import create_app

app = create_app() # pylint: disable=C0103

if __name__ == "__main__":
    app.run()
    
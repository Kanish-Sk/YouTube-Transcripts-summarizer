from flask import Flask
from summarizer.routes import pages

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] ="AheosS50sI1L7wqD6iyDoDzDgqD9J54uKoAjCxQkMiU"
    app.register_blueprint(pages)

    return app

if __name__ == '__main__':
    flask_app = create_app()    
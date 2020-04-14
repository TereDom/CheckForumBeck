from flask import Flask
from data import db_session


app = Flask(__name__)


def main():
    app.run(host='127.0.0.1', port=8080)


@app.route('/')
def index():
    return "CheckForumBeck"


if __name__ == '__main__':
    main()

from flask import Flask

from domain.covid.get import a

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    a()
    return 'Hello World!'


if __name__ == '__main__':
    app.run()

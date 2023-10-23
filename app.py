
from flask import Flask,jsonify
from src.Routes.user import userRoute
from src.Routes.profile import profileRoute
from src.Routes.role import roleRoute
from src.Routes.login import loginRoute
from src.Routes.card import cardRoute
from src.Routes.tweet import tweetRoute
from src.Routes.search import searchRoute
from src.Routes.tweetUser import tweetUserRoute


app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'Hello, World! My name is Twit Sentimy, creado por el Grupo - 1'

profileRoute(app)
userRoute(app)
roleRoute(app)
loginRoute(app)
cardRoute(app)
tweetRoute(app)
tweetUserRoute(app)
searchRoute(app)

if __name__ == "__main__":
    app.run('0.0.0.0',port=3000,debug=True)
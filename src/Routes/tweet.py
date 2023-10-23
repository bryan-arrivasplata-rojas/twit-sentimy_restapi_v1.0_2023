from flask import request,jsonify
from src.Controllers.tweetController import getTweetsController,getTweetController,postTweetController,putTweetController,deleteTweetController
def tweetRoute (app):
    @app.route('/api/tweets', methods = ['GET'])
    def tweets():
        response = getTweetsController()
        return jsonify(response)
    
    @app.route('/api/tweet/<idTweet>', methods = ['GET','PUT','DELETE'])
    def tweet(idTweet):
        if request.method == 'GET':
            response = getTweetController(idTweet)
            return jsonify(response)
        elif request.method == 'PUT':
            data = request.get_json()
            name_tweet = data.get('name_tweet')
            response = putTweetController(idTweet,name_tweet)
            return jsonify(response)
        elif request.method == 'DELETE':
            response = deleteTweetController(idTweet)
            return jsonify(response)
    
    @app.route('/api/tweet', methods = ['POST'])
    def tweet_post():
        data = request.get_json()
        name_tweet = data.get('name_tweet')
        response = postTweetController(name_tweet)
        return jsonify(response)
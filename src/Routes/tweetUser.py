from flask import request,jsonify
from src.Controllers.tweetUserController import getTweetUsersController,getTweetUserController,postTweetUserController,putTweetUserController,deleteTweetUserController
def tweetUserRoute (app):
    @app.route('/api/tweet_users', methods = ['GET'])
    def tweetUsers():
        response = getTweetUsersController()
        return jsonify(response)
    
    @app.route('/api/tweet_user/<idTweetUser>', methods = ['GET','PUT','DELETE'])
    def tweetUser(idTweetUser):
        if request.method == 'GET':
            response = getTweetUserController(idTweetUser)
            return jsonify(response)
        elif request.method == 'PUT':
            data = request.get_json()
            idUser = data.get('idUser')
            idTweet = data.get('idTweet')
            response = putTweetUserController(idTweetUser, idUser, idTweet)
            return jsonify(response)
        elif request.method == 'DELETE':
            response = deleteTweetUserController(idTweetUser)
            return jsonify(response)
    
    @app.route('/api/tweet_users', methods = ['POST'])
    def tweetUser_post():
        data = request.get_json()
        idUser = data.get('idUser')
        idTweet = data.get('idTweet')
        response = postTweetUserController(idUser, idTweet)
        return jsonify(response)
from flask import request,jsonify
from src.Controllers.searchController import postSearchController
def searchRoute (app):
    @app.route('/api/search', methods = ['POST'])
    def search_post():
        data = request.get_json()
        idUser = data.get('idUser')
        identifier = data.get('identifier')
        name_tweet = data.get('name_tweet')
        response = postSearchController(idUser,identifier,name_tweet)
        return jsonify(response)
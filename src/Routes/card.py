from flask import request,jsonify
from src.Controllers.cardController import getCardsController,getCardController,postCardController,putCardController,deleteCardController
def cardRoute (app):
    @app.route('/api/cards', methods = ['GET'])
    def cards():
        response = getCardsController()
        return jsonify(response)
    
    @app.route('/api/card/<idCard>', methods = ['GET','PUT','DELETE'])
    def card(idCard):
        if request.method == 'GET':
            response = getCardController(idCard)
            return jsonify(response)
        elif request.method == 'PUT':
            data = request.get_json()
            number = data.get('number')
            date = data.get('date')
            ccv = data.get('ccv')
            response = putCardController(idCard,number,date,ccv)
            return jsonify(response)
        elif request.method == 'DELETE':
            response = deleteCardController(idCard)
            return jsonify(response)
    
    @app.route('/api/card', methods = ['POST'])
    def card_post():
        data = request.get_json()
        number = data.get('number')
        date = data.get('date')
        ccv = data.get('ccv')
        response = postCardController(number,date,ccv)
        return jsonify(response)
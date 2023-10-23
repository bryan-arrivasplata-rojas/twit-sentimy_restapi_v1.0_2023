from flask import jsonify
from src.Controllers.loginController import getLoginController
def loginRoute (app):
    
    @app.route('/api/login/<username>/<password>', methods = ['GET'])
    def login(username,password):
        response = getLoginController(username,password)
        return jsonify(response)
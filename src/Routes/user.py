from flask import request,jsonify
from src.Controllers.userController import getUsersController,getUserController,postUserController,putUserController,deleteUserController
def userRoute (app):
    @app.route('/api/users', methods = ['GET'])
    def users():
        response = getUsersController()
        return jsonify(response)
    
    @app.route('/api/user/<idUser>', methods = ['GET','PUT','DELETE'])
    def user(idUser):
        if request.method == 'GET':
            response = getUserController(idUser)
            return jsonify(response)
        elif request.method == 'PUT':
            data = request.get_json()
            password = data.get('password')
            response = putUserController(idUser,password)
            return jsonify(response)
        elif request.method == 'DELETE':
            response = deleteUserController(idUser)
            return jsonify(response)
    
    @app.route('/api/user', methods = ['POST'])
    def user_post():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        name_profile = data.get('name_profile')
        lastname = data.get('lastname')
        birthdate = data.get('birthdate')
        response = postUserController(username,password,name_profile,lastname,birthdate)
        return jsonify(response)
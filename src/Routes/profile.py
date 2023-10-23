from flask import request,jsonify
from src.Controllers.profileController import getProfilesController,getProfileController,postProfileController,putProfileController,deleteProfileController
def profileRoute (app):
    @app.route('/api/profiles', methods = ['GET'])
    def profiles():
        response = getProfilesController()
        return jsonify(response)
    
    @app.route('/api/profile/<idProfile>', methods = ['GET','PUT','DELETE'])
    def profile(idProfile):
        if request.method == 'GET':
            response = getProfileController(idProfile)
            return jsonify(response)
        elif request.method == 'PUT':
            data = request.get_json()
            name_profile = data.get('name_profile')
            lastName = data.get('lastName')
            birthdate = data.get('birthdate')
            idUser = data.get('idUser')
            idRole = data.get('idRole')
            idCard = data.get('idCard')
            response = putProfileController(idProfile,name_profile, lastName, birthdate, idUser, idRole, idCard)
            return jsonify(response)
        elif request.method == 'DELETE':
            response = deleteProfileController(idProfile)
            return jsonify(response)
    
    @app.route('/api/profile', methods = ['POST'])
    def profile_post():
        data = request.get_json()
        name_profile = data.get('name_profile')
        lastName = data.get('lastName')
        birthdate = data.get('birthdate')
        idUser = data.get('idUser')
        idRole = data.get('idRole')
        idCard = data.get('idCard')
        response = postProfileController(name_profile, lastName, birthdate, idUser, idRole, idCard)
        return jsonify(response)
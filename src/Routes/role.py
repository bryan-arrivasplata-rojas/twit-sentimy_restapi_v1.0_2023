from flask import request,jsonify
from src.Controllers.roleController import getRolesController,getRoleController,postRoleController,putRoleController,deleteRoleController
def roleRoute (app):
    @app.route('/api/roles', methods = ['GET'])
    def roles():
        response = getRolesController()
        return jsonify(response)
    
    @app.route('/api/role/<idRole>', methods = ['GET','PUT','DELETE'])
    def role(idRole):
        if request.method == 'GET':
            response = getRoleController(idRole)
            return jsonify(response)
        elif request.method == 'PUT':
            data = request.get_json()
            name_role = data.get('name_role')
            response = putRoleController(idRole,name_role)
            return jsonify(response)
        elif request.method == 'DELETE':
            response = deleteRoleController(idRole)
            return jsonify(response)
    
    @app.route('/api/role', methods = ['POST'])
    def role_post():
        data = request.get_json()
        name_role = data.get('name_role')
        response = postRoleController(name_role)
        return jsonify(response)
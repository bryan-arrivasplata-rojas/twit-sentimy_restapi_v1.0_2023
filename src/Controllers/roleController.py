from src.Models.roleModel import getRoles,getRole,postRole,putRole,deleteRole

def getRolesController():
    response = getRoles()
    if isinstance(response, list) and not response:
        return response
    elif isinstance(response, list) and 'message_error' in response[0]:
        respuesta = {'message_error': str(response)}
        return respuesta
    else:
        return response

def getRoleController(idRole):
    response = getRole(idRole)
    if not (isinstance(response, list) and 'message_error' in response[0]):
        return response
    else:
        respuesta = {'message_error':str(response)}
        return respuesta
    
def postRoleController(name_role):
    response = postRole(name_role)
    if not (isinstance(response, list) and 'message_error' in response[0]):
        return response
    else:
        respuesta = {'message_error':str(response)}
        return respuesta

def putRoleController(idRole,name_role):
    response = putRole(idRole,name_role)
    if not (isinstance(response, list) and 'message_error' in response[0]):
        return response
    else:
        respuesta = {'message_error':str(response)}
        return respuesta
def deleteRoleController(idRole):
    response = deleteRole(idRole)
    if not (isinstance(response, list) and 'message_error' in response[0]):
        return response
    else:
        respuesta = {'message_error':str(response)}
        return respuesta
from src.Models.userModel import getUsers,getUser,postUser,putUser,deleteUser

def getUsersController():
    response = getUsers()
    if isinstance(response, list) and not response:
        return response
    elif isinstance(response, list) and 'message_error' in response[0]:
        respuesta = {'message_error': str(response)}
        return respuesta
    else:
        return response

def getUserController(idUser):
    response = getUser(idUser)
    if not (isinstance(response, list) and 'message_error' in response[0]):
        return response
    else:
        respuesta = {'message_error':str(response)}
        return respuesta
    
def postUserController(username,password):
    response = postUser(username,password)
    if not (isinstance(response, list) and 'message_error' in response[0]):
        return response
    else:
        respuesta = {'message_error':str(response)}
        return respuesta

def putUserController(idUser,password):
    response = putUser(idUser,password)
    if not (isinstance(response, list) and 'message_error' in response[0]):
        return response
    else:
        respuesta = {'message_error':str(response)}
        return respuesta
def deleteUserController(idUser):
    response = deleteUser(idUser)
    if not (isinstance(response, list) and 'message_error' in response[0]):
        return response
    else:
        respuesta = {'message_error':str(response)}
        return respuesta
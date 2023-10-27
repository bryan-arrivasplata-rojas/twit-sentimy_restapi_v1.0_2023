from src.Models.userModel import getUsers,getUser,postUser,putUser,deleteUser
from src.Models.profileModel import postProfile

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
    
def postUserController(username,password,name_profile, lastName, birthdate):
    response = postUser(username,password)
    if not (isinstance(response, list) and 'message_error' in response[0]):
        idUser = response['idUser']
        reponse_profile = postProfile(name_profile, lastName, birthdate, idUser, 2) #2 es rol user_basic
        if not (isinstance(reponse_profile, list) and 'message_error' in reponse_profile[0]):
            return {**response, **reponse_profile}
        else:
            respuesta_profile = {'message_error':str(reponse_profile)}
            return respuesta_profile
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
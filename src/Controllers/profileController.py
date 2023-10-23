from src.Models.profileModel import getProfiles,getProfile,postProfile,putProfile,deleteProfile

def getProfilesController():
    response = getProfiles()
    if isinstance(response, list) and not response:
        return response
    elif isinstance(response, list) and 'message_error' in response[0]:
        respuesta = {'message_error': str(response)}
        return respuesta
    else:
        return response

def getProfileController(idProfile):
    response = getProfile(idProfile)
    if not (isinstance(response, list) and 'message_error' in response[0]):
        return response
    else:
        respuesta = {'message_error':str(response)}
        return respuesta
    
def postProfileController(name_profile, lastName, birthdate, idUser, idRole, idCard):
    response = postProfile(name_profile, lastName, birthdate, idUser, idRole, idCard)
    if not (isinstance(response, list) and 'message_error' in response[0]):
        return response
    else:
        respuesta = {'message_error':str(response)}
        return respuesta

def putProfileController(idProfile,name_profile, lastName, birthdate, idUser, idRole, idCard):
    response = putProfile(idProfile,name_profile, lastName, birthdate, idUser, idRole, idCard)
    if not (isinstance(response, list) and 'message_error' in response[0]):
        return response
    else:
        respuesta = {'message_error':str(response)}
        return respuesta
def deleteProfileController(idProfile):
    response = deleteProfile(idProfile)
    if not (isinstance(response, list) and 'message_error' in response[0]):
        return response
    else:
        respuesta = {'message_error':str(response)}
        return respuesta
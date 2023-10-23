from src.Models.loginModel import getLogin

def getLoginController(user,password):
    response = getLogin(user,password)
    if not (isinstance(response, list) and 'message_error' in response[0]):
        return response
    else:
        respuesta = {'message_error':str(response)}
        return respuesta
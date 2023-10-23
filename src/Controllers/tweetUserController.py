from src.Models.tweetUserModel import getTweetUsers,getTweetUser,postTweetUser,putTweetUser,deleteTweetUser

def getTweetUsersController():
    response = getTweetUsers()
    if isinstance(response, list) and not response:
        return response
    elif isinstance(response, list) and 'message_error' in response[0]:
        respuesta = {'message_error': str(response)}
        return respuesta
    else:
        return response

def getTweetUserController(idTweetUser):
    response = getTweetUser(idTweetUser)
    if not (isinstance(response, list) and 'message_error' in response[0]):
        return response
    else:
        respuesta = {'message_error':str(response)}
        return respuesta

def postTweetUserController(idUser, idTweet):
    response = postTweetUser(idUser, idTweet)
    if not (isinstance(response, list) and 'message_error' in response[0]):
        return response
    else:
        respuesta = {'message_error':str(response)}
        return respuesta

def putTweetUserController(idTweetUser, idUser, idTweet):
    response = putTweetUser(idTweetUser, idUser, idTweet)
    if not (isinstance(response, list) and 'message_error' in response[0]):
        return response
    else:
        respuesta = {'message_error':str(response)}
        return respuesta
def deleteTweetUserController(idTweetUser):
    response = deleteTweetUser(idTweetUser)
    if not (isinstance(response, list) and 'message_error' in response[0]):
        return response
    else:
        respuesta = {'message_error':str(response)}
        return respuesta
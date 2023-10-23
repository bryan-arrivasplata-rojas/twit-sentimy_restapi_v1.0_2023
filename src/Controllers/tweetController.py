from src.Models.tweetModel import getTweets,getTweet,postTweet,putTweet,deleteTweet

def getTweetsController():
    response = getTweets()
    if isinstance(response, list) and not response:
        return response
    elif isinstance(response, list) and 'message_error' in response[0]:
        respuesta = {'message_error': str(response)}
        return respuesta
    else:
        return response

def getTweetController(idTweet):
    response = getTweet(idTweet)
    if not (isinstance(response, list) and 'message_error' in response[0]):
        return response
    else:
        respuesta = {'message_error':str(response)}
        return respuesta
    
def postTweetController(name_tweet):
    response = postTweet(name_tweet)
    if not (isinstance(response, list) and 'message_error' in response[0]):
        return response
    else:
        respuesta = {'message_error':str(response)}
        return respuesta

def putTweetController(idTweet,name_tweet):
    response = putTweet(idTweet,name_tweet)
    if not (isinstance(response, list) and 'message_error' in response[0]):
        return response
    else:
        respuesta = {'message_error':str(response)}
        return respuesta
def deleteTweetController(idTweet):
    response = deleteTweet(idTweet)
    if not (isinstance(response, list) and 'message_error' in response[0]):
        return response
    else:
        respuesta = {'message_error':str(response)}
        return respuesta
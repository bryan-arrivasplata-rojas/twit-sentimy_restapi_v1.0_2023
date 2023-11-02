from src.Models.searchModel import getSearch
from src.Models.tweetModel import getTweetByIdentifier,postTweet
from src.Models.tweetUserModel import getTweetUserByIdentifierIdUser,postTweetUser
from helpers.read import readComments


def postSearchController(idUser, identifier, name_tweet):
    list_tweet_identifier = getTweetByIdentifier(identifier)

    # Crear una variable para controlar si se encuentra una coincidencia
    found_match = False
    information = ''
    for tweet in list_tweet_identifier:
        idTweetByList = tweet['idTweet']
        response_filter = getTweetUserByIdentifierIdUser(idUser,idTweetByList)
        information = response_filter
        if isinstance(response_filter, list) and not response_filter:
            continue  # Continuar con la siguiente iteración si no hay coincidencia
        else:
            found_match = True  # Marcar que se encontró una coincidencia
            break  # Salir del bucle si se encontró una coincidencia
    tweet_text = ''
    comments = ''
    if not found_match:
        tweet_response = postTweet(identifier,name_tweet)
        if not 'message_error' in tweet_response:
            idTweet = tweet_response['idTweet']
            response = postTweetUser(idUser, idTweet)
            information = response
            if 'message_error' in response:
                return response
    comments = readComments(identifier)
    
    if 'message_error' in comments:
        return comments
    if isinstance(comments, dict):
        tweet_text = comments.get('tweet')  # Obtener el contenido del tweet
        comments = comments.get('comments', '')
    print(information)
    response_search = getSearch(tweet_text,comments)
    if not (isinstance(response_search, list) and 'message_error' in response_search[0]):
        response_search["name_tweet"] = information["tweet"]["name_tweet"]
        response_search["idTweetUser"] = information["idTweetUser"]
        response_search["idTweet"] = information["idTweet"]
        
        # Calcula la variable polarity en función de los porcentajes
        if response_search["neutral_percentage"] > 70:
            if response_search["negative_percentage"] > response_search["positive_percentage"]:
                response_search["polarity"] = "negative"
            else:
                response_search["polarity"] = "positive"
        else:
            response_search["polarity"] = "neutral"
        return response_search
    else:
        respuesta = {'message_error':str(response_search)}
        return respuesta
from src.Models.searchModel import getSearch
from src.Models.tweetModel import getTweetByIdentifier,postTweet
from src.Models.tweetUserModel import getTweetUserByIdentifierIdUser,postTweetUser
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob

def postSearchController(idUser, identifier, name_tweet):
    list_tweet_identifier = getTweetByIdentifier(identifier)

    # Crear una variable para controlar si se encuentra una coincidencia
    found_match = False

    for tweet in list_tweet_identifier:
        idTweetByList = tweet['idTweet']
        response_filter = getTweetUserByIdentifierIdUser(idUser,idTweetByList)
        if isinstance(response_filter, list) and not response_filter:
            continue  # Continuar con la siguiente iteración si no hay coincidencia
        else:
            found_match = True  # Marcar que se encontró una coincidencia
            break  # Salir del bucle si se encontró una coincidencia
    nltk.download('vader_lexicon')
    sia = SentimentIntensityAnalyzer()
    if found_match:
        comments = getSearch(identifier)

        if 'message_error' in comments:
            return comments
        
        textblob_analysis = TextBlob(comments)
        # Realiza el análisis de sentimientos con NLTK
        nltk_sentiment = sia.polarity_scores(comments)


        # Imprime los resultados de TextBlob
        print("Análisis de sentimientos con TextBlob:")
        print("Texto del comentario:", comments)
        print("Polaridad:", textblob_analysis.sentiment.polarity)
        print("Subjetividad:", textblob_analysis.sentiment.subjectivity)

        # Imprime los resultados de NLTK
        print("\nAnálisis de sentimientos con NLTK:")
        print("Texto del comentario:", comments)
        print("Polaridad de NLTK:", nltk_sentiment['compound'])

        # Muestra una etiqueta personalizada basada en el análisis de NLTK
        if nltk_sentiment['compound'] >= 0.05:
            print("Sentimiento: Positivo")
        elif nltk_sentiment['compound'] <= -0.05:
            print("Sentimiento: Negativo")
        else:
            print("Sentimiento: Neutro")


        return response_filter  # Devolver la respuesta encontrada
    tweet_response = postTweet(identifier,name_tweet)
    if 'message_error' in tweet_response:
        # Si hubo un error al crear el tweet, devuelve el error.
        return tweet_response
    else:
        idTweet = tweet_response['idTweet']
        response = postTweetUser(idUser, idTweet)
        if not (isinstance(response, list) and 'message_error' in response[0]):
            return response
        else:
            respuesta = {'message_error':str(response)}
            return respuesta
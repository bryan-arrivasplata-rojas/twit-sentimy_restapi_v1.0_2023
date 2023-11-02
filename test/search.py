import sys
import os

# Obtiene la ruta al directorio raíz de tu proyecto
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from src.Models.tweetModel import getTweetByIdentifier,postTweet
from src.Models.tweetUserModel import getTweetUserByIdentifierIdUser,postTweetUser
import nltk
from helpers.read import readComments
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob

# Obtiene la ruta al directorio raíz de tu proyecto
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from src.Models.tweetModel import getTweetByIdentifier, postTweet
from src.Models.tweetUserModel import getTweetUserByIdentifierIdUser
from helpers.read import readComments
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
def get_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    nltk_sentiment = sia.polarity_scores(text)

    if nltk_sentiment['compound'] >= 0.05:
        return 'positivo'
    elif nltk_sentiment['compound'] <= -0.05:
        return 'negativo'
    else:
        return 'neutro'
def calculate_polarity(comment):
    analysis = TextBlob(comment)
    return analysis.sentiment.polarity
def generate_summary(comments):
    # Concatena los comentarios en un solo texto
    comments_text = ' '.join(comments)

    # Inicializa el resumidor LexRank
    summarizer = LexRankSummarizer()

    # Tokeniza el texto
    parser = PlaintextParser.from_string(comments_text, Tokenizer("english"))

    # Genera un resumen del texto
    summary = summarizer(parser.document, sentences_count=2)  # Ajusta el número de oraciones en el resumen

    # Convierte el resumen en una cadena
    summary_text = ' '.join([str(sentence) for sentence in summary])

    return summary_text
def postSearchController(idUser, identifier, name_tweet):
    list_tweet_identifier = getTweetByIdentifier(identifier)
    # Crear una variable para controlar si se encuentra una coincidencia
    found_match = False

    for tweet in list_tweet_identifier:
        idTweetByList = tweet['idTweet']
        response_filter = getTweetUserByIdentifierIdUser(idUser, idTweetByList)
        if isinstance(response_filter, list) and not response_filter:
            continue  # Continuar con la siguiente iteración si no hay coincidencia
        else:
            found_match = True  # Marcar que se encontró una coincidencia
            break  # Salir del bucle si se encontró una coincidencia

    nltk.download('vader_lexicon')
    sia = SentimentIntensityAnalyzer()  # Agregar esta línea para definir sia
    if found_match:
        comments = readComments(identifier)
        if 'message_error' in comments:
            return comments
        if isinstance(comments, dict):
            comments = comments.get('comments', '')

        # Unir los comentarios en una sola cadena
        comments_text = ' '.join(comments)

        # Crear listas para almacenar los sentimientos
        sentiments = []
        positive_comments = []
        negative_comments = []

        # Realiza el análisis de sentimientos para cada comentario
        for comment in comments:
            sentiment = get_sentiment(comment)
            sentiments.append(sentiment)

            if sentiment == 'positivo':
                positive_comments.append(comment)
            elif sentiment == 'negativo':
                negative_comments.append(comment)

        # Calcular el porcentaje de mensajes positivos, negativos y neutros
        total_comments = len(sentiments)
        positive_percentage = sentiments.count('positivo') / total_comments * 100
        negative_percentage = sentiments.count('negativo') / total_comments * 100
        neutral_percentage = sentiments.count('neutro') / total_comments * 100

        # Calcular estadísticas
        positive_scores = [sia.polarity_scores(comment)['compound'] for comment in positive_comments]
        negative_scores = [sia.polarity_scores(comment)['compound'] for comment in negative_comments]

        # Obtener los 3 comentarios más positivos y los 3 más negativos
        top_3_positive = [comment for _, comment in sorted(zip(positive_scores, positive_comments), reverse=True)[:3]]
        top_3_negative = [comment for _, comment in sorted(zip(negative_scores, negative_comments))[:3]]
        # Genera un resumen de los comentarios
        summary = generate_summary(comments)
        print("\nResumen de comentarios:")
        print(summary)
        # Imprimir los resultados
        print("Análisis de sentimientos:")
        print("Porcentaje de mensajes positivos:", positive_percentage)
        print("Porcentaje de mensajes negativos:", negative_percentage)
        print("Porcentaje de mensajes neutros:", neutral_percentage)
        print("\nLos 3 mensajes más positivos:")
        for i, comment in enumerate(top_3_positive, 1):
            print(f"{i}. {comment}")
        print("\nLos 3 mensajes más negativos:")
        for i, comment in enumerate(top_3_negative, 1):
            print(f"{i}. {comment}")
        

        # Crear listas para almacenar las polaridades
        polarities = []

        # Calcular la polaridad de cada comentario
        for comment in comments:
            polarity = calculate_polarity(comment)
            polarities.append(polarity)

        # Calcular el promedio de polaridades
        average_polarity = sum(polarities) / len(polarities)

        # Imprimir el promedio de polaridad
        print("\nPromedio de polaridad de los comentarios:", average_polarity)
        
        return response_filter  # Devolver la respuesta encontrada

    tweet_response = postTweet(identifier, name_tweet)
    if 'message_error' in tweet_response:
        # Si hubo un error al crear el tweet, devuelve el error.
        return tweet_response
    else:
        idTweet = tweet_response['idTweet']
        response = postTweetUser(idUser, idTweet)
        if not (isinstance(response, list) and 'message_error' in response[0]):
            return response
        else:
            respuesta = {'message_error': str(response)}
            return respuesta

postSearchController(2, '1718318502975561742', 'prueba2')

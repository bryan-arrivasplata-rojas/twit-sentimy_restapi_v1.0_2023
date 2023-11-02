import sys
import os
# Obtiene la ruta al directorio raíz de tu proyecto
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
from src.Models.tweetModel import getTweetByIdentifier,postTweet
from src.Models.tweetUserModel import getTweetUserByIdentifierIdUser,postTweetUser
from helpers.read import readComments
import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import spacy.cli
spacy.cli.download("es_core_news_sm")
# Cargar el modelo de spaCy (debes descargar e instalar un modelo de lenguaje previamente)
nlp = spacy.load("es_core_news_sm")  # Reemplaza "es_core_news_sm" con el modelo en español que prefieras

# Inicializar el analizador de sentimientos de VADER
analyzer = SentimentIntensityAnalyzer()

def analyze_sentiments(text):
    # Realizar el análisis de sentimientos con VADER
    sentiment = analyzer.polarity_scores(text)
    
    # Determinar la polaridad en función de los puntajes VADER
    if sentiment['compound'] >= 0.05:
        return 'positivo'
    elif sentiment['compound'] <= -0.05:
        return 'negativo'
    else:
        return 'neutro'
def analyze_polarity(text, analyzer):
    sentiment = analyzer.polarity_scores(text)
    return sentiment['compound']

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

    if found_match:
        comments = readComments(identifier)
        if 'message_error' in comments:
            return comments
        if isinstance(comments, dict):
            tweet_text = comments.get('tweet')  # Obtener el contenido del tweet
            comments = comments.get('comments', '')

        # Crear listas para almacenar los sentimientos y las polaridades
        sentiments = []
        polarities = []

        # Realizar el análisis de sentimientos para cada comentario y calcular las polaridades
        for comment in comments:
            sentiment = analyze_sentiments(comment)
            sentiments.append(sentiment)
            polarity = analyze_polarity(comment, analyzer)
            polarities.append(polarity)

        # Calcular el porcentaje de mensajes positivos, negativos y neutros
        total_comments = len(sentiments)
        positive_percentage = sentiments.count('positivo') / total_comments * 100
        negative_percentage = sentiments.count('negativo') / total_comments * 100
        neutral_percentage = sentiments.count('neutro') / total_comments * 100

        # Obtener los 3 comentarios más positivos y los 3 más negativos
        sorted_comments = list(zip(polarities, comments))
        sorted_comments.sort(reverse=True)  # Ordenar en orden descendente por polaridad
        top_3_positive = [comment for _, comment in sorted_comments[:3]]
        sorted_comments.sort()  # Ordenar en orden ascendente por polaridad
        top_3_negative = [comment for _, comment in sorted_comments[:3]]

        # Crear un resumen de todos los comentarios con el contenido del tweet
        all_comments_summary = generate_summary(comments, tweet_text)

        # Resto del código para análisis y resumen de comentarios...
        print(all_comments_summary)
        print("Contenido del Tweet:")
        print(tweet_text)
        print("Los 3 comentarios más positivos:")
        for i, comment in enumerate(top_3_positive, 1):
            print(f"{i}. {comment}")
        print("Los 3 comentarios más negativos:")
        for i, comment in enumerate(top_3_negative, 1):
            print(f"{i}. {comment}")
        print("Porcentaje de mensajes positivos:", positive_percentage)
        print("Porcentaje de mensajes negativos:", negative_percentage)
        print("Porcentaje de mensajes neutros:", neutral_percentage)
        return response_filter  # Devolver la respuesta encontrada

    # Resto del código para publicar tweets y gestionar errores...

# Función para generar un resumen de los comentarios con el contenido del tweet
def generate_summary(comments, tweet_text):
    # Concatenar el contenido del tweet y los comentarios en un solo texto
    comments_text = ' '.join([tweet_text] + comments)
    
    # Procesar el texto con spaCy
    doc = nlp(comments_text)
    
    # Extraer las oraciones
    sentences = [sent.text for sent in doc.sents]
    
    # Tomar las primeras N oraciones como resumen
    num_sentences_in_summary = 3  # Puedes ajustar este valor
    summary = ' '.join(sentences[:num_sentences_in_summary])
    
    return summary

# Ejecutar la función con los parámetros necesarios
postSearchController(2, '1716462421181620400', 'cueva mal jugador')
from helpers.analyzer import analyze_polarity,analyze_sentiments,generate_summary
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def getSearch(tweet_text,comments):
    try:
        sentiments = []
        polarities = []
        analyzer = SentimentIntensityAnalyzer()
        for comment in comments:
            sentiment = analyze_sentiments(comment, analyzer)
            sentiments.append(sentiment)
            polarity = analyze_polarity(comment, analyzer)
            polarities.append(polarity)
            
        # Calcular el porcentaje de mensajes positivos, negativos y neutros
        total_comments = len(sentiments)
        positive_percentage = sentiments.count('positivo') / total_comments * 100
        negative_percentage = sentiments.count('negativo') / total_comments * 100
        neutral_percentage = sentiments.count('neutro') / total_comments * 100
        
        # Crear un resumen de todos los comentarios con el contenido del tweet
        all_comments_summary = generate_summary(comments, tweet_text)

        # Obtener los 3 comentarios más positivos y los 3 más negativos
        sorted_comments = list(zip(polarities, comments))
        sorted_comments.sort(reverse=True)  # Ordenar en orden descendente por polaridad
        top_3_positive = [comment for _, comment in sorted_comments[:3]]
        sorted_comments.sort()  # Ordenar en orden ascendente por polaridad
        top_3_negative = [comment for _, comment in sorted_comments[:3]]

        # Crear un diccionario con los resultados
        result = {
            "tweet_text": tweet_text,
            "summary":all_comments_summary,
            "top_3_positives": top_3_positive,
            "top_3_negatives": top_3_negative,
            "positive_percentage": positive_percentage,
            "negative_percentage": negative_percentage,
            "neutral_percentage": neutral_percentage
        }

        return result
    except Exception as e:
        return {'message_error': str(e), 'section': 'getSearch'}
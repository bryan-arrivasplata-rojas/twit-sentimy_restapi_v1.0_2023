import spacy.cli
def analyze_sentiments(text,analyzer):
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

def generate_summary(comments, tweet_text):
    spacy.cli.download("es_core_news_sm")
    nlp = spacy.load("es_core_news_sm")
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
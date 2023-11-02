import json

def readAllComments():
    try:
        with open('helpers/comments.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except:
        return {'message_error': 'readAllComments'}

def readComments(identified):
    try:
        with open('helpers/comments.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        for item in data:
            if(identified==item["identified"]):
                return item
        return {'message_error': 'No es posible obtener los comentarios del tweet'}
    except:
        return {'message_error': 'readComments'}
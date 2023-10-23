from Connection.Connection import connect

def getTweets():
    dataBase = connect()
    if not isinstance(dataBase, list):
        cursorObject = dataBase.cursor()
        try:
            stmt = "SELECT idTweet, identifier, name_tweet, created_at FROM tweet ORDER BY created_at DESC"
            cursorObject.execute(stmt)
            columns = [desc[0] for desc in cursorObject.description]
            results = cursorObject.fetchall()
            cursorObject.close()

            tweets = []
            for row in results:
                tweet_dict = dict(zip(columns, row))
                tweets.append(tweet_dict)

            dataBase.close()
            return tweets  # Convertir la lista de tweets a JSON

        except Exception as e:
            cursorObject.close()
            dataBase.close()
            return {'message_error': str(e), 'section': 'getTweets'}
    else:
        error_message = dataBase[0]['message']
        return {'message_error': str(error_message)}

def getTweet(idTweet):
    dataBase = connect()
    if not isinstance(dataBase, list):
        cursorObject = dataBase.cursor()
        try:
            stmt = "SELECT idTweet, identifier, name_tweet FROM tweet WHERE idTweet = %s"
            cursorObject.execute(stmt, (idTweet,))
            columns = [desc[0] for desc in cursorObject.description]
            result = cursorObject.fetchone()
            cursorObject.close()

            if result:
                tweet_dict = dict(zip(columns, result))
                dataBase.close()
                return tweet_dict

            else:
                dataBase.close()
                return {'message_error': 'Tweet not found'}

        except Exception as e:
            cursorObject.close()
            dataBase.close()
            return {'message_error': str(e), 'section': 'getTweetById'}
    else:
        error_message = dataBase[0]['message']
        return {'message_error': str(error_message)}

def getTweetByIdentifier(identifier):
    dataBase = connect()
    if not isinstance(dataBase, list):
        cursorObject = dataBase.cursor()
        try:
            stmt = "SELECT idTweet, identifier, name_tweet FROM tweet WHERE identifier = %s"
            cursorObject.execute(stmt, (identifier,))
            columns = [desc[0] for desc in cursorObject.description]
            results = cursorObject.fetchall()
            cursorObject.close()

            tweets = []
            
            for row in results:
                tweet_dict = dict(zip(columns, row))
                tweets.append(tweet_dict)
            dataBase.close()
            return tweets  # Convertir la lista de roles a JSON

        except Exception as e:
            cursorObject.close()
            dataBase.close()
            return {'message_error': str(e), 'section': 'getTweetByIdentifier'}
    else:
        error_message = dataBase[0]['message']
        return {'message_error': str(error_message)}

def postTweet(identifier, name_tweet):
    dataBase = connect()
    if not isinstance(dataBase, list):
        cursorObject = dataBase.cursor()
        try:
            insert_stmt = "INSERT INTO tweet (identifier, name_tweet) VALUES (%s, %s)"
            cursorObject.execute(insert_stmt, (identifier, name_tweet))
            dataBase.commit()
            new_tweet_id = cursorObject.lastrowid
            cursorObject.close()
            dataBase.close()
            return {'idTweet': new_tweet_id, 'identifier': identifier, 'name_tweet': name_tweet}

        except Exception as e:
            cursorObject.close()
            dataBase.close()
            return {'message_error': str(e), 'section': 'postTweet'}
    else:
        error_message = dataBase[0]['message']
        return {'message_error': str(error_message)}
    
def putTweet(idTweet, new_identifier, new_name_tweet):
    dataBase = connect()
    if not isinstance(dataBase, list):
        cursorObject = dataBase.cursor()
        try:
            # Verifica si el idTweet existe antes de actualizar los datos del tweet
            tweet_check_stmt = "SELECT idTweet, identifier FROM tweet WHERE idTweet = %s"
            cursorObject.execute(tweet_check_stmt, (idTweet,))
            existing_tweet = cursorObject.fetchone()

            if existing_tweet:
                current_identifier = existing_tweet[1]  # Identificador actual del tweet

                # Verificar si el nuevo identificador es diferente del actual
                if new_identifier != current_identifier:
                    # Comprobar si el nuevo identificador ya existe en la tabla de tweets
                    check_stmt = "SELECT idTweet FROM tweet WHERE identifier = %s"
                    cursorObject.execute(check_stmt, (new_identifier,))
                    existing_tweet_with_new_identifier = cursorObject.fetchone()

                    if existing_tweet_with_new_identifier:
                        cursorObject.close()
                        dataBase.close()
                        return {'message_error': 'El nuevo identificador ya existe en la base de datos', 'section': 'putTweet'}

                # El idTweet existe y el nuevo identificador no está duplicado, actualizar los datos del tweet
                update_stmt = "UPDATE tweet SET identifier = %s, name_tweet = %s WHERE idTweet = %s"
                cursorObject.execute(update_stmt, (new_identifier, new_name_tweet, idTweet))
                dataBase.commit()
                cursorObject.close()
                dataBase.close()
                return {'idTweet': idTweet, 'identifier': new_identifier, 'name_tweet': new_name_tweet}

            else:
                cursorObject.close()
                dataBase.close()
                return {'message_error': 'Tweet not found'}

        except Exception as e:
            cursorObject.close()
            dataBase.close()
            return {'message_error': str(e), 'section': 'putTweet'}

    else:
        error_message = dataBase[0]['message']
        return {'message_error': str(error_message)}

def deleteTweet(idTweet):
    dataBase = connect()
    if not isinstance(dataBase, list):
        cursorObject = dataBase.cursor()
        try:
            # Verifica si el idTweet existe antes de eliminar el tweet
            tweet_check_stmt = "SELECT idTweet FROM tweet WHERE idTweet = %s"
            cursorObject.execute(tweet_check_stmt, (idTweet,))
            existing_tweet = cursorObject.fetchone()

            if existing_tweet:
                # El idTweet existe, ahora elimina el tweet
                delete_stmt = "DELETE FROM tweet WHERE idTweet = %s"
                cursorObject.execute(delete_stmt, (idTweet,))
                dataBase.commit()
                cursorObject.close()
                dataBase.close()
                return {'message': f'Tweet {existing_tweet[0]} eliminado con éxito'}

            else:
                cursorObject.close()
                dataBase.close()
                return {'message_error': 'Tweet not found'}

        except Exception as e:
            cursorObject.close()
            dataBase.close()
            return {'message_error': str(e), 'section': 'deleteTweet'}

    else:
        error_message = dataBase[0]['message']
        return {'message_error': str(error_message)}
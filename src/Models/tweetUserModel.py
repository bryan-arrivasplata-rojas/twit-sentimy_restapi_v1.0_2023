from Connection.Connection import connect

def getTweetUsers():
    dataBase = connect()
    if not isinstance(dataBase, list):
        cursorObject = dataBase.cursor()
        try:
            stmt = ("SELECT "
                    "tu.idTweetUser, "
                    "tu.idTweet, "
                    "tu.idUser, "
                    "u.username, "
                    "u.password, "
                    "t.identifier, "
                    "t.name_tweet "
                    "FROM tweet_user tu "
                    "LEFT JOIN user u ON tu.idUser = u.idUser "
                    "LEFT JOIN tweet t ON tu.idTweet = t.idTweet")
            cursorObject.execute(stmt)
            columns = [desc[0] for desc in cursorObject.description]
            results = cursorObject.fetchall()
            cursorObject.close()

            tweet_users = []
            for row in results:
                tweet_user_dict = dict(zip(columns, row))

                # Estructura los datos de user y tweet como subdiccionarios
                user_info = {
                    'idUser': tweet_user_dict['idUser'],
                    'username': tweet_user_dict['username'],
                    'password': tweet_user_dict['password']
                }
                tweet_info = {
                    'idTweet': tweet_user_dict['idTweet'],
                    'identifier': tweet_user_dict['identifier'],
                    'name_tweet': tweet_user_dict['name_tweet']
                }

                # Reemplaza campos nulos o vacíos con diccionarios vacíos
                if user_info['idUser'] is None:
                    user_info = {}
                if tweet_info['idTweet'] is None:
                    tweet_info = {}
                
                tweet_user_dict['user'] = user_info
                tweet_user_dict['tweet'] = tweet_info

                # Elimina los campos principales de tweet_user
                del tweet_user_dict['username']
                del tweet_user_dict['password']
                del tweet_user_dict['identifier']
                del tweet_user_dict['name_tweet']

                tweet_users.append(tweet_user_dict)

            dataBase.close()
            return tweet_users

        except Exception as e:
            cursorObject.close()
            dataBase.close()
            return {'message_error': str(e), 'section': 'getTweetUsers'}
    else:
        error_message = dataBase[0]['message']
        return {'message_error': str(error_message)}

def getTweetUser(idTweetUser):
    dataBase = connect()
    if not isinstance(dataBase, list):
        cursorObject = dataBase.cursor()
        try:
            stmt = ("SELECT "
                    "tu.idTweetUser, "
                    "tu.idTweet, "
                    "tu.idUser, "
                    "u.username, "
                    "u.password, "
                    "t.identifier, "
                    "t.name_tweet "
                    "FROM tweet_user tu "
                    "LEFT JOIN user u ON tu.idUser = u.idUser "
                    "LEFT JOIN tweet t ON tu.idTweet = t.idTweet "
                    "WHERE tu.idTweetUser = %s")
            cursorObject.execute(stmt, (idTweetUser,))
            columns = [desc[0] for desc in cursorObject.description]
            result = cursorObject.fetchone()
            cursorObject.close()
            if result:
                tweet_user_dict = dict(zip(columns, result))

                # Estructura los datos de user y tweet como subdiccionarios
                user_info = {
                    'idUser': tweet_user_dict['idUser'],
                    'username': tweet_user_dict['username'],
                    'password': tweet_user_dict['password']
                }
                tweet_info = {
                    'idTweet': tweet_user_dict['idTweet'],
                    'identifier': tweet_user_dict['identifier'],
                    'name_tweet': tweet_user_dict['name_tweet']
                }

                # Reemplaza campos nulos o vacíos con diccionarios vacíos
                if user_info['idUser'] is None:
                    user_info = {}
                if tweet_info['idTweet'] is None:
                    tweet_info = {}
                
                tweet_user_dict['user'] = user_info
                tweet_user_dict['tweet'] = tweet_info

                # Elimina los campos principales de tweet_user
                del tweet_user_dict['username']
                del tweet_user_dict['password']
                del tweet_user_dict['identifier']
                del tweet_user_dict['name_tweet']

                dataBase.close()
                return tweet_user_dict
            else:
                dataBase.close()
                return {'message_error': 'TweetUser not found'}

        except Exception as e:
            cursorObject.close()
            dataBase.close()
            return {'message_error': str(e), 'section': 'getTweetUser'}
    else:
        error_message = dataBase[0]['message']
        return {'message_error': str(error_message)}

def getTweetUserByIdentifierIdUser(idUser, idTweet):
    dataBase = connect()
    if not isinstance(dataBase, list):
        cursorObject = dataBase.cursor()
        try:
            stmt = ("SELECT "
                    "tu.idTweetUser, "
                    "tu.idTweet, "
                    "tu.idUser, "
                    "u.username, "
                    "u.password, "
                    "t.identifier, "
                    "t.name_tweet "
                    "FROM tweet_user tu "
                    "LEFT JOIN user u ON tu.idUser = u.idUser "
                    "LEFT JOIN tweet t ON tu.idTweet = t.idTweet "
                    "WHERE tu.idUser = %s AND tu.idTweet = %s")
            cursorObject.execute(stmt, (idUser, idTweet))
            columns = [desc[0] for desc in cursorObject.description]
            result = cursorObject.fetchone()
            cursorObject.close()

            if result:
                tweet_user_dict = dict(zip(columns, result))

                # Estructura los datos de user y tweet como subdiccionarios
                user_info = {
                    'idUser': tweet_user_dict['idUser'],
                    'username': tweet_user_dict['username'],
                    'password': tweet_user_dict['password']
                }
                tweet_info = {
                    'idTweet': tweet_user_dict['idTweet'],
                    'identifier': tweet_user_dict['identifier'],
                    'name_tweet': tweet_user_dict['name_tweet']
                }

                tweet_user_dict['user'] = user_info
                tweet_user_dict['tweet'] = tweet_info

                # Elimina los campos principales de tweet_user
                del tweet_user_dict['username']
                del tweet_user_dict['password']
                del tweet_user_dict['identifier']
                del tweet_user_dict['name_tweet']

                dataBase.close()
                return tweet_user_dict

            else:
                dataBase.close()
                return []  # Devuelve una lista vacía si no hay coincidencia

        except Exception as e:
            cursorObject.close()
            dataBase.close()
            return {'message_error': str(e), 'section': 'getTweetUserByIdentifierIdUser'}
    else:
        error_message = dataBase[0]['message']
        return {'message_error': str(error_message)}

def postTweetUser(idUser, idTweet):
    dataBase = connect()
    if not isinstance(dataBase, list):
        cursorObject = dataBase.cursor()
        try:
            # Validar que el idUser y el idTweet existan
            check_user_stmt = "SELECT idUser,username,password FROM user WHERE idUser = %s"
            cursorObject.execute(check_user_stmt, (idUser,))
            existing_user = cursorObject.fetchone()

            check_tweet_stmt = "SELECT idTweet, identifier, name_tweet FROM tweet WHERE idTweet = %s"
            cursorObject.execute(check_tweet_stmt, (idTweet,))
            existing_tweet = cursorObject.fetchone()

            if not existing_user:
                cursorObject.close()
                dataBase.close()
                return {'message_error': 'El idUser no existe'}

            if not existing_tweet:
                cursorObject.close()
                dataBase.close()
                return {'message_error': 'El idTweet no existe'}

            # Verificar si la entrada ya existe en la tabla tweet_user
            check_tweet_user_stmt = "SELECT idTweetUser FROM tweet_user WHERE idUser = %s AND idTweet = %s"
            cursorObject.execute(check_tweet_user_stmt, (idUser, idTweet))
            existing_entry = cursorObject.fetchone()

            if existing_entry:
                cursorObject.close()
                dataBase.close()
                return {'message_error': 'Esta relación ya existe en la base de datos', 'section': 'postTweetUser'}

            # Si no existe, proceder a insertar la nueva relación en la tabla tweet_user
            insert_stmt = "INSERT INTO tweet_user (idUser, idTweet) VALUES (%s, %s)"
            cursorObject.execute(insert_stmt, (idUser, idTweet))
            dataBase.commit()
            new_tweet_user_id = cursorObject.lastrowid
            cursorObject.close()

            # Obtener la información de usuario y tweet
            user_info = {
                'idUser': idUser,
                'username': existing_user[1],  # Aquí asumimos que el primer campo es el username
                'password': existing_user[2]  # Suponiendo que el segundo campo es la contraseña
            }

            tweet_info = {
                'idTweet': idTweet,
                'identifier': existing_tweet[1],  # Suponiendo que el segundo campo es el identifier
                'name_tweet': existing_tweet[2]  # Suponiendo que el tercer campo es el nombre del tweet
            }

            dataBase.close()

            response = {'idTweetUser': new_tweet_user_id, 'idUser': idUser, 'idTweet': idTweet}
            response['user'] = user_info
            response['tweet'] = tweet_info

            return response

        except Exception as e:
            cursorObject.close()
            dataBase.close()
            return {'message_error': str(e), 'section': 'postTweetUser'}
    else:
        error_message = dataBase[0]['message']
        return {'message_error': str(error_message)}

def putTweetUser(idTweetUser, new_idUser, new_idTweet):
    dataBase = connect()
    if not isinstance(dataBase, list):
        cursorObject = dataBase.cursor()
        try:
            # Verificar si la entrada de tweet_user existe
            tweet_user_check_stmt = "SELECT idUser, idTweet FROM tweet_user WHERE idTweetUser = %s"
            cursorObject.execute(tweet_user_check_stmt, (idTweetUser,))
            existing_entry = cursorObject.fetchone()

            if existing_entry:
                current_idUser = existing_entry[0]
                current_idTweet = existing_entry[1]

                # Verificar si los nuevos valores son diferentes de los actuales
                if (new_idUser != current_idUser and new_idUser is not None) or (new_idTweet != current_idTweet and new_idTweet is not None):
                    # Verificar si el nuevo idUser existe
                    if new_idUser:
                        check_user_stmt = "SELECT idUser FROM user WHERE idUser = %s"
                        cursorObject.execute(check_user_stmt, (new_idUser,))
                        existing_user = cursorObject.fetchone()
                        if not existing_user:
                            cursorObject.close()
                            dataBase.close()
                            return {'message_error': 'El nuevo idUser no existe en la base de datos'}

                    # Verificar si el nuevo idTweet existe
                    if new_idTweet:
                        check_tweet_stmt = "SELECT idTweet FROM tweet WHERE idTweet = %s"
                        cursorObject.execute(check_tweet_stmt, (new_idTweet,))
                        existing_tweet = cursorObject.fetchone()
                        if not existing_tweet:
                            cursorObject.close()
                            dataBase.close()
                            return {'message_error': 'El nuevo idTweet no existe en la base de datos'}

                # Actualizar la relación tweet_user si todas las validaciones pasan
                update_stmt = "UPDATE tweet_user SET idUser = %s, idTweet = %s WHERE idTweetUser = %s"
                cursorObject.execute(update_stmt, (new_idUser, new_idTweet, idTweetUser))
                dataBase.commit()
                cursorObject.close()
                dataBase.close()

                return {'idTweetUser': idTweetUser, 'idUser': new_idUser, 'idTweet': new_idTweet}

            else:
                cursorObject.close()
                dataBase.close()
                return {'message_error': 'TweetUser entry not found'}

        except Exception as e:
            cursorObject.close()
            dataBase.close()
            return {'message_error': str(e), 'section': 'putTweetUser'}
    else:
        error_message = dataBase[0]['message']
        return {'message_error': str(error_message)}

def deleteTweetUser(idTweetUser):
    dataBase = connect()
    if not isinstance(dataBase, list):
        cursorObject = dataBase.cursor()
        try:
            tweet_user_check_stmt = "SELECT idTweetUser FROM tweet_user WHERE idTweetUser = %s"
            cursorObject.execute(tweet_user_check_stmt, (idTweetUser,))
            existing_tweet_user = cursorObject.fetchone()

            if existing_tweet_user:
                delete_stmt = "DELETE FROM tweet_user WHERE idTweetUser = %s"
                cursorObject.execute(delete_stmt, (idTweetUser,))
                dataBase.commit()
                cursorObject.close()
                dataBase.close()

                return {'message': f'TweetUser {existing_tweet_user[0]} deleted successfully'}

            else:
                cursorObject.close()
                dataBase.close()
                return {'message_error': 'TweetUser entry not found'}

        except Exception as e:
            cursorObject.close()
            dataBase.close()
            return {'message_error': str(e), 'section': 'deleteTweetUser'}
    else:
        error_message = dataBase[0]['message']
        return {'message_error': str(error_message)}
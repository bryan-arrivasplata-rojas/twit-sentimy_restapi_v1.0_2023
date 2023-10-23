from Connection.Connection import connect
def getCards():
    dataBase = connect()
    if not isinstance(dataBase, list):
        cursorObject = dataBase.cursor()
        try:
            stmt = "SELECT idCard, number, date, ccv FROM card"
            cursorObject.execute(stmt)
            columns = [desc[0] for desc in cursorObject.description]
            results = cursorObject.fetchall()
            cursorObject.close()

            cards = []
            for row in results:
                card_dict = dict(zip(columns, row))
                cards.append(card_dict)

            dataBase.close()
            return cards  # Convertir la lista de tarjetas a JSON

        except Exception as e:
            cursorObject.close()
            dataBase.close()
            return {'message_error': str(e), 'section': 'getCards'}
    else:
        error_message = dataBase[0]['message']
        return {'message_error': str(error_message)}

def getCard(idCard):
    dataBase = connect()
    if not isinstance(dataBase, list):
        cursorObject = dataBase.cursor()
        try:
            stmt = "SELECT idCard, number, date, ccv FROM card WHERE idCard = %s"
            cursorObject.execute(stmt, (idCard,))
            columns = [desc[0] for desc in cursorObject.description]
            result = cursorObject.fetchone()
            cursorObject.close()

            if result:
                card_dict = dict(zip(columns, result))
                dataBase.close()
                return card_dict

            else:
                dataBase.close()
                return {'message_error': 'Card not found'}

        except Exception as e:
            cursorObject.close()
            dataBase.close()
            return {'message_error': str(e), 'section': 'getCardById'}
    else:
        error_message = dataBase[0]['message']
        return {'message_error': str(error_message)}

def postCard(number, date, ccv):
    dataBase = connect()
    if not isinstance(dataBase, list):
        cursorObject = dataBase.cursor()
        try:
            # Verificar si el número de tarjeta ya existe
            check_stmt = "SELECT idCard FROM card WHERE number = %s"
            cursorObject.execute(check_stmt, (number,))
            existing_card = cursorObject.fetchone()

            if existing_card:
                cursorObject.close()
                dataBase.close()
                return {'message_error': 'El número de tarjeta ya está en uso', 'section': 'postCard'}

            # Si el número de tarjeta no existe, insertar la nueva tarjeta
            insert_stmt = "INSERT INTO card (number, date, ccv) VALUES (%s, %s, %s)"
            cursorObject.execute(insert_stmt, (number, date, ccv))
            dataBase.commit()
            new_card_id = cursorObject.lastrowid
            cursorObject.close()
            dataBase.close()
            return {'idCard': new_card_id, 'number': number, 'date': date, 'ccv': ccv}

        except Exception as e:
            cursorObject.close()
            dataBase.close()
            return {'message_error': str(e), 'section': 'postCard'}
    else:
        error_message = dataBase[0]['message']
        return {'message_error': str(error_message)}

def putCard(idCard, new_number, new_date, new_ccv):
    dataBase = connect()
    if not isinstance(dataBase, list):
        cursorObject = dataBase.cursor()
        try:
            # Verificar si la tarjeta existe
            card_check_stmt = "SELECT idCard, number FROM card WHERE idCard = %s"
            cursorObject.execute(card_check_stmt, (idCard,))
            existing_card = cursorObject.fetchone()

            if existing_card:
                current_number = existing_card['number']

                # Verificar si el nuevo número es diferente al número actual
                if new_number != current_number:
                    # Verificar si el nuevo número está en uso
                    check_stmt = "SELECT idCard FROM card WHERE number = %s"
                    cursorObject.execute(check_stmt, (new_number,))
                    existing_card_with_new_number = cursorObject.fetchone()

                    if existing_card_with_new_number:
                        cursorObject.close()
                        dataBase.close()
                        return {'message_error': 'El nuevo número de tarjeta ya está en uso', 'section': 'putCard'}

                # Si el nuevo número no está en uso o es el mismo, realizar la actualización
                update_stmt = "UPDATE card SET number = %s, date = %s, ccv = %s WHERE idCard = %s"
                cursorObject.execute(update_stmt, (new_number, new_date, new_ccv, idCard))
                dataBase.commit()
                cursorObject.close()
                dataBase.close()
                return {'idCard': idCard, 'number': new_number, 'date': new_date, 'ccv': new_ccv}

            else:
                cursorObject.close()
                dataBase.close()
                return {'message_error': 'Tarjeta no encontrada'}

        except Exception as e:
            cursorObject.close()
            dataBase.close()
            return {'message_error': str(e), 'section': 'putCard'}

    else:
        error_message = dataBase[0]['message']
        return {'message_error': str(error_message)}

def deleteCard(idCard):
    dataBase = connect()
    if not isinstance(dataBase, list):
        cursorObject = dataBase.cursor()
        try:
            card_check_stmt = "SELECT idCard FROM card WHERE idCard = %s"
            cursorObject.execute(card_check_stmt, (idCard,))
            existing_card = cursorObject.fetchone()

            if existing_card:
                delete_stmt = "DELETE FROM card WHERE idCard = %s"
                cursorObject.execute(delete_stmt, (idCard,))
                dataBase.commit()
                cursorObject.close()
                dataBase.close()
                return {'message': f'Card {existing_card[0]} eliminada con éxito'}

            else:
                cursorObject.close()
                dataBase.close()
                return {'message_error': 'Card not found'}

        except Exception as e:
            cursorObject.close()
            dataBase.close()
            return {'message_error': str(e), 'section': 'deleteCard'}

    else:
        error_message = dataBase[0]['message']
        return {'message_error': str(error_message)}
from Connection.Connection import connect
import json
from datetime import date

def format_birthdate(birthdate):
    return birthdate.strftime('%d-%m-%Y')

def getLogin(username, password):
    dataBase = connect()
    if not isinstance(dataBase, list):
        cursorObject = dataBase.cursor()
        try:
            stmt = ("SELECT "
                    "a.username,a.password,b.name_profile,b.lastName,b.birthdate,b.idRole,c.name_role "
                    "FROM "
                    "user a,"
                    "profile b,"
                    "role c "
                    "WHERE "
                    "b.idUser=a.idUser and "
                    "b.idRole=c.idRole and "
                    "a.username = %s")
            cursorObject.execute(stmt,(username,))
            columns = [desc[0] for desc in cursorObject.description]
            result = cursorObject.fetchone()
            cursorObject.close()

            if result:
                user_dict = dict(zip(columns, result))
                user_dict['birthdate'] = format_birthdate(user_dict['birthdate'])
                
                if user_dict['password'] == password:
                    dataBase.close()
                    return user_dict  # Devuelve los detalles del usuario en caso de validación exitosa
                else:
                    dataBase.close()
                    return {'message_error': 'Invalid password'}

            else:
                dataBase.close()
                return {'message_error': 'User not found'}

        except Exception as e:
            cursorObject.close()
            dataBase.close()
            return {'message_error': str(e), 'section': 'getLogin'}
    else:
        error_message = dataBase[0]['message']
        return {'message_error': str(error_message)}
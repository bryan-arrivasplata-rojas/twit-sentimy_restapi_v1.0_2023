from Connection.Connection import connect
import json
from datetime import date

def format_birthdate(birthdate):
    return birthdate.strftime('%d-%m-%Y')

def getUsers():
    dataBase = connect()
    if not isinstance(dataBase, list):
        cursorObject = dataBase.cursor()
        try:
            stmt = ("SELECT "
                    "a.idUser,a.username,a.password,b.name_profile,b.lastName,b.birthdate,b.idRole,c.name_role "
                    "FROM "
                    "user a,"
                    "profile b,"
                    "role c "
                    "WHERE "
                    "b.idUser=a.idUser and "
                    "b.idRole=c.idRole "
                    "ORDER BY "
                    "a.username ASC")
            cursorObject.execute(stmt)
            columns = [desc[0] for desc in cursorObject.description]
            results = cursorObject.fetchall()
            cursorObject.close()

            users = []
            for row in results:
                user_dict = dict(zip(columns, row))
                user_dict['birthdate'] = format_birthdate(user_dict['birthdate'])  # Formatea la fecha
                users.append(user_dict)

            dataBase.close()
            return users  # Convert the list to JSON
        except Exception as e:
            cursorObject.close()
            dataBase.close()
            return {'message_error': str(e),'section': 'getUserAll'}
    else:
        error_message = dataBase[0]['message']
        return {'message_error': str(error_message)}

def getUser(idUser):
    dataBase = connect()
    if not isinstance(dataBase, list):
        cursorObject = dataBase.cursor()
        try:
            stmt = ("SELECT "
                    "a.idUser,a.username,a.password,b.name_profile,b.lastName,b.birthdate,b.idRole,c.name_role "
                    "FROM "
                    "user a,"
                    "profile b,"
                    "role c "
                    "WHERE "
                    "b.idUser=a.idUser and "
                    "b.idRole=c.idRole and "
                    "a.idUser = %s")
            cursorObject.execute(stmt,(idUser,))
            columns = [desc[0] for desc in cursorObject.description]
            result = cursorObject.fetchone()
            cursorObject.close()

            if result:
                user_dict = dict(zip(columns, result))
                user_dict['birthdate'] = format_birthdate(user_dict['birthdate'])
                dataBase.close()
                return user_dict  # Devuelve el usuario encontrado como un diccionario
            else:
                dataBase.close()
                return {'message_error': 'User not found'}

        except Exception as e:
            cursorObject.close()
            dataBase.close()
            return {'message_error': str(e), 'section': 'getUser'}
    else:
        error_message = dataBase[0]['message']
        return {'message_error': str(error_message)}
    
def postUser(username, password):
    dataBase = connect()
    if not isinstance(dataBase, list):
        cursorObject = dataBase.cursor()
        try:
            # Verificar si el username ya existe
            check_stmt = "SELECT idUser FROM user WHERE username = %s"
            cursorObject.execute(check_stmt, (username,))
            existing_user = cursorObject.fetchone()

            if existing_user:
                cursorObject.close()
                dataBase.close()
                return {'message_error': 'El username ya está en uso', 'section': 'postUser'}

            # Si el username no existe, insertar el nuevo usuario
            insert_stmt = "INSERT INTO user (username, password) VALUES (%s, %s)"
            cursorObject.execute(insert_stmt, (username, password))
            dataBase.commit()
            new_user_id = cursorObject.lastrowid
            cursorObject.close()
            dataBase.close()
            return {'idUser': new_user_id, 'user': username, 'password': password}

        except Exception as e:
            cursorObject.close()
            dataBase.close()
            return {'message_error': str(e), 'section': 'postUser'}
    else:
        error_message = dataBase[0]['message']
        return {'message_error': str(error_message)}


def putUser(idUser, new_password):
    dataBase = connect()
    if not isinstance(dataBase, list):
        cursorObject = dataBase.cursor()
        try:
            # Verifica si el idUser existe antes de actualizar la contraseña
            user_check_stmt = "SELECT idUser,username FROM user WHERE idUser = %s"
            cursorObject.execute(user_check_stmt, (idUser,))
            existing_user = cursorObject.fetchone()

            if existing_user:
                # El idUser existe, ahora actualiza la contraseña
                update_stmt = "UPDATE user SET password = %s WHERE idUser = %s"
                cursorObject.execute(update_stmt, (new_password, idUser))
                dataBase.commit()
                cursorObject.close()
                dataBase.close()
                return {'idUser': idUser, 'username': existing_user[1], 'password': new_password}

            else:
                cursorObject.close()
                dataBase.close()
                return {'message_error': 'User not found'}

        except Exception as e:
            cursorObject.close()
            dataBase.close()
            return {'message_error': str(e), 'section': 'putUser'}

    else:
        error_message = dataBase[0]['message']
        return {'message_error': str(error_message)}
    
def deleteUser(idUser):
    dataBase = connect()
    if not isinstance(dataBase, list):
        cursorObject = dataBase.cursor()
        try:
            # Verifica si el idUser existe antes de eliminar al usuario
            user_check_stmt = "SELECT idUser FROM user WHERE idUser = %s"
            cursorObject.execute(user_check_stmt, (idUser,))
            existing_user = cursorObject.fetchone()

            if existing_user:
                # El idUser existe, ahora elimina al usuario
                delete_stmt = "DELETE FROM user WHERE idUser = %s"
                cursorObject.execute(delete_stmt, (idUser,))
                dataBase.commit()
                cursorObject.close()
                dataBase.close()

                return {'message': f'Usuario {existing_user[0]} eliminado con éxito'}

            else:
                cursorObject.close()
                dataBase.close()
                return {'message_error': 'Usuario no encontrado'}

        except Exception as e:
            cursorObject.close()
            dataBase.close()
            return {'message_error': str(e), 'section': 'deleteUser'}

    else:
        error_message = dataBase[0]['message']
        return {'message_error': str(error_message)}
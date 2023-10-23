from Connection.Connection import connect
import json
from datetime import date

def format_birthdate(birthdate):
    return birthdate.strftime('%d-%m-%Y')

def getProfiles():
    dataBase = connect()
    if not isinstance(dataBase, list):
        cursorObject = dataBase.cursor()
        try:
            stmt = ("SELECT "
                    "p.idProfile, "
                    "p.name_profile, "
                    "p.lastName, "
                    "p.birthdate, "
                    "u.idUser, "
                    "u.username, "
                    "u.password, "
                    "r.idRole, "
                    "r.name_role, "
                    "c.idCard, "
                    "c.number, "
                    "c.date, "
                    "c.ccv "
                    "FROM profile p "
                    "LEFT JOIN user u ON p.idUser = u.idUser "
                    "LEFT JOIN role r ON p.idRole = r.idRole "
                    "LEFT JOIN card c ON p.idCard = c.idCard")
            cursorObject.execute(stmt)
            columns = [desc[0] for desc in cursorObject.description]
            results = cursorObject.fetchall()
            cursorObject.close()

            profiles = []
            for row in results:
                profile_dict = dict(zip(columns, row))
                # Formatea la fecha de nacimiento
                profile_dict['birthdate'] = format_birthdate(profile_dict['birthdate'])

                # Estructura los datos de user, role y card como subdiccionarios
                user_info = {
                    'idUser': profile_dict['idUser'],
                    'username': profile_dict['username'],
                    'password': profile_dict['password']
                }
                role_info = {
                    'idRole': profile_dict['idRole'],
                    'name_role': profile_dict['name_role']
                }
                card_info = {
                    'idCard': profile_dict['idCard'],
                    'number': profile_dict['number'],
                    'date': profile_dict['date'],
                    'ccv': profile_dict['ccv']
                }

                # Reemplaza campos nulos o vacíos con diccionarios vacíos
                if user_info['idUser'] is None:
                    user_info = {}
                if role_info['idRole'] is None:
                    role_info = {}
                if card_info['idCard'] is None:
                    card_info = {}

                profile_dict['user'] = user_info
                profile_dict['role'] = role_info
                profile_dict['card'] = card_info

                # Elimina los campos principales de profile
                del profile_dict['username']
                del profile_dict['password']
                del profile_dict['name_role']
                del profile_dict['number']
                del profile_dict['date']
                del profile_dict['ccv']


                profiles.append(profile_dict)

            dataBase.close()
            return profiles

        except Exception as e:
            cursorObject.close()
            dataBase.close()
            return {'message_error': str(e), 'section': 'getProfiles'}
    else:
        error_message = dataBase[0]['message']
        return {'message_error': str(error_message)}
    
def getProfile(idProfile):
    dataBase = connect()
    if not isinstance(dataBase, list):
        cursorObject = dataBase.cursor()
        try:
            stmt = ("SELECT "
                    "p.idProfile, "
                    "p.name_profile, "
                    "p.lastName, "
                    "p.birthdate, "
                    "u.idUser, "
                    "u.username, "
                    "u.password, "
                    "r.idRole, "
                    "r.name_role, "
                    "c.idCard, "
                    "c.number, "
                    "c.date, "
                    "c.ccv "
                    "FROM profile p "
                    "LEFT JOIN user u ON p.idUser = u.idUser "
                    "LEFT JOIN role r ON p.idRole = r.idRole "
                    "LEFT JOIN card c ON p.idCard = c.idCard "
                    "WHERE p.idProfile = %s")
            cursorObject.execute(stmt, (idProfile,))
            columns = [desc[0] for desc in cursorObject.description]
            result = cursorObject.fetchone()
            cursorObject.close()
            if result:
                profile_dict = dict(zip(columns, result))
                # Formatea la fecha de nacimiento
                profile_dict['birthdate'] = format_birthdate(profile_dict['birthdate'])

                # Estructura los datos de user, role y card como subdiccionarios
                user_info = {
                    'idUser': profile_dict['idUser'],
                    'username': profile_dict['username'],
                    'password': profile_dict['password']
                }
                role_info = {
                    'idRole': profile_dict['idRole'],
                    'name_role': profile_dict['name_role']
                }
                card_info = {
                    'idCard': profile_dict['idCard'],
                    'number': profile_dict['number'],
                    'date': profile_dict['date'],
                    'ccv': profile_dict['ccv']
                }

                # Reemplaza campos nulos o vacíos con diccionarios vacíos
                if user_info['idUser'] is None:
                    user_info = {}
                if role_info['idRole'] is None:
                    role_info = {}
                if card_info['idCard'] is None:
                    card_info = {}

                profile_dict['user'] = user_info
                profile_dict['role'] = role_info
                profile_dict['card'] = card_info

                # Elimina los campos principales de profile
                del profile_dict['username']
                del profile_dict['password']
                del profile_dict['name_role']
                del profile_dict['number']
                del profile_dict['date']
                del profile_dict['ccv']

                dataBase.close()
                return profile_dict

            else:
                dataBase.close()
                return {'message_error': 'Profile not found'}

        except Exception as e:
            cursorObject.close()
            dataBase.close()
            return {'message_error': str(e), 'section': 'getProfile'}
    else:
        error_message = dataBase[0]['message']
        return {'message_error': str(error_message)}

def postProfile(name_profile, lastName, birthdate, idUser, idRole, idCard):
    dataBase = connect()
    if not isinstance(dataBase, list):
        cursorObject = dataBase.cursor()
        try:
            # Validar que el idUser no esté en uso
            check_user_stmt = "SELECT idUser FROM user WHERE idUser = %s"
            cursorObject.execute(check_user_stmt, (idUser,))
            existing_user = cursorObject.fetchone()

            if existing_user:
                cursorObject.close()
                dataBase.close()
                return {'message_error': 'Usuario a asignar actualmente en uso'}

            # Validar que el idCard no esté en uso
            check_card_stmt = "SELECT idCard FROM card WHERE idCard = %s"
            cursorObject.execute(check_card_stmt, (idCard,))
            existing_card = cursorObject.fetchone()

            if existing_card:
                cursorObject.close()
                dataBase.close()
                return {'message_error': 'Card a asignar actualmente en uso'}

            # Si ambas validaciones pasan, procede a insertar el perfil
            insert_stmt = ("INSERT INTO profile (name_profile, lastName, birthdate, idUser, idRole, idCard) "
                           "VALUES (%s, %s, %s, %s, %s, %s)")
            cursorObject.execute(insert_stmt, (name_profile, lastName, birthdate, idUser, idRole, idCard))
            dataBase.commit()
            new_profile_id = cursorObject.lastrowid
            cursorObject.close()
            dataBase.close()

            return {'idProfile': new_profile_id, 'name_profile': name_profile, 'lastName': lastName,
                    'birthdate': birthdate, 'idUser': idUser, 'idRole': idRole, 'idCard': idCard}

        except Exception as e:
            cursorObject.close()
            dataBase.close()
            return {'message_error': str(e), 'section': 'postProfile'}
    else:
        error_message = dataBase[0]['message']
        return {'message_error': str(error_message)}

def putProfile(idProfile, new_name_profile, new_lastName, new_birthdate, new_idUser, new_idRole, new_idCard):
    dataBase = connect()
    if not isinstance(dataBase, list):
        cursorObject = dataBase.cursor()
        try:
            # Verificar si el perfil existe
            profile_check_stmt = "SELECT idProfile, idUser, idCard FROM profile WHERE idProfile = %s"
            cursorObject.execute(profile_check_stmt, (idProfile,))
            existing_profile = cursorObject.fetchone()

            if existing_profile:
                # Obtener los valores actuales de idUser e idCard
                current_idUser = existing_profile[1]
                current_idCard = existing_profile[2]

                # Verificar si los nuevos idUser e idCard son diferentes de los actuales
                if (new_idUser != current_idUser and new_idUser is not None) or (new_idCard != current_idCard and new_idCard is not None):
                    # Verificar si el nuevo idUser ya está en uso
                    if new_idUser:
                        check_user_stmt = "SELECT idUser FROM user WHERE idUser = %s"
                        cursorObject.execute(check_user_stmt, (new_idUser,))
                        existing_user = cursorObject.fetchone()
                        if existing_user:
                            cursorObject.close()
                            dataBase.close()
                            return {'message_error': 'El nuevo idUser está actualmente en uso'}

                    # Verificar si el nuevo idCard ya está en uso
                    if new_idCard:
                        check_card_stmt = "SELECT idCard FROM card WHERE idCard = %s"
                        cursorObject.execute(check_card_stmt, (new_idCard,))
                        existing_card = cursorObject.fetchone()
                        if existing_card:
                            cursorObject.close()
                            dataBase.close()
                            return {'message_error': 'El nuevo idCard está actualmente en uso'}

                # Actualizar el perfil si todas las validaciones pasan
                update_stmt = ("UPDATE profile "
                               "SET name_profile = %s, lastName = %s, birthdate = %s, idUser = %s, idRole = %s, idCard = %s "
                               "WHERE idProfile = %s")
                cursorObject.execute(update_stmt, (new_name_profile, new_lastName, new_birthdate,
                                                  new_idUser, new_idRole, new_idCard, idProfile))
                dataBase.commit()
                cursorObject.close()
                dataBase.close()

                return {'idProfile': idProfile, 'name_profile': new_name_profile, 'lastName': new_lastName,
                        'birthdate': new_birthdate, 'idUser': new_idUser, 'idRole': new_idRole, 'idCard': new_idCard}

            else:
                cursorObject.close()
                dataBase.close()
                return {'message_error': 'Profile not found'}

        except Exception as e:
            cursorObject.close()
            dataBase.close()
            return {'message_error': str(e), 'section': 'putProfile'}

    else:
        error_message = dataBase[0]['message']
        return {'message_error': str(error_message)}

def deleteProfile(idProfile):
    dataBase = connect()
    if not isinstance(dataBase, list):
        cursorObject = dataBase.cursor()
        try:
            profile_check_stmt = "SELECT idProfile FROM profile WHERE idProfile = %s"
            cursorObject.execute(profile_check_stmt, (idProfile,))
            existing_profile = cursorObject.fetchone()

            if existing_profile:
                delete_stmt = "DELETE FROM profile WHERE idProfile = %s"
                cursorObject.execute(delete_stmt, (idProfile,))
                dataBase.commit()
                cursorObject.close()
                dataBase.close()

                return {'message': f'Profile {existing_profile[0]} eliminado con éxito'}

            else:
                cursorObject.close()
                dataBase.close()
                return {'message_error': 'Profile not found'}

        except Exception as e:
            cursorObject.close()
            dataBase.close()
            return {'message_error': str(e), 'section': 'deleteProfile'}

    else:
        error_message = dataBase[0]['message']
        return {'message_error': str(error_message)}
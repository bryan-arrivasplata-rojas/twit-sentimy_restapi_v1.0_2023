from Connection.Connection import connect
def getRoles():
    dataBase = connect()
    if not isinstance(dataBase, list):
        cursorObject = dataBase.cursor()
        try:
            stmt = "SELECT idRole, name_role FROM role"
            cursorObject.execute(stmt)
            columns = [desc[0] for desc in cursorObject.description]
            results = cursorObject.fetchall()
            cursorObject.close()

            roles = []
            for row in results:
                role_dict = dict(zip(columns, row))
                roles.append(role_dict)

            dataBase.close()
            return roles  # Convertir la lista de roles a JSON

        except Exception as e:
            cursorObject.close()
            dataBase.close()
            return {'message_error': str(e), 'section': 'getRoles'}
    else:
        error_message = dataBase[0]['message']
        return {'message_error': str(error_message)}
    
def getRole(idRole):
    dataBase = connect()
    if not isinstance(dataBase, list):
        cursorObject = dataBase.cursor()
        try:
            stmt = "SELECT idRole, name_role FROM role WHERE idRole = %s"
            cursorObject.execute(stmt, (idRole,))
            columns = [desc[0] for desc in cursorObject.description]
            result = cursorObject.fetchone()
            cursorObject.close()

            if result:
                role_dict = dict(zip(columns, result))
                dataBase.close()
                return role_dict

            else:
                dataBase.close()
                return {'message_error': 'Role not found'}

        except Exception as e:
            cursorObject.close()
            dataBase.close()
            return {'message_error': str(e), 'section': 'getRoleById'}
    else:
        error_message = dataBase[0]['message']
        return {'message_error': str(error_message)}

def postRole(name_role):
    dataBase = connect()
    if not isinstance(dataBase, list):
        cursorObject = dataBase.cursor()
        try:
            # Verificar si el nombre de rol ya existe en la tabla
            check_stmt = "SELECT idRole FROM role WHERE name_role = %s"
            cursorObject.execute(check_stmt, (name_role,))
            existing_role = cursorObject.fetchone()

            if existing_role:
                cursorObject.close()
                dataBase.close()
                return {'message_error': 'El rol ya existe en la base de datos', 'section': 'postRole'}
            
            # Si el nombre de rol no existe, proceder a insertar el nuevo rol
            insert_stmt = "INSERT INTO role (name_role) VALUES (%s)"
            cursorObject.execute(insert_stmt, (name_role,))
            dataBase.commit()
            new_role_id = cursorObject.lastrowid
            cursorObject.close()
            dataBase.close()
            return {'idRole': new_role_id, 'name_role': name_role}

        except Exception as e:
            cursorObject.close()
            dataBase.close()
            return {'message_error': str(e), 'section': 'postRole'}
    else:
        error_message = dataBase[0]['message']
        return {'message_error': str(error_message)}

def putRole(idRole, new_name_role):
    dataBase = connect()
    if not isinstance(dataBase, list):
        cursorObject = dataBase.cursor()
        try:
            # Verifica si el idRole existe antes de actualizar los datos del rol
            role_check_stmt = "SELECT idRole, name_role FROM role WHERE idRole = %s"
            cursorObject.execute(role_check_stmt, (idRole,))
            existing_role = cursorObject.fetchone()

            if existing_role:
                current_name_role = existing_role[1]  # Nombre de rol actual

                # Verificar si el nuevo nombre de rol es diferente del actual
                if new_name_role != current_name_role:
                    # Comprobar si el nuevo nombre de rol ya existe en la tabla
                    check_stmt = "SELECT idRole FROM role WHERE name_role = %s"
                    cursorObject.execute(check_stmt, (new_name_role,))
                    existing_rol_with_new_name_role = cursorObject.fetchone()

                    if existing_rol_with_new_name_role:
                        cursorObject.close()
                        dataBase.close()
                        return {'message_error': 'El nuevo nombre de rol ya existe en la base de datos', 'section': 'putRole'}

                # El idRole existe y el nuevo nombre no está duplicado, actualizar los datos del rol
                update_stmt = "UPDATE role SET name_role = %s WHERE idRole = %s"
                cursorObject.execute(update_stmt, (new_name_role, idRole))
                dataBase.commit()
                cursorObject.close()
                dataBase.close()
                return {'idRole': idRole, 'name_role': new_name_role}

            else:
                cursorObject.close()
                dataBase.close()
                return {'message_error': 'Role not found'}

        except Exception as e:
            cursorObject.close()
            dataBase.close()
            return {'message_error': str(e), 'section': 'putRole'}

    else:
        error_message = dataBase[0]['message']
        return {'message_error': str(error_message)}

def deleteRole(idRole):
    dataBase = connect()
    if not isinstance(dataBase, list):
        cursorObject = dataBase.cursor()
        try:
            # Verifica si el idRole existe antes de eliminar el rol
            role_check_stmt = "SELECT idRole FROM role WHERE idRole = %s"
            cursorObject.execute(role_check_stmt, (idRole,))
            existing_role = cursorObject.fetchone()

            if existing_role:
                # El idRole existe, ahora elimina el rol
                delete_stmt = "DELETE FROM role WHERE idRole = %s"
                cursorObject.execute(delete_stmt, (idRole,))
                dataBase.commit()
                cursorObject.close()
                dataBase.close()
                return {'message': f'Role {existing_role[0]} eliminado con éxito'}

            else:
                cursorObject.close()
                dataBase.close()
                return {'message_error': 'Role not found'}

        except Exception as e:
            cursorObject.close()
            dataBase.close()
            return {'message_error': str(e), 'section': 'deleteRole'}

    else:
        error_message = dataBase[0]['message']
        return {'message_error': str(error_message)}
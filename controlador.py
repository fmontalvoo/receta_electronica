from conexion_db import obtener_conexion

conexion = obtener_conexion()

def recuperar_sesion(correo, clave):
    with conexion.cursor() as cursor:
        sql = "SELECT clave, rol FROM usuario WHERE correo=%s AND clave=%s"
        cursor.execute(sql, (correo,clave))
        result = cursor.fetchone()
        print(result)
        if result != None:
            clave = result['clave']
            rol = result['rol']
            print(clave, rol)
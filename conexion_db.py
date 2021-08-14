import pymysql

from decouple import config

def obtener_conexion():
    return pymysql.connect(host='localhost',
                             user=config('DB_USER'),
                             password=config('DB_PASSWORD'),
                             database=config('DATABASE'),
                             cursorclass=pymysql.cursors.DictCursor)
import mysql.connector
from mysql.connector import Error

class RepositorioBase:
    def __init__(self): #Clase para conectar
        try:
            self.conn = mysql.connector.connect(
                host="localhost",      
                user="Usuario",      
                password="1234",
                database="checkrealdb"
            )

            if self.conn.is_connected():
                print("Conexión exitosa a MySQL")
                self.cursor = self.conn.cursor()

        except Error as e:
            print("Error al conectar a MySQL:", e)
            self.conn = None
            self.cursor = None
    
    def Conexion(self):
        return self.conn
    
    def Cursor(self):
        return self.cursor
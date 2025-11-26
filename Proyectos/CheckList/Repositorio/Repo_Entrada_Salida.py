#Repositorio referente a Entradas y Salidas (ALTAS)
from mysql.connector import Error
from Repositorio.repo_base import RepositorioBase

# ==ENTRADAS==
class RepoEntrada:
    def __init__(self):
        base = RepositorioBase()
        self.conn = base.Conexion()
        self.cursor = base.Cursor()

    def RInsertarEntrada(self,objEntrada):
        try:
            self.cursor.execute(
                "INSERT INTO entrada (ID_Personal,Horario) VALUES (%s,%s);",
                (objEntrada.IdPersonal,objEntrada.Horario)
            )
            self.conn.commit()
            return True
        except Error as e:
            print("Error al guardar:", e)
            return False

    def RListarEntradas(self):
        try:
            self.cursor.execute("SELECT * FROM entrada order by ID_Entrada;")
            return self.cursor.fetchall()  # lista de tuplas
        except Error:
            return f"Error al listar: {Error}"
        
    def RInsertarSalida(self,objSalida):
        try:
            self.cursor.execute(
                "INSERT INTO salida (ID_Personal,Horario) VALUES (%s,%s);",
                (objSalida.IdPersonal,objSalida.Horario)
            )
            self.conn.commit()
            return True
        except Error as e:
            print("Error al guardar:", e)
            return False
        
    def RListarSalida(self):
        try:
            self.cursor.execute("SELECT * FROM salida order by ID_Salida;")
            return self.cursor.fetchall()  # lista de tuplas
        except Error:
            return f"Error al listar: {Error}"
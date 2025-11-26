#Repositorio referente a Personal (ABM)
from mysql.connector import Error
from Repositorio.repo_base import RepositorioBase
from model.Empleados import Personal
class AbmPersonal:
    def __init__(self):
        base = RepositorioBase()
        self.conn = base.Conexion()
        self.cursor = base.Cursor()

    def RInsertarPersonal(self, Nombre, Apellido, Dni, IdUsuario):
        try:
            self.cursor.execute(
                "INSERT INTO personal (Nombre,Apellido,DNI,ID_Usuario) VALUES (%s,%s,%s,%s);",
                (Nombre,Apellido,Dni,IdUsuario)
            )
            self.conn.commit()
            return True
        except Error as e:
            print("Error al guardar:", e)
            return False
    
    def RInsertarUsuario(self, Usuario, Clave, Rol):
        try:
            self.cursor.execute(
                "INSERT INTO usuarios (Usuario,Clave,Rol) VALUES (%s,%s,%s);",
                (Usuario,Clave,Rol)
            )
            self.conn.commit()
            return True
        except Error as e:
            print("Error al guardar:", e)
            return False
    
    def RBuscarIDUsuario(self, Usuario, Clave): #Metodo para Buscar el Id_Usuario del personal
        try:
            self.cursor.execute(
                "select ID_Usuario from usuarios where Usuario=%s and Clave=%s;",
                (Usuario, Clave))
            registros = self.cursor.fetchone() #Obtengo los registros
            resultado = registros[0] #Obtengo el primer registro
            if isinstance(resultado, int): #verifico si el primer registro es int
                return resultado #Lo devuelvo
            else:
                return False #Si no envio error como bool
        except Error as e:
            return f"Error al consultar → {e}"
    
    def RListar_todos(self):
        try:
            self.cursor.execute("SELECT Nombre,Apellido,DNI FROM personal order by ID_Personal;")
            return self.cursor.fetchall()  # lista de tuplas
        except Error:
            return f"Error al listar: {Error}"
        
    def RBuscarUsuario(self,Nombre,Apellido): #Metodo para Buscar Usuario por nombre y apellido
        try:
            self.cursor.execute(
                "SELECT ID_Personal FROM personal WHERE nombre=%s and apellido=%s;",
                (Nombre,Apellido))
            registros = self.cursor.fetchone() #Obtengo los registros
            resultado = registros[0] #Obtengo el primer registro
            if isinstance(resultado, int): #verifico si el primer registro es int
                return resultado #Lo devuelvo
            else:
                return False #Si no envio error como bool
        except Error as e:
            return f"Error al consultar → {e}" 
    
    def RLogin(self,Usuario,Clave): #Metodo para Buscar Usuario por nombre y apellido
        try:
            self.cursor.execute(
                "SELECT Rol, ID_Personal FROM usuarios inner join personal on usuarios.Usuario=%s and usuarios.Clave=%s where usuarios.ID_Usuario = personal.ID_Usuario;",
                (Usuario,Clave))
            registros = self.cursor.fetchone() #Obtengo los registros
            
            if registros is None: #Veriico si hay registros
                return None
            #Creo el Objeto Personal para pasarle los datos de Rol y ID_Personal
            objPersonal = Personal()
            objPersonal.rol = registros[0] #Obtengo el primer registro
            objPersonal.IdEmpleado = registros[1]
            return objPersonal
        except Error as e:
            return f"Error al consultar → {e}" 
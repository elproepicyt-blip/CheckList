from Repositorio.repo_Personal import AbmPersonal

class ServicioPersonal:
    def __init__(self):
        self.repoP = AbmPersonal()

    def procesar_boton1(self):
        dato = self.repoP.consultar_algo()
        return f"Botón 1 consultó la BD y obtuvo: {dato}"

    def SInsertarPersonal(self,Nombre,Apellido,Dni,IdUsuario):
        exito = self.repoP.RInsertarPersonal(Nombre,Apellido,Dni,IdUsuario)
        return "Guardado correctamente" if exito else "Error guardando"
    
    def SInsertarUsuario(self,Usuario,Clave,Rol):
        exito = self.repoP.RInsertarUsuario(Usuario,Clave,Rol)
        return "Guardado correctamente" if exito else "Error guardando"
    
    def SBuscarIDUsuario(self,Usuario, Clave):
        return self.repoP.RBuscarIDUsuario(Usuario, Clave)
    
    def SListar_todos(self):
        return self.repoP.RListar_todos()
    
    def SInsertarEntrada(self):
        return self.repoP.RInsertarEntrada()
    
    def SBuscarUsuario(self,Nombre,Apellido):
        return self.repoP.RBuscarUsuario(Nombre,Apellido)
    
    def SLogin(self,Usuario,Clave):
        return self.repoP.RLogin(Usuario,Clave)
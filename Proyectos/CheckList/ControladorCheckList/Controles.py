from services.ServicioPersonal import ServicioPersonal
from services.ServicioEntradaSalida import ServicioEntradaSalida

class Controlador:
    def __init__(self):
        self.servicio = ServicioPersonal()
        self.servicioE_S = ServicioEntradaSalida()

    def CInsertarPersonal(self,Nombre,Apellido,Dni,IdUsuario): #PERSONAL
        return self.servicio.SInsertarPersonal(Nombre,Apellido,Dni,IdUsuario)
    
    def CInsertarUsuario(self,Usuario,Clave,Rol): #PERSONAL
        return self.servicio.SInsertarUsuario(Usuario,Clave,Rol)
    
    def CBuscarIDUsuario(self,Usuario, Clave): #PERSONAL
        return self.servicio.SBuscarIDUsuario(Usuario, Clave)
    
    def CListar(self): #PERSONAL
        return self.servicio.SListar_todos()
    
    def CInsertarEntrada(self,objEntrada):
        return self.servicioE_S.SInsertarEntrada(objEntrada)
    
    def CListarEntradas(self):
        return self.servicioE_S.SListarEntradas()
    
    def CInsertarSalida(self,objSalida):
        return self.servicioE_S.SInsertarSalida(objSalida)
    
    def CListarSalida(self):
        return self.servicioE_S.SListarSalida()

    def CBuscarUsuario(self,Nombre,Apellido): #PERSONAL
        return self.servicio.SBuscarUsuario(Nombre,Apellido)
    
    def CLogin(self,Usuario,Clave):
        return self.servicio.SLogin(Usuario,Clave)
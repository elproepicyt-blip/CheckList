from datetime import datetime
from model.Horarios import Horarios

class Asistencias:
    def __init__(self):
        self.registros = []
    
    def RegistrarEntrada(self,EmpleadoId):
        registro = Horarios(EmpleadoId)
        self.registros.append(registro)
        return registro
    
    def RegistrarSalida(self,EmpleadoId):
        for registro in reversed(self.registros):
            if registro.Empleado_Id == EmpleadoId & registro.H_S is None:
                registro.H_S = datetime.now()
                return registro
        return None
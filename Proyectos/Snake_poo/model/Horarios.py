class Horarios:
    def __init__(self,Empleado_Id,HorarioEntrada=None,HorarioSalida=None):
        self.EmpleadoID = Empleado_Id
        self.H_E = HorarioEntrada
        self.H_S = HorarioSalida
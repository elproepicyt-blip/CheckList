#Servicio referente a Entradas y Salidas
from Repositorio.Repo_Entrada_Salida import RepoEntrada

# ==ENTRADAS==
class ServicioEntradaSalida:
    def __init__(self):
        self.repoE_S = RepoEntrada()

    def SListar_todos(self):
        return self.repoE_S.RListar_todos()

    def SInsertarEntrada(self,objEntrada):
        return self.repoE_S.RInsertarEntrada(objEntrada)

    def SListarEntradas(self):
        return self.repoE_S.RListarEntradas()

    # ==SALIDAS==
    def SInsertarSalida(self,objSalida):
        return self.repoE_S.RInsertarSalida(objSalida)

    def SListarSalida(self):
        return self.repoE_S.RListarSalida()
import tkinter as tk
from ControladorCheckList.Controles import Controlador
from datetime import date, datetime
from model.Entrada import Entrada
from model.Salida import Salida
from tkinter import messagebox
from mysql.connector import Error

class VentanaLogin:
    def __init__(self):
        self.controller = Controlador()

        self.VentanaLogin = tk.Tk()
        self.VentanaLogin.title("CheckList - Login")
        self.VentanaLogin.geometry("350x250")

        tk.Label(self.VentanaLogin, text="Usuario:").pack(pady=5)
        self.userEntry = tk.Entry(self.VentanaLogin, width=30)
        self.userEntry.pack()

        tk.Label(self.VentanaLogin, text="Contraseña:").pack(pady=5)
        self.passEntry = tk.Entry(self.VentanaLogin, width=30, show="*")
        self.passEntry.pack()

        tk.Button(self.VentanaLogin, text="Ingresar", command=self.Login).pack(pady=15)
    
    def iniciar(self):
        self.VentanaLogin.mainloop()

    # LOGIN GENERAL (ADMIN O USUARIO)
    def Login(self):
        Usuario = self.userEntry.get()
        Clave = self.passEntry.get()

        datos = self.controller.CLogin(Usuario, Clave)

        if datos is None:
            messagebox.showerror("Error", "Usuario o clave incorrectos")
            return

        Rol = datos.rol     # Admin / Usuario
        Id = datos.IdEmpleado  # ID en base

        messagebox.showinfo("Login correcto", "Bienvenido")

        self.VentanaLogin.withdraw()

        if Rol == "admin":
            VentanaPrincipalAdmin(self.VentanaLogin,Id)
        else:
            VentanaPrincipalUsuario(self.VentanaLogin,Id)

#Ventanas Usuario
class VentanaPrincipalUsuario: #Ventana Principal que ve el usuario al entrar
    def __init__(self,VtnPadre,Id):
        self.VtnPadre = VtnPadre
        self.id = Id
        self.ventanaMenuU = tk.Toplevel(self.VtnPadre)
        self.ventanaMenuU.title("CheckList App")
        self.ventanaMenuU.geometry("350x200")
        
        #Boton Atras
        self.btnAtras = tk.Button(self.ventanaMenuU, text="Atras", command=self.Atras)
        self.btnAtras.pack(side="top", anchor="w", padx=10, pady=20)
        
        #Boton Registrar Entrada
        self.btnRegistrarE = tk.Button(self.ventanaMenuU, text="Marcar Entrada", command=self.RegistrarEntrada)
        self.btnRegistrarE.pack(pady=10)
        
        #Boton Registrar Salida
        self.btnRegistrarS = tk.Button(self.ventanaMenuU, text="Marcar Salida", command=self.RegistrarSalida)
        self.btnRegistrarS.pack(pady=10)
        
    def RegistrarEntrada(self):
        VentanaAgregarEntrada(self.ventanaMenuU,self.id)
        
    def RegistrarSalida(self):
        VentanaAgregarSalida(self.ventanaMenuU,self.id)
        
    def Atras(self): #Accion del boton Atras
        self.ventanaMenuU.destroy() # Cierro mi ventana Actual (Usuario)
        self.VtnPadre.deiconify()   #Muestro la Ventana Login
        
#Ventanas Admin
class VentanaPrincipalAdmin: #Ventana Principal que ve el usuario al entrar
    def __init__(self,VtnPadre,Id):
        self.id = Id
        self.VtnPadre = VtnPadre
        self.ventanaMenuA = tk.Toplevel(self.VtnPadre)
        self.ventanaMenuA.title("CheckList App")
        self.ventanaMenuA.geometry("350x200")
        
        #Boton Ver Personal
        self.btnVerPersonal = tk.Button(self.ventanaMenuA, text="Ver Personal", command=self.MostrarListadoPersonal)
        self.btnVerPersonal.pack(pady=10)
        
        #Boton Registrar Entrada
        self.btnRegistrarE = tk.Button(self.ventanaMenuA, text="Ver Entradas", command=self.MostrarListadoEntrada)
        self.btnRegistrarE.pack(pady=10)
        
        #Boton Registrar Salida
        self.btnRegistrarS = tk.Button(self.ventanaMenuA, text="Ver Salidas", command=self.MostrarListadoSalida)
        self.btnRegistrarS.pack(pady=10)

    def MostrarListadoPersonal(self):
        VentanaVerPersonal(self.ventanaMenuA,self.id)
        self.ventanaMenuA.withdraw()
    
    def MostrarListadoEntrada(self):
        VentanaVerEntrada(self.ventanaMenuA,self.id)
        self.ventanaMenuA.withdraw()
    
    def MostrarListadoSalida(self):
        VentanaVerSalida(self.ventanaMenuA,self.id)
        self.ventanaMenuA.withdraw()

class VentanaVerEntrada: #Ventana referente a boton 
    def __init__(self,VtnPadre,Id):
        self.controller = Controlador()
        self.VtnPadre = VtnPadre
        self.id = Id

        self.ventanaEntrada = tk.Toplevel(self.VtnPadre)
        self.ventanaEntrada.title("CheckList - Ver Entradas")
        self.ventanaEntrada.geometry("650x380")

        #Boton Atras
        self.btnAtras = tk.Button(self.ventanaEntrada, text="Atras", command=self.Atras)
        self.btnAtras.pack(side="top", anchor="w", padx=10, pady=20)
        
        #Label de Agregar Entrada
        tk.Label(self.ventanaEntrada, text="Agregar Entrada:").pack()
        
        #Boton Agregar Entrada
        self.btnAgregar = tk.Button(self.ventanaEntrada, text="Agregar Entrada", command=self.VentAgregarEntrada)
        self.btnAgregar.pack(pady=10)
        
        # #Boton Actualizar
        # self.btnActualizar = tk.Button(self.ventanaEntrada, text="Actualizar", command=self.ListarEntradas)
        # self.btnActualizar.pack(side="top", anchor="ne", padx=40, pady=20)
        
        # Área de Listado
        self.lblResultado = tk.Label(self.ventanaEntrada, text="", fg="Black")
        self.lblResultado.pack(side="left", fill="x")
        self.lblResultado.pack(pady=1)

        self.ListarEntradas()

    def ListarEntradas(self):
        resultados = self.controller.CListarEntradas()
        if resultados:
            texto = "\n ".join([f"N° Entrada: {fila[1]}   | ID Usuario: {fila[0]}   | Horario: {fila[2]}" for fila in resultados])
            self.lblResultado.config(text=texto)
        else:
            self.lblResultado.config(text="No hay registros")

    def VentAgregarEntrada(self): #Accion del boton Agregar Entrada
        respuesta = messagebox.askyesno("Agregar Entrada", "¿Es para otro Usuario?") 
        if respuesta:
            VentanaAgregarEntrada(self.ventanaEntrada,self.id)
        else:
            try:
                Horario = datetime.now()
                self.objEntrada = Entrada(Horario)
                ok = self.controller.CInsertarEntrada(self.objEntrada)
                if ok:
                    messagebox.showinfo("Agregado", "Se agrego correctamente.")
                else:
                    messagebox.showwarning("Problemas", "No se pudo agregar la entrada")
            except Error as e:
                messagebox.showerror("Error", "Ocurrio un error en el proceso")   

    def Atras(self): #Accion del boton Atras
        self.ventanaEntrada.destroy() # Cierro mi ventana Actual (Ver Entrada)
        self.VtnPadre.deiconify()   #Muestro la Ventana VerPersonal

class VentanaAgregarEntrada: #Ventana referente a boton 
    def __init__(self,VtnPadre,Id):
        self.controller = Controlador()
        self.id = Id
        self.VtnPadre = VtnPadre

        self.ventanaAgregarEntrada = tk.Toplevel(self.VtnPadre)
        self.ventanaAgregarEntrada.title("CheckList - Agregar Entrada")
        self.ventanaAgregarEntrada.geometry("650x380")

        #Boton Atras
        self.btnAtras = tk.Button(self.ventanaAgregarEntrada, text="Atras", command=self.Atras)
        self.btnAtras.pack(side="top", anchor="w", padx=10, pady=20)
        
        #Caja de texto para escribir el nombre
        tk.Label(self.ventanaAgregarEntrada, text="Nombre del Usuario:").pack()
        self.entryNombre = tk.Entry(self.ventanaAgregarEntrada, width=30)
        self.entryNombre.pack(pady=5)
        
        #Caja de texto para escribir el Apellido
        tk.Label(self.ventanaAgregarEntrada, text="Apellido del Usuario:").pack()
        self.entryApellido = tk.Entry(self.ventanaAgregarEntrada, width=30)
        self.entryApellido.pack(pady=5)
        
        #Label de Agregar Entrada
        tk.Label(self.ventanaAgregarEntrada, text="Agregar").pack()
        #Boton Agregar Entrada
        self.btnGuardar = tk.Button(self.ventanaAgregarEntrada, text="Guardar", command=self.BuscarNombre)
        self.btnGuardar.pack(pady=10)

    def GuardarEntrada(self): #Accion del boton Guardar
        try:
            Horario = datetime.now()
            self.objEntrada = Entrada(Horario)
            self.objEntrada.IdPersonal = self.id
            ok = self.controller.CInsertarEntrada(self.objEntrada)
            if ok:
                messagebox.showinfo("Agregado", "Se agrego correctamente.")
            else:
                messagebox.showwarning("Problemas", "No se pudo agregar la entrada")
        except Error as e:
            messagebox.showerror("Error", "Ocurrio un error en el proceso")  
        self.Atras()    

    def BuscarNombre(self):
        try:
            N = self.entryNombre.get()
            A = self.entryApellido.get()
            ok = self.controller.CBuscarUsuario(N,A)
            if ok:
                self.id = ok
                self.GuardarEntrada()
            else:
                messagebox.showwarning("Problemas", "No se pudo encontrar al usuario")
        except Error as e:
            messagebox.showerror("Error", "Ocurrio un error en el proceso")    

    def Atras(self): #Accion del boton Atras
        self.ventanaAgregarEntrada.destroy() # Cierro mi ventana Actual (Agregar Entradas)
        self.VtnPadre.deiconify() #Muestro la Ventana Ver Entrada
        
#======================================================#
class VentanaVerSalida: #Ventana referente a boton 
    def __init__(self,VtnPadre,Id):
        self.controller = Controlador()
        self.VtnPadre = VtnPadre
        self.id = Id

        self.ventanaSalida = tk.Toplevel(self.VtnPadre)
        self.ventanaSalida.title("CheckList - Ver Salida")
        self.ventanaSalida.geometry("650x380")

        #Boton Atras
        self.btnAtras = tk.Button(self.ventanaSalida, text="Atras", command=self.Atras)
        self.btnAtras.pack(side="top", anchor="w", padx=10, pady=20)
        
        #Label de Agregar Salida
        tk.Label(self.ventanaSalida, text="Agregar Salida:").pack()
        
        #Boton Agregar Salidas
        self.btnAgregar = tk.Button(self.ventanaSalida, text="Agregar Salida", command=self.VentAgregarSalida)
        self.btnAgregar.pack(pady=10)

        # #Boton Actualizar
        # self.btnActualizar = tk.Button(self.ventanaSalida, text="Actualizar", command=self.ListarSalida)
        # self.btnActualizar.pack(side="top", anchor="ne", padx=40, pady=20)
        
        # Área de Listado
        self.lblResultado = tk.Label(self.ventanaSalida, text="", fg="Black")
        self.lblResultado.pack(side="left", fill="x")
        self.lblResultado.pack(pady=1)

        self.ListarSalida()

    def ListarSalida(self):
        resultados = self.controller.CListarSalida()
        if resultados:
            texto = "\n ".join([f"N° Entrada: {fila[1]}   | ID Usuario: {fila[0]}   | Horario: {fila[2]}" for fila in resultados])
            self.lblResultado.config(text=texto)
        else:
            self.lblResultado.config(text="No hay registros")
        
        
    def VentAgregarSalida(self): #Accion del boton Agregar Salida
        respuesta = messagebox.askyesno("Salida", "¿Es para otro Usuario?") 
        if respuesta:
            VentanaAgregarSalida(self.ventanaSalida,self.id,self.ListarSalida)
            self.ventanaSalida.withdraw()
        else:
            try:
                Horario = datetime.now()
                self.objSalida = Salida(Horario)
                ok = self.controller.CInsertarSalida(self.objSalida)
                if ok:
                    messagebox.showinfo("Agregado", "Se agrego correctamente.")
                else:
                    messagebox.showwarning("Problemas", "No se pudo agregar la salida")
            except Error as e:
                messagebox.showerror("Error", "Ocurrio un error en el proceso")   
        
    def Atras(self): #Accion del boton Atras
        self.ventanaSalida.destroy() # Cierro mi ventana Actual (Ver Salida)
        self.VtnPadre.deiconify() #Muestro la Ventana Ver Principal

#======================================================#
class VentanaAgregarSalida: #Ventana referente a boton 
    def __init__(self,VtnPadre,Id,ListarS):
        self.controller = Controlador()
        self.VtnPadre = VtnPadre
        self.ListarS = ListarS
        self.id = Id

        self.ventanaAgregarSalida = tk.Toplevel(self.VtnPadre)
        self.ventanaAgregarSalida.title("CheckList - Agregar Salida")
        self.ventanaAgregarSalida.geometry("650x380")

        #Boton Atras
        self.btnAtras = tk.Button(self.ventanaAgregarSalida, text="Atras", command=self.Atras)
        self.btnAtras.pack(side="top", anchor="w", padx=10, pady=20)
        
        #Caja de texto para escribir el nombre
        tk.Label(self.ventanaAgregarSalida, text="Nombre del Usuario:").pack()
        self.entryNombre = tk.Entry(self.ventanaAgregarSalida, width=30)
        self.entryNombre.pack(pady=5)
        
        #Caja de texto para escribir el Apellido
        tk.Label(self.ventanaAgregarSalida, text="Apellido del Usuario:").pack()
        self.entryApellido = tk.Entry(self.ventanaAgregarSalida, width=30)
        self.entryApellido.pack(pady=5)
        
        #Label de Agregar Entrada
        tk.Label(self.ventanaAgregarSalida, text="Agregar").pack()
        #Boton Agregar Entrada
        self.btnGuardar = tk.Button(self.ventanaAgregarSalida, text="Guardar", command=self.BuscarNombre)
        self.btnGuardar.pack(pady=10)
        
    def GuardarSalida(self): #Accion del boton Guardar
        try:
            Horario = datetime.now()
            self.objSalida = Salida(Horario)
            self.objSalida.IdPersonal = self.id
            ok = self.controller.CInsertarSalida(self.objSalida)
            if ok:
                messagebox.showinfo("Agregado", "Se agrego correctamente.")
            else:
                messagebox.showwarning("Problemas", "No se pudo agregar la salida")
        except Error as e:
            messagebox.showerror("Error", "Ocurrio un error en el proceso")  
        self.ventanaAgregarSalida.destroy()
        # Muestro ventana Ver Salida
        self.VtnPadre.deiconify()

    def BuscarNombre(self):
        try:
            N = self.entryNombre.get()
            A = self.entryApellido.get()
            ok = self.controller.CBuscarUsuario(N,A)
            if ok:
                self.id = ok
                self.GuardarSalida()
            else:
                messagebox.showwarning("Problemas", "No se pudo encontrar al usuario")
        except Error as e:
            messagebox.showerror("Error", "Ocurrio un error en el proceso")    

    def Atras(self): #Accion del boton Atras
        self.ventanaAgregarSalida.destroy() # Cierro mi ventana Actual (Agregar salida)
        self.VtnPadre.deiconify()  #Muestro la Ventana Menu

#======================================================#
#==PERSONAL==
class VentanaVerPersonal: #Ventana referente a boton
    def __init__(self,VtnPadre,Id):
        self.controller = Controlador()
        self.VtnPadre = VtnPadre
        self.id = Id

        self.VentanaPersonal = tk.Toplevel(self.VtnPadre)
        self.VentanaPersonal.title("CheckList Ver Personal")
        self.VentanaPersonal.geometry("800x600")
        
        #Boton Atras
        self.btnAtras = tk.Button(self.VentanaPersonal, text="Atras", command=self.Atras)
        self.btnAtras.pack(side="top", anchor="w", padx=10, pady=20,)

        #Boton Agregar
        self.btn2 = tk.Button(self.VentanaPersonal, text="Agregar Personal", command=self.MostrarVentanaAgregar)
        self.btn2.pack(pady=10, side="top")

        # #Boton Actualizar
        # self.btnActualizar = tk.Button(self.VentanaPersonal, text="Actualizar", command=self.listar)
        # self.btnActualizar.pack(side="top", anchor="ne", padx=40, pady=20)

        # Área de Listado
        self.lblResultado = tk.Label(self.VentanaPersonal, text="", fg="Black")
        self.lblResultado.pack(side="left", fill="x")
        self.lblResultado.pack(pady=1)

        self.listar()

    def listar(self):
        resultados = self.controller.CListar()
        if resultados:
            texto = "\n ".join([f"Nombre: {fila[0]}   | Apellido: {fila[1]}   | DNI: {fila[2]}" for fila in resultados])
            self.lblResultado.config(text=texto)
        else:
            self.lblResultado.config(text="No hay registros")
    
    def MostrarVentanaAgregar(self):
        VentanaAgregarPersonal(self.VentanaPersonal,self.id,self.listar)
        self.VentanaPersonal.withdraw()
        
    def Atras(self): #Accion del boton Atras
        self.VentanaPersonal.destroy() # Cierro mi ventana Actual (VerPersonal)
        self.VtnPadre.deiconify()  #Muestro la Ventana Menu

#======================================================#
class VentanaAgregarPersonal: #Ventana referente a boton 
    def __init__(self,VtnPadre,Id,ListarP):
        self.controller = Controlador()
        self.VtnPadre = VtnPadre
        self.ListarP = ListarP
        self.id = Id

        self.ventanaAgregarPersonal = tk.Toplevel(self.VtnPadre)
        self.ventanaAgregarPersonal.title("CheckList - Agregar Personal")
        self.ventanaAgregarPersonal.geometry("650x380")

        #Boton Atras
        self.btnAtras = tk.Button(self.ventanaAgregarPersonal, text="Atras", command=self.Atras)
        self.btnAtras.pack(side="top", anchor="w", padx=10, pady=20)
        
        tk.Label(self.ventanaAgregarPersonal, text="Usuario:").pack(pady=5)
        self.userEntry = tk.Entry(self.ventanaAgregarPersonal, width=30)
        self.userEntry.pack()

        tk.Label(self.ventanaAgregarPersonal, text="Contraseña:").pack(pady=5)
        self.passEntry = tk.Entry(self.ventanaAgregarPersonal, width=30, show="*")
        self.passEntry.pack()
        
        #Caja de texto para escribir el nombre
        tk.Label(self.ventanaAgregarPersonal, text="Nombre:").pack()
        self.entryNombre = tk.Entry(self.ventanaAgregarPersonal, width=30)
        self.entryNombre.pack(pady=5)
        
        #Caja de texto para escribir el Apellido
        tk.Label(self.ventanaAgregarPersonal, text="Apellido:").pack()
        self.entryApellido = tk.Entry(self.ventanaAgregarPersonal, width=30)
        self.entryApellido.pack(pady=5)
        
        #Caja de texto para escribir el DNI
        tk.Label(self.ventanaAgregarPersonal, text="DNI:").pack()
        self.entryDni = tk.Entry(self.ventanaAgregarPersonal, width=30)
        self.entryDni.pack(pady=5)
        
        #Variables del boton check
        self.rolAdmin = tk.IntVar()
        self.rolUser = tk.IntVar()
        # Check Admin
        self.chkAdmin = tk.Checkbutton(
            self.ventanaAgregarPersonal,
            text="Admin",
            variable=self.rolAdmin,
            command=self.seleccionarAdmin
        )
        self.chkAdmin.pack(side="left", padx=10, pady=20)

        # Check User
        self.chkUser = tk.Checkbutton(
            self.ventanaAgregarPersonal,
            text="User",
            variable=self.rolUser,
            command=self.seleccionarUser
        )
        self.chkUser.pack(side="left", padx=10, pady=20)
        
        #Boton Guardar
        self.btnGuardar = tk.Button(self.ventanaAgregarPersonal, text="Guardar", command=self.Guardar)
        self.btnGuardar.pack(pady=10)

        # Área de mensaje
        self.lblAgregado = tk.Label(self.ventanaAgregarPersonal, text="", fg="blue")
        self.lblAgregado.pack(pady=20)

    def seleccionarAdmin(self):
        if self.rolAdmin.get() == 1:
            self.rolUser.set(0)

    def seleccionarUser(self):
        if self.rolUser.get() == 1:
            self.rolAdmin.set(0)
    
    def Guardar(self): #Accion del boton Guardar
        #Lo agrego a la base de datos en Usuarios
        Usuario = self.userEntry.get()
        Clave = self.passEntry.get()
        if self.rolAdmin.get() == 1:
            Rol = "admin"
        elif self.rolUser.get() == 1:
            Rol = "user"
        else:
            messagebox.showwarning("Problemas", "Seleccione un Rol. Porfavor")
        print(Usuario)
        print(Clave)
        self.controller.CInsertarUsuario(Usuario,Clave,Rol)
        
        #Inserto el Personal
        Dni = int(self.entryDni.get())
        N = self.entryNombre.get()
        A = self.entryApellido.get()
        ok = self.controller.CBuscarIDUsuario(Usuario,Clave)
        if isinstance(ok, int):
            IdUsuario = ok
            resultado = self.controller.CInsertarPersonal(N,A,Dni,IdUsuario)
            self.lblAgregado.config(text=resultado)
            messagebox.showinfo("Exito", "Agregado Correctamente")
        else:
            messagebox.showwarning("Error", "No se pudo agregar")
    def Atras(self): #Accion del boton Atras
        self.ventanaAgregarPersonal.destroy() # Cierro mi ventana Actual (Agregar)
        self.VtnPadre.deiconify()  #Muestro la Ventana Menu
from interfaces.pantallaPrincipal import MainScreen
from interfaces.pantallaRegistro import Registro
from models.systemdb import Pydb
from tkinter import *
from tkinter import ttk, messagebox

class MainApp(Tk):
    modoDefault = 'login'
    database = Pydb()
    
    def __init__(self):
        super().__init__()  
        self.title("Sistema Proyecto")
        self.geometry("800x450")
        self.config(bg="#ffffff")   
        self.frameone = Frame(self,bg="#cab4a0")
        self.iconHome = PhotoImage(file="assets/home.png")
        self.setup_ui()

    def setup_ui(self):
        self.frameone.place(x=0,y=0,width=350,height=450)
        Label(self.frameone, image=self.iconHome,bg="#cab4a0").pack(pady=80)
        Label(self.frameone, text="SMART HOME", font=("Helvetica", 24, 'bold'), bg="#cab4a0", fg="#000000").pack()
        Label(self, text="Bienvenido Nuevamente", font=("Helvetica", 24, 'bold'), bg="#ffffff", fg="#000000").place(y=40,x=390)
        Label(self, text="Introduce tus datos", font=("Helvetica", 12,'bold'), bg="#ffffff", fg="#000000").place(y=90,x=500)

        self.label_correo = Label(self, text="Correo Electrónico:", font=("Helvetica", 10,'bold'), bg="#ffffff", fg="#000000")
        self.entry_correo = Entry(self, width=35, font=("Helvetica", 10), highlightbackground="#000000",highlightthickness=1)

        self.label_contrasena = Label(self, text="Contraseña:", font=("Helvetica", 10, 'bold'), bg="#ffffff", fg="#000000")
        self.entry_contrasena = Entry(self, width=35, font=("Helvetica", 10), show="*", highlightbackground="#000000",highlightthickness=1)

        self.label_correo.place(y=170, x=440)
        self.entry_correo.place(y=202, x=450)
        self.label_contrasena.place(y=230, x=440)
        self.entry_contrasena.place(y=260, x=450)

        self.boton_login = Button(self, text='Iniciar Sesión', bg="#755f50", fg="#ffffff", font=('Helvetica', 12, 'bold'), command=self.auth_user)
        self.boton_registro = Button(self, text='Registrarse', bg="#755f50", fg="#ffffff", font=('Helvetica', 12, 'bold'), command=self.registro)
        
        self.boton_login.place(y=350, x=440)
        self.boton_registro.place(y=350, x=590)

    def auth_user(self):
        correo = self.entry_correo.get()
        contrasena = self.entry_contrasena.get()
        if correo == '' and contrasena == '':
            messagebox.showerror(title='Sistema Proyecto', message='No puedes dejar el campo correo electrónico y contraseña vacíos')
        elif contrasena == "":
            messagebox.showerror(title='Sistema Proyecto', message='No puedes dejar el campo contraseña vacío')
        elif correo == '':
            messagebox.showerror(title='Sistema Proyecto', message='No puedes dejar el campo correo electrónico vacío')
        else:
            vef = self.database.verificar_usuario(correo, contrasena)
            if vef:
                messagebox.showinfo(title='Sistema Proyecto', message='Has iniciado sesión correctamente')
                self.destroy()
                succes = MainScreen(vef)
                succes.mainloop()
            else:
                messagebox.showerror(title="Sistema Proyecto", message='Correo o contraseña incorrectos')

    def registro(self):
        registro = Registro()
        registro.focus()
        registro.grab_set()  

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()

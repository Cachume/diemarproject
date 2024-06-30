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
        self.geometry("500x500")
        self.config(bg="#f0f0f0")   

        self.setup_ui()

    def setup_ui(self):
        Label(self, text="Iniciar Sesión", font=("Helvetica", 24, 'bold'), bg="#f0f0f0", fg="#333").pack(anchor=CENTER, pady=20)
        Label(self, text="Introduce tus datos", font=("Helvetica", 12), bg="#f0f0f0", fg="#666").pack(anchor=CENTER, pady=5)

        self.label_correo = Label(self, text="Correo Electrónico:", font=("Helvetica", 10), bg="#f0f0f0", fg="#333")
        self.entry_correo = Entry(self, width=30, font=("Helvetica", 10))

        self.label_contrasena = Label(self, text="Contraseña:", font=("Helvetica", 10), bg="#f0f0f0", fg="#333")
        self.entry_contrasena = Entry(self, width=30, font=("Helvetica", 10), show="*")

        self.label_correo.place(y=200, x=60)
        self.entry_correo.place(y=202, x=230)
        self.label_contrasena.place(y=230, x=60)
        self.entry_contrasena.place(y=232, x=230)

        self.boton_login = Button(self, text='Iniciar Sesión', bg="#007acc", fg="#fff", font=('Helvetica', 12, 'bold'), command=self.auth_user)
        self.boton_registro = Button(self, text='Registrarse', bg="#f0f0f0", fg="#007acc", font=('Helvetica', 12, 'bold'), command=self.registro)
        
        self.boton_login.place(y=350, x=120)
        self.boton_registro.place(y=350, x=260)

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

from models.systemdb import Pydb
from tkinter import *
from tkinter import ttk, messagebox

class Registro(Toplevel):
    database = Pydb()
    
    def __init__(self):
        super().__init__()  
        self.title("Sistema Proyecto")
        self.geometry("500x550")
        self.config(bg="#f0f0f0")   

        self.setup_ui()

    def setup_ui(self):
        Label(self, text="Registrarme", font=("Helvetica", 24, 'bold'), bg="#f0f0f0", fg="#333").pack(anchor=CENTER, pady=20)
        Label(self, text="Introduce tus datos", font=("Helvetica", 12), bg="#f0f0f0", fg="#666").pack(anchor=CENTER, pady=5)

        self.label_nombre = Label(self, text="Nombre:", font=("Helvetica", 10), bg="#f0f0f0", fg="#333")
        self.entry_nombre = Entry(self, width=30, font=("Helvetica", 10))

        self.label_correo = Label(self, text="Correo Electrónico:", font=("Helvetica", 10), bg="#f0f0f0", fg="#333")
        self.entry_correo = Entry(self, width=30, font=("Helvetica", 10))

        self.label_contrasena = Label(self, text="Contraseña:", font=("Helvetica", 10), bg="#f0f0f0", fg="#333")
        self.entry_contrasena = Entry(self, width=30, font=("Helvetica", 10), show="*")

        self.label_confirmar_contrasena = Label(self, text="Confirmar Contraseña:", font=("Helvetica", 10), bg="#f0f0f0", fg="#333")
        self.entry_confirmar_contrasena = Entry(self, width=30, font=("Helvetica", 10), show="*")

        self.label_nombre.place(y=150, x=60)
        self.entry_nombre.place(y=152, x=230)
        self.label_correo.place(y=180, x=60)
        self.entry_correo.place(y=182, x=230)
        self.label_contrasena.place(y=210, x=60)
        self.entry_contrasena.place(y=212, x=230)
        self.label_confirmar_contrasena.place(y=240, x=60)
        self.entry_confirmar_contrasena.place(y=242, x=230)

        self.boton_registro = Button(self, text='Registrarme', bg="#007acc", fg="#fff", font=('Helvetica', 12, 'bold'), command=self.register_user)
        self.boton_registro.place(y=350, x=200)

    def register_user(self):
        nombre = self.entry_nombre.get()
        correo = self.entry_correo.get()
        contrasena = self.entry_contrasena.get()
        confirmar_contrasena = self.entry_confirmar_contrasena.get()

        if not nombre or not correo or not contrasena or not confirmar_contrasena:
            messagebox.showerror(title='Sistema Proyecto', message='Todos los campos son obligatorios')
        elif contrasena != confirmar_contrasena:
            messagebox.showerror(title='Sistema Proyecto', message='Las contraseñas no coinciden')
        else:
            if self.database.registrar_usuario(nombre, correo, contrasena):
                messagebox.showinfo(title='Sistema Proyecto', message='Te has registrado correctamente')
                self.destroy()
                # Aquí puedes abrir la pantalla principal después del registro si es necesario
            else:
                messagebox.showerror(title='Sistema Proyecto', message='El registro ha fallado, intenta nuevamente')

if __name__ == "__main__":
    app = Registro()
    app.mainloop()

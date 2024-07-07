from tkinter import *

class passadmin(Toplevel):
    
    def __init__(self,parent):
        super().__init__(parent)
        self.title("Ingrese Contraseña")
        self.geometry("300x100")

        label = Label(self, text="Ingresa tu contraseña:")
        label.pack(pady=5)

        self.password_entry = Entry(self, show="*")
        self.password_entry.pack(pady=5)

        self.submit_button = Button(self, text="Aceptar", command=self.save_password)
        self.submit_button.pack(pady=10)
        
        self.parent = parent

    def save_password(self):
        self.parent.adminpass = self.password_entry.get()
        self.destroy()
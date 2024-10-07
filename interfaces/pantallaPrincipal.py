from tkinter import *
from tkinter import Menu, messagebox
from interfaces.passadm import passadmin
from models.systemdb import Pydb

class MainScreen(Tk):


    def __init__(self, user_info):
        super().__init__()
        self.user_session = user_info
        self.title("Sistema Proyecto")
        self.geometry("600x400")
        self.config(bg="#e0e0e0")
        self.db=Pydb()
        self.create_menu()
        self.create_labels()
    
    def create_menu(self):
        main_menu = Menu(self)
        self.config(menu=main_menu)
        
        modules_menu = Menu(main_menu, tearoff=0)
        modules_menu.add_command(label="Leds", command=self.open_leds)
        modules_menu.add_command(label="Motor", command=self.open_motor)

        if self.user_session[3]:
            admin_menu = Menu(main_menu, tearoff=0)
            admin_menu.add_command(label="Administrar Leds", command=self.admin_leds)
            admin_menu.add_command(label="Administrar Motor", command=self.admin_motor)
            main_menu.add_cascade(label="Administración", menu=admin_menu)
            self.adminpass = ""
        
        main_menu.add_cascade(label="Módulos", menu=modules_menu)
        main_menu.add_command(label="Cerrar sesión", command=self.logout)
        main_menu.add_command(label="Salir", command=self.exit_program)
    
    def create_labels(self):
        Label(self, text="Bienvenido al sistema del proyecto", font=('Helvetica', 14, "bold"), bg="#e0e0e0").pack(pady=15)
        Label(self, text="Utiliza el menú superior para navegar", font=('Helvetica', 10), bg="#e0e0e0").pack(pady=5)
        Label(self, text="Has iniciado sesión como:", font=('Helvetica', 12), bg="#e0e0e0").pack(pady=10)
        Label(self, text=f"Correo: {self.user_session[0]}", font=('Helvetica', 10), bg="#e0e0e0").pack(pady=5)
        Label(self, text=f"Última conexión: {self.user_session[2]}", font=('Helvetica', 10), bg="#e0e0e0").pack(pady=5)
    
    def open_leds(self):
        print("hola")
    
    def open_motor(self):
        print("hola")
    
    def logout(self):
        self.destroy()
    
    def exit_program(self):
        self.destroy()
    
    def admin_leds(self):
        if self.adminpass != "":
            if self.db.verificaradmin(self.adminpass,self.user_session[0]):
                print("si")
            else:
                messagebox.showerror("Sistema Manejo","La contraseña es incorrecta")
                self.adminpass == ""
        else:
            passadminv = passadmin(self)
            passadminv.grab_set()
            passadminv.wait_window()
            self.admin_leds()
    
    def admin_motor(self):
        print("adminmotor")

if __name__ == "__main__":
    app = MainScreen([1, 'albertq703@gmail.com', '2024-06-29 12:22:46'])
    app.mainloop()

import sqlite3
from hashlib import sha256
from datetime import datetime

class Pydb:

    db_file = './sistema.db'
    conex = None

    def __init__(self):
        self.conex = sqlite3.connect(self.db_file)
        self.create_user_table()

    def create_user_table(self):
        try:
            cursor = self.conex.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    correo TEXT NOT NULL UNIQUE,
                    contrasena TEXT NOT NULL,
                    ultimo_inicio_sesion TEXT
                )
            ''')
            self.conex.commit()
        except sqlite3.Error as e:
            print(f"Error al crear la tabla: {e}")

    def hash_password(self, password):
        return sha256(password.encode()).hexdigest()

    def registrar_usuario(self, nombre, correo, contrasena):
        try:
            cursor = self.conex.cursor()
            hashed_password = self.hash_password(contrasena)
            cursor.execute('''
                INSERT INTO usuarios (nombre, correo, contrasena) 
                VALUES (?, ?, ?)
            ''', (nombre, correo, hashed_password))
            self.conex.commit()
            print("Usuario registrado con éxito")
            return True
        except sqlite3.IntegrityError:
            print("Error: El correo ya está registrado")
            return False
        except sqlite3.Error as e:
            print(f"Error registrando el usuario: {e}")
            return False

    def actualizar_ultimo_inicio_sesion(self, correo):
        try:
            cursor = self.conex.cursor()
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute('''
                UPDATE usuarios
                SET ultimo_inicio_sesion = ?
                WHERE correo = ?
            ''', (now, correo))
            self.conex.commit()
        except sqlite3.Error as e:
            print(f"Error al actualizar el último inicio de sesión: {e}")

    def verificar_usuario(self, correo, contrasena):
        try:
            cursor = self.conex.cursor()
            hashed_password = self.hash_password(contrasena)
            cursor.execute('''
                SELECT * FROM usuarios WHERE correo = ? AND contrasena = ?
            ''', (correo, hashed_password))
            user = cursor.fetchone()
            if user:
                print("Usuario verificado con éxito")
                self.actualizar_ultimo_inicio_sesion(correo)
                duser = [user[0], user[1], user[4]]
                return duser
            else:
                print("Error: Usuario o contraseña incorrectos")
                return False
        except sqlite3.Error as e:
            print(f"Error al verificar el usuario: {e}")
            return False

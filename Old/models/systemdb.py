import sqlite3
from hashlib import sha256
from datetime import datetime

class Pydb:

    db_file = './sistema.db'
    conex = None

    def __init__(self):
        self.conex = sqlite3.connect(self.db_file)
        self.create_user_table()
        self.create_sequence_table()
        self.crear_admin()

    def create_user_table(self):
        try:
            cursor = self.conex.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    correo TEXT NOT NULL UNIQUE,
                    contrasena TEXT NOT NULL,
                    ultimo_inicio_sesion TEXT,
                    es_admin BOOLEAN NOT NULL DEFAULT 0
                )
            ''')
            self.conex.commit()
        except sqlite3.Error as e:
            print(f"Error al crear la tabla: {e}")

    def create_sequence_table(self):
        try:
            cursor = self.conex.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS secuencias (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha TEXT NOT NULL,
                    modo TEXT NOT NULL,
                    leds TEXT NOT NULL
                )
            ''')
            self.conex.commit()
        except sqlite3.Error as e:
            print(f"Error al crear la tabla de secuencias: {e}")

    def hash_password(self, password):
        return sha256(password.encode()).hexdigest()

    def registrar_usuario(self, nombre, correo, contrasena, es_admin=False):
        try:
            cursor = self.conex.cursor()
            hashed_password = self.hash_password(contrasena)
            cursor.execute('''
                INSERT INTO usuarios (nombre, correo, contrasena, es_admin) 
                VALUES (?, ?, ?, ?)
            ''', (nombre, correo, hashed_password, es_admin))
            self.conex.commit()
            print("Usuario registrado con éxito")
            return True
        except sqlite3.IntegrityError:
            print("Error: El correo ya está registrado")
            return False
        except sqlite3.Error as e:
            print(f"Error registrando el usuario: {e}")
            return False

    def crear_admin(self):
        try:
            cursor = self.conex.cursor()
            cursor.execute('''
                SELECT COUNT(*) FROM usuarios WHERE es_admin = 1
            ''')
            if cursor.fetchone()[0] == 0:
                self.registrar_usuario('admin', 'admin@admin.com', 'admin123', True)
                print("Usuario administrador creado con éxito")
            else:
                print("Ya existe un usuario administrador")
        except sqlite3.Error as e:
            print(f"Error al crear el usuario administrador: {e}")

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
                duser = [user[2], user[1], user[4], user[5]]  # Añadimos es_admin al array duser
                return duser
            else:
                print("Error: Usuario o contraseña incorrectos")
                return False
        except sqlite3.Error as e:
            print(f"Error al verificar el usuario: {e}")
            return False

    def guardar_secuencia(self, modo, leds):
        try:
            cursor = self.conex.cursor()
            cursor.execute('''
                SELECT COUNT(*) FROM secuencias WHERE modo = ? AND leds = ?
            ''', (modo, leds))
            resultado = cursor.fetchone()

            if resultado[0] == 0:
                fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute('''
                    INSERT INTO secuencias (fecha, modo, leds) 
                    VALUES (?, ?, ?)
                ''', (fecha, modo, leds))
                self.conex.commit()
                print("Secuencia guardada con éxito")
                return True
            else:
                print("Secuencia ya existente, no se guardó")
                return False 

        except sqlite3.Error as e:
            print(f"Error al guardar la secuencia: {e}")

    def obtener_secuencias(self):
        try:
            cursor = self.conex.cursor()
            cursor.execute('''
                SELECT modo, leds FROM secuencias
            ''')
            secuencias = cursor.fetchall()
            return secuencias
        except sqlite3.Error as e:
            print(f"Error al obtener las secuencias: {e}")
            return []
    
    def verificaradmin(self, adminpass, correo):
        cursor = self.conex.cursor()
        hashed_password = self.hash_password(adminpass)
        cursor.execute('''
            SELECT * FROM usuarios WHERE correo = ? AND contrasena = ?
        ''', (correo, hashed_password))
        user = cursor.fetchone()
        if user:
            print("Contrasena correcta")
            return True
        else:
            print("Contrasena incorrecta")
            return False
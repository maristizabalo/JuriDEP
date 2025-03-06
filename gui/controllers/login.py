import pickle
import os
from PyQt6 import uic
from PyQt6.QtWidgets import QLineEdit
from utils.ldap import Ldap
from database.connection import DatabaseConnection
from gui.controllers.home import Home

SESSION_FILE = "session.pkl"  # Archivo donde se almacenará la sesión

class Login():
    def __init__(self):
        # Si hay una sesión guardada, abrir directamente el Home
        if self.is_session_active():
            self.home = Home()
            return
        
        self.login = uic.loadUi("gui/views/login.ui")
        self.initGUI()
        self.login.lblMesaggeLogin.setText("")
        self.login.show()

    def show_pwd(self, clicked):
        if clicked:
            self.login.txtPwd.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.login.txtPwd.setEchoMode(QLineEdit.EchoMode.Password)

    def get_into(self):
        username = self.login.txtUser.text()
        password = self.login.txtPwd.text()

        # Autenticar usuario usando LDAP
        ldap = Ldap()
        login_res, message, user_ldap = ldap.login_user(username, password)

        if login_res:
            self.login.lblMesaggeLogin.setText("Login exitoso")

            # Verificar si el usuario existe en la base de datos
            db = DatabaseConnection()
            conn = db.connect()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT ID_USUARIO FROM USUARIO WHERE USUARIO = ?", (username,))
                user = cursor.fetchone()

                if user is None:
                    # Insertar nuevo usuario si no existe
                    cursor.execute("""
                        INSERT INTO USUARIO (NOMBRE_COMPLETO, USUARIO, ACTIVO, ACTIVO_LDAP, CORREO, 
                                            USUARIO_CREO, IP_CREO, ROL_ID)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (user_ldap['nombre_completo'], username, 1, 1, user_ldap['correo'], 'SYSTEM', 'localhost', 4))
                    conn.commit()
                    self.login.lblMesaggeLogin.setText("Usuario creado exitosamente")
                
                db.close()

            # Guardar sesión del usuario
            self.save_session(username, user_ldap)

            # Cerrar la ventana de login y abrir Home
            self.login.close()
            self.home = Home()
        
        else:
            self.login.lblMesaggeLogin.setText(message)

    def save_session(self, username, user_data):
        """Guarda la sesión del usuario en un archivo local."""
        session_data = {
            "username": username,
            "user_data": user_data
        }
        with open(SESSION_FILE, "wb") as f:
            pickle.dump(session_data, f)

    def is_session_active(self):
        """Verifica si hay una sesión activa almacenada."""
        return os.path.exists(SESSION_FILE)

    def get_session_data(self):
        """Obtiene los datos de la sesión si existe."""
        if self.is_session_active():
            with open(SESSION_FILE, "rb") as f:
                return pickle.load(f)
        return None

    def logout(self):
        """Elimina la sesión guardada."""
        if self.is_session_active():
            os.remove(SESSION_FILE)

    def initGUI(self):
        self.login.btnLogin.clicked.connect(self.get_into)
        self.login.checkBoxPwd.clicked.connect(self.show_pwd)

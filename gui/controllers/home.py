import pickle
import os
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow

SESSION_FILE = "session.pkl"  # Archivo de sesión

class Home(QMainWindow):
    def __init__(self):
        super().__init__()
        self.home = uic.loadUi("gui/views/home.ui", self)

        # Cargar sesión del usuario
        session_data = self.get_session_data()
        if session_data:
            nombre_completo = session_data['user_data'].get('nombre_completo', 'Usuario')
            self.home.helloNameLabel.setText(f"Hola, {nombre_completo}!")  # Actualizar QLabel

        # Conectar el botón exitBtn con la función logout
        self.home.exitBtn.clicked.connect(self.logout)

        self.show()

    def get_session_data(self):
        """Obtiene los datos de la sesión si existe."""
        if os.path.exists(SESSION_FILE):
            with open(SESSION_FILE, "rb") as f:
                return pickle.load(f)
        return None

    def logout(self):
        """Elimina la sesión y vuelve a la pantalla de login."""
        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)  # Eliminar archivo de sesión
        
        self.close()  # Cerrar Home

        from gui.controllers.login import Login  # importacion de manera diferida
        self.login = Login()  # Abrir pantalla de login

from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox

class Login():
    def __init__(self):
        self.login = uic.loadUi("gui/login.ui")
        self.initGUI()
        self.login.lblMesaggeLogin.setText("")
        self.login.show()
    
    def get_into(self):
        if self.login.txtUser.text() == "admin" and self.login.txtPwd.text() == "admin":
            self.login.lblMesaggeLogin.setText("Bienvenido")
        else:
            self.login.lblMesaggeLogin.setText("Usuario o contraseña incorrectos")
            QMessageBox.warning(self.login, "Error", "Usuario o contraseña incorrectos")
    
    def initGUI(self):
        self.login.btnLogin.clicked.connect(self.get_into)
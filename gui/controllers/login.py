from PyQt6 import uic
from PyQt6.QtWidgets import QLineEdit
from utils.ldap import Ldap

class Login():
    def __init__(self):
        self.login = uic.loadUi("gui/views/login.ui")
        self.initGUI()
        self.login.lblMesaggeLogin.setText("")
        self.login.show()
    
    def show_pwd(self, clicked):
        
        if clicked:
            self.login.txtPwd.setEchoMode(
                QLineEdit.EchoMode.Normal
            )
        else:
            self.login.txtPwd.setEchoMode(
                QLineEdit.EchoMode.Password
            )
        
    
    def get_into(self):
        
        username = self.login.txtUser.text()
        password = self.login.txtPwd.text()
        
        # autenticar usuario usando ldap
        ldap = Ldap()
        login_res, message = ldap.login_user(username, password)
        
        if login_res:
            self.login.lblMesaggeLogin.setText(message)
        else:
            self.login.lblMesaggeLogin.setText(message)
    
    
    
    def initGUI(self):
        self.login.btnLogin.clicked.connect(self.get_into)
        self.login.checkBoxPwd.clicked.connect(self.show_pwd)
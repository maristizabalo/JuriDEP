from PyQt6 import uic
from PyQt6.QtWidgets import QLineEdit
from utils.ldap import Ldap
from database.connection import DatabaseConnection

class Login():
    def __init__(self):
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
                else:
                    self.login.lblMesaggeLogin.setText("Usuario autenticado correctamente")
                
                db.close()

                #
        else:
            self.login.lblMesaggeLogin.setText(message)
    
    def initGUI(self):
        self.login.btnLogin.clicked.connect(self.get_into)
        self.login.checkBoxPwd.clicked.connect(self.show_pwd)
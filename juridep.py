# from database.connection import DatabaseConnection
# db = DatabaseConnection()
# conn = db.connect()
# if conn:
#     print("Conexión establecida.")
# db.close()

from PyQt6.QtWidgets import QApplication
from gui.controllers.login import Login

class JuriDEP():
    def __init__(self):
        self.app = QApplication([])
        self.Login = Login()
        self.app.exec()

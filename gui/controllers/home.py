from PyQt6 import uic
from PyQt6.QtWidgets import QTableView, QMainWindow
from PyQt6.QtGui import QStandardItemModel, QStandardItem

class Home(QMainWindow):
    def __init__(self):
        super().__init__()
        self.home = uic.loadUi("gui/views/home.ui", self)
        self.populate_table()
        self.show()
    
    def populate_table(self):
        data = [
            ["715785", "PENAL", "2022-17968", "PENAL", "7/01/2022", "FISCALIA 136 INTERVENCIÓN TEMPRANA", "JOSE AGUSTÍN AVENDAÑO", "DADEP"],
            ["715786", "CIVIL", "2023-10234", "CIVIL", "15/03/2023", "JUZGADO 12 CIVIL", "MARÍA GÓMEZ", "EMPRESA XYZ"],
            ["715787", "LABORAL", "2021-56789", "LABORAL", "22/11/2021", "JUZGADO 5 LABORAL", "CARLOS PÉREZ", "JUAN PÉREZ"]
        ]
        
        headers = ["ID", "JURISDICCIÓN", "PROCESO", "TIPO DE PROCESO", "FECHA DE PRESENTACION DE DEMANDA", "DESPACHO QUE ACTUALMENTE CONOCE EL PROCESO", "ABOGADO A CARGO", "DEMANDANTE / DENUNCIANTE"]
        
        model = QStandardItemModel(len(data), len(headers))
        model.setHorizontalHeaderLabels(headers)
        
        for row_idx, row_data in enumerate(data):
            for col_idx, cell_data in enumerate(row_data):
                model.setItem(row_idx, col_idx, QStandardItem(cell_data))
        
        self.home.processTable.setModel(model)

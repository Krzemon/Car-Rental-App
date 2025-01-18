from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QStatusBar, QTabWidget, QGridLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QFont, QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize, QTimer

from database.db_connector import get_connection
from gui.base_window import BaseWindow
from database.models import Car
import psycopg2
from gui.customer.car_widget import CarWidget

class RentalWidget(QWidget):
    def __init__(self, customer_id, rental):
        super().__init__()

        self.customer_id = customer_id
        self.rental = rental
        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Przykładowe dane wynajmu
        # Zakładamy, że rental to obiekt z atrybutami: start_date, end_date, car_make, car_model, status
        start_date_label = QLabel(f"Data rozpoczęcia: {self.rental.start_date}")
        layout.addWidget(start_date_label)

        end_date_label = QLabel(f"Data zakończenia: {self.rental.end_date}")
        layout.addWidget(end_date_label)
        
        car_label = QLabel(f"Marka i model pojazdu: {self.rental.car_make} {self.rental.car_model}")
        layout.addWidget(car_label)
        
        status_label = QLabel(f"Status wynajmu: {self.rental.status}")
        layout.addWidget(status_label)

        self.setLayout(layout)

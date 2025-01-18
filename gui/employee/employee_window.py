from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QSlider, QStatusBar, QTabWidget, QPushButton, QSpinBox, QTableWidget, QCheckBox, QTableWidgetItem, QComboBox, QMessageBox, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QFont, QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize, QTimer
from gui.base_window import BaseWindow, font

from gui.employee.car_view import CarView
from gui.employee.rental_view import RentalView
from gui.employee.payment_view import PaymentView

class EmployeeWindow(BaseWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user

        self.title_label.setText("Panel Pracownika")
        self.tabs = QTabWidget(self)

        self.car_view = CarView()
        self.rental_view = RentalView()
        self.payment_view = PaymentView()   

        self.cars_widget = self.car_view.create()
        self.rental_widget = self.rental_view.create()
        self.payment_widget = self.payment_view.create()

        self.tabs.addTab(self.cars_widget, "Samochody")
        self.tabs.addTab(self.rental_widget, "Wypożyczenia")
        self.tabs.addTab(self.payment_widget, "Płatności")

        # Dodanie zakładek do layoutu klasy bazowej
        self.layout.addWidget(self.tabs)  # Używamy layoutu z klasy BaseWindow
        self.setLayout(self.layout)  # Zachowujemy layout z klasy BaseWindow
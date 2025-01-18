from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QSlider, QStatusBar, QTabWidget, QPushButton, QSpinBox, QTableWidget, QCheckBox, QTableWidgetItem, QComboBox, QMessageBox, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QFont, QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize, QTimer
from gui.base_window import BaseWindow, font

from gui.admin.rental_view import RentalView
from gui.admin.user_view import UserView
from gui.admin.customer_view import CustomerView
from gui.admin.employee_view import EmployeeView
from gui.admin.car_view import CarView
from gui.admin.report_view import ReportView

class AdminWindow(BaseWindow):
    def __init__(self):
        super().__init__()

        self.title_label.setText("Panel Administratora")
        self.tabs = QTabWidget(self)

        self.rental_view = RentalView()
        self.user_view = UserView()
        self.customer_view = CustomerView()
        self.employee_view = EmployeeView()
        self.car_view = CarView()        
        self.report_view = ReportView()        

        self.dashboard_widget = self.create_dashboard_view()
        self.rentals_widget = self.rental_view.create()
        self.users_widget = self.user_view.create()
        self.customers_widget = self.customer_view.create()
        self.employees_widget = self.employee_view.create()
        self.cars_widget = self.car_view.create()
        self.reports_widget = self.report_view.create()

        self.tabs.addTab(self.dashboard_widget, "Panel")
        self.tabs.addTab(self.rentals_widget, "Wypożyczenia")
        self.tabs.addTab(self.users_widget, "Użytkownicy")
        self.tabs.addTab(self.customers_widget, "Klienci")
        self.tabs.addTab(self.employees_widget, "Pracownicy")
        self.tabs.addTab(self.cars_widget, "Samochody")
        self.tabs.addTab(self.reports_widget, "Raporty")

        # Dodanie zakładek do layoutu klasy bazowej
        self.layout.addWidget(self.tabs)  # Używamy layoutu z klasy BaseWindow
        self.setLayout(self.layout)  # Zachowujemy layout z klasy BaseWindow


    def create_dashboard_view(self):
        widget = QWidget()
        layout = QVBoxLayout()
        # hello = QLabel("Witamy w Panelu administracyjnym")
        # hello.setFont(font)
        # layout.addWidget(hello)

        # description
        a = QLabel("W tym tygodniu dołączyło x nopwych użytkowników", alignment=Qt.AlignmentFlag.AlignTop)
        b = QLabel("Liczba aktywnych wypożyczeń", alignment=Qt.AlignmentFlag.AlignTop)
        c = QLabel("Liczba dostępnych produktów", alignment=Qt.AlignmentFlag.AlignTop)
        d = QLabel("Naruszenie regulaminu: x", alignment=Qt.AlignmentFlag.AlignTop)

        layout.addWidget(a)
        layout.addWidget(b)
        layout.addWidget(c)
        layout.addWidget(d)

        widget.setLayout(layout)
        return widget


# dashboad pracownika 

# Opóźnienia w zwrocie – lista klientów, którzy nie zwrócili produktu w terminie.
# Problemy techniczne – produkty wymagające uwagi, np. uszkodzenia zgłoszone przez klientów.
# Nadchodzące rezerwacje – lista najbliższych wypożyczeń.
from PyQt6.QtWidgets import QTabWidget
from gui.base_window import BaseWindow

from gui.admin.rental_view import RentalView
from gui.admin.user_view import UserView
from gui.admin.customer_view import CustomerView
from gui.admin.employee_view import EmployeeView
from gui.admin.car_view import CarView
from gui.admin.report_view import ReportView

class AdminWindow(BaseWindow):
    """ Klasa reprezentująca okno panelu administratora """
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

        self.reports_widget = self.report_view.create()
        self.rentals_widget = self.rental_view.create()
        self.users_widget = self.user_view.create()
        self.customers_widget = self.customer_view.create()
        self.employees_widget = self.employee_view.create()
        self.cars_widget = self.car_view.create()

        self.tabs.addTab(self.reports_widget, "Raporty")
        self.tabs.addTab(self.rentals_widget, "Wypożyczenia")
        self.tabs.addTab(self.users_widget, "Użytkownicy")
        self.tabs.addTab(self.customers_widget, "Klienci")
        self.tabs.addTab(self.employees_widget, "Pracownicy")
        self.tabs.addTab(self.cars_widget, "Samochody")

        # Dodanie zakładek do layoutu klasy bazowej
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
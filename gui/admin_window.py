from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QStatusBar, QTabWidget, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QFont, QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize, QTimer

from database.db_connector import close_connection, get_connection
from gui.base_window import BaseWindow
from database.models import User, Customer, Employee, Car

class AdminWindow(BaseWindow):
    def __init__(self):
        super().__init__()

        # Zmiana tytułu na "Panel Administratora"
        self.title_label.setText("Panel Administratora")

        # Dodanie zakładek specyficznych dla administratora
        self.tabs = QTabWidget(self)

        self.dashboard_widget = self.create_dashboard_view()
        self.reservations_widget = self.create_reservations_view()
        self.users_widget = self.create_users_view()
        self.customers_widget = self.create_customers_view()
        self.employees_widget = self.create_employees_view()
        self.cars_widget = self.create_cars_view()
        self.reports_widget = self.create_reports_view()

        self.tabs.addTab(self.dashboard_widget, "Panel")
        self.tabs.addTab(self.reservations_widget, "Rezerwacje")
        self.tabs.addTab(self.users_widget, "Użytkownicy")
        self.tabs.addTab(self.customers_widget, "Klienci")
        self.tabs.addTab(self.employees_widget, "Pracownicy")
        self.tabs.addTab(self.cars_widget, "Samochody")
        self.tabs.addTab(self.reports_widget, "Raporty")

        # Dodanie zakładek do layoutu klasy bazowej
        self.layout.addWidget(self.tabs)  # Używamy layoutu z klasy BaseWindow
        self.setLayout(self.layout)  # Zachowujemy layout z klasy BaseWindow


    # Funkcje tworzące widoki dla poszczególnych zakładek

    def create_dashboard_view(self):
        """Tworzy widok Panelu dla administratora."""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Witamy w Panelu administracyjnym"))
        layout.addWidget(QLabel("Tutaj możesz zarządzać systemem"))
        widget.setLayout(layout)
        return widget

    def create_reservations_view(self):
        """Tworzy widok Rezerwacji dla administratora."""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Witamy w widoku rezerwacji"))
        widget.setLayout(layout)
        return widget
    
    def create_users_view(self):
        """Tworzy widok uzytkownikow dla administratora."""
        widget = QWidget()
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setRowCount(0)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['ID uzytkownika', 'Imię', 'Nazwisko', 'Adres', 'Numer telefonu', 'E-mail'])

        self.load_users_to_table()

        layout.addWidget(self.table)
        widget.setLayout(layout)
        return widget

    def create_customers_view(self):
        """Tworzy widok Klientów dla administratora."""
        widget = QWidget()
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setRowCount(0)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['ID klienta', 'Imię', 'Nazwisko', 'Adres', 'Numer telefonu', 'E-mail'])

        self.load_customers_to_table()
        
        layout.addWidget(self.table)
        widget.setLayout(layout)
        return widget


    def create_employees_view(self):
        """Tworzy widok Pracowników dla administratora."""
        widget = QWidget()
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setRowCount(0)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['ID pracownika', 'Imię', 'Nazwisko', 'Adres', 'Numer telefonu', 'E-mail'])

        self.load_employees_to_table()

        layout.addWidget(self.table)
        widget.setLayout(layout)
        return widget
    
    def create_cars_view(self):
        """Tworzy widok Pojazdów dla administratora."""
        widget = QWidget()
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setRowCount(0)
        self.table.setColumnCount(12)
        self.table.setHorizontalHeaderLabels(['ID samochodu', 'Marka', 'Model', 'Rok', 'Nr rejestracyjny', 'Dzienna stawka', 'VIN', 'Status', 'Rodzaj paliwa', 'Status ubezpieczenia', 'Liczba miejsc', 'Kolor'])
        
        self.load_cars_to_table()

        layout.addWidget(self.table)
        widget.setLayout(layout)
        return widget

    def create_reports_view(self):
        """Tworzy widok Raportów dla administratora."""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Tutaj możesz przeglądać raporty"))
        widget.setLayout(layout)
        return widget

    # Funkcje pomocnicze do ładowania danych do tabeli

    def load_users_to_table(self):
        """Ładuje użytkowników do tabeli."""
        try:
            connection = get_connection()
            users = User.get_all(connection)
            self.table.setRowCount(len(users))

            for row_index, user in enumerate(users):
                self.table.setItem(row_index, 0, QTableWidgetItem(str(user.user_id)))
                self.table.setItem(row_index, 1, QTableWidgetItem(str(user.email)))
                self.table.setItem(row_index, 2, QTableWidgetItem(str(user.role)))
        except Exception as e:
            print(f"Error loading users into table: {e}")

    def load_customers_to_table(self):
        """Ładuje klientow do tabeli."""
        try:
            connection = get_connection()
            customers = Customer.get_all(connection)
            self.table.setRowCount(len(customers))

            for row_index, customer in enumerate(customers):
                self.table.setItem(row_index, 0, QTableWidgetItem(str(customer.customer_id)))
                self.table.setItem(row_index, 1, QTableWidgetItem(str(customer.first_name)))
                self.table.setItem(row_index, 2, QTableWidgetItem(str(customer.last_name)))
                self.table.setItem(row_index, 3, QTableWidgetItem(str(customer.address)))
                self.table.setItem(row_index, 4, QTableWidgetItem(str(customer.phone_number)))
                self.table.setItem(row_index, 5, QTableWidgetItem(str(customer.email)))
        except Exception as e:
            print(f"Error loading customers into table: {e}")


    def load_employees_to_table(self):
        """Ładuje pracownikow do tabeli."""
        try:
            connection = get_connection()
            employees = Employee.get_all(connection)
            self.table.setRowCount(len(employees))

            for row_index, employee in enumerate(employees):
                self.table.setItem(row_index, 0, QTableWidgetItem(str(employee.employee_id)))
                self.table.setItem(row_index, 1, QTableWidgetItem(str(employee.first_name)))
                self.table.setItem(row_index, 2, QTableWidgetItem(str(employee.last_name)))
                self.table.setItem(row_index, 3, QTableWidgetItem(str(employee.address)))
                self.table.setItem(row_index, 4, QTableWidgetItem(str(employee.phone_number)))
                self.table.setItem(row_index, 5, QTableWidgetItem(str(employee.email)))
        except Exception as e:
            print(f"Error loading employees into table: {e}")

    def load_cars_to_table(self):
        """Ładuje samochody do tabeli."""
        try:
            connection = get_connection()
            cars = Car.get_all(connection)
            self.table.setRowCount(len(cars))

            for row_index, car in enumerate(cars):
                self.table.setItem(row_index, 0, QTableWidgetItem(str(car.car_id)))
                self.table.setItem(row_index, 1, QTableWidgetItem(str(car.make)))
                self.table.setItem(row_index, 2, QTableWidgetItem(str(car.model)))
                self.table.setItem(row_index, 3, QTableWidgetItem(str(car.year)))
                self.table.setItem(row_index, 4, QTableWidgetItem(str(car.license_plate)))
                self.table.setItem(row_index, 5, QTableWidgetItem(str(car.daily_rate)))
                self.table.setItem(row_index, 6, QTableWidgetItem(str(car.vin)))
                self.table.setItem(row_index, 7, QTableWidgetItem(str(car.status)))
                self.table.setItem(row_index, 8, QTableWidgetItem(str(car.fuel_type)))
                self.table.setItem(row_index, 9, QTableWidgetItem(str(car.insurance_status)))
                self.table.setItem(row_index, 10, QTableWidgetItem(str(car.seat_count)))
                self.table.setItem(row_index, 11, QTableWidgetItem(str(car.color)))
        except Exception as e:
            print(f"Error loading cars into table: {e}")

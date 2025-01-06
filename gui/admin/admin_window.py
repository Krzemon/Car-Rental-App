from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QStatusBar, QTabWidget, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
from database.db_connector import close_connection, get_connection
from database.models import User, Customer, Employee, Car
from PyQt6.QtGui import QFont
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QTimer


class AdminWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Panel administratora")
        self.setGeometry(100, 100, 800, 600)

        self.setStyleSheet("background-color: #2f2f2f; color: white;")

        self.layout = QVBoxLayout(self)
        self.tool_layout = QHBoxLayout()

        title_font = QFont("Lora", 12, QFont.Weight.Bold)
        self.title_label = QLabel("Panel administratora")
        self.title_label.setFont(title_font)

        self.tool_layout.addWidget(self.title_label)
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.tool_layout.addItem(spacer)

        self.status_icon = QLabel(self)
        self.tool_layout.addWidget(self.status_icon, alignment=Qt.AlignmentFlag.AlignRight)
        self.green_circle = QPixmap("resources/images/green_circle.png")
        self.red_circle = QPixmap("resources/images/red_circle.png")
        self.green_circle = self.green_circle.scaled(15, 15)
        self.red_circle = self.red_circle.scaled(15, 15)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_connection)
        self.timer.start(5000)  # co 5 sekund
        self.status_icon.setPixmap(self.green_circle)
        self.status_icon.setFixedSize(30, 30)

        self.dark_light_mode_button = QPushButton()
        self.dark_light_mode_button.setIcon(QIcon("resources/images/mode.png"))
        self.dark_light_mode_button.setIconSize(QSize(32, 32))
        self.dark_light_mode_button.setToolTip("Włącz tryb jasny")
        self.dark_light_mode_button.setFixedSize(40, 40)
        self.dark_light_mode_button.clicked.connect(self.toggle_dark_light_mode)
        self.tool_layout.addWidget(self.dark_light_mode_button, alignment=Qt.AlignmentFlag.AlignRight)
        self.tool_layout.setAlignment(self.dark_light_mode_button, Qt.AlignmentFlag.AlignRight)
        self.is_dark_mode = True

        self.logout_button = QPushButton("Wyloguj", self)
        self.logout_button.clicked.connect(self.logout)
        self.tool_layout.addWidget(self.logout_button, alignment=Qt.AlignmentFlag.AlignRight)
        self.tool_layout.setAlignment(self.logout_button, Qt.AlignmentFlag.AlignRight)

        self.layout.addLayout(self.tool_layout)
        self.status_bar = QStatusBar(self)
        self.layout.addWidget(self.status_bar)

        # Dodanie zakładek

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

        #   #   #
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def open_login_window(self):
        """Otwórz okno logowania."""
        from gui.login_window import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()

    def check_connection(self):
        """Symulacja sprawdzania połączenia z bazą danych."""
        connected = get_connection()
        if connected:
            self.status_icon.setPixmap(self.green_circle)
            self.status_icon.setToolTip("Połączenie aktywne")
        else:
            self.status_icon.setPixmap(self.red_circle)
            self.status_icon.setToolTip("Brak połączenia")

    def toggle_dark_light_mode(self):
        if self.is_dark_mode:
            self.setStyleSheet("background-color: white; color: black;")
            self.dark_light_mode_button.setToolTip("Włącz tryb ciemny")
            self.status_bar.showMessage("Włączono tryb jasny", 2000)
        else:
            self.setStyleSheet("background-color: #2f2f2f; color: white;")
            self.dark_light_mode_button.setToolTip("Włącz tryb jasny")
            self.status_bar.showMessage("Włączono tryb ciemny", 2000)
        self.is_dark_mode = not self.is_dark_mode

    def logout(self):
        """Funkcja logowania - użytkownik jest wylogowywany."""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Wylogowywanie")
        msg_box.setText("Czy na pewno chcesz się wylogować?")

        yes_button = msg_box.addButton("Tak", QMessageBox.ButtonRole.YesRole)
        no_button = msg_box.addButton("Nie", QMessageBox.ButtonRole.NoRole)

        msg_box.exec()

        clicked_button = msg_box.clickedButton()

        if clicked_button == yes_button:
            close_connection()
            self.close()
            self.open_login_window()

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

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTabWidget, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt6.QtCore import Qt
from database.db_connector import close_connection, get_connection
from database.models import User

class AdminWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Dashboard")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout(self)

        self.logout_button = QPushButton("Wyloguj", self)
        self.logout_button.clicked.connect(self.logout)
        self.layout.addWidget(self.logout_button)
        self.layout.setAlignment(self.logout_button, Qt.AlignmentFlag.AlignRight)

        # Dodanie przycisku do sprawdzania połączenia
        self.connection_check_button = QPushButton("Sprawdź połączenie z bazą danych", self)
        self.connection_check_button.clicked.connect(self.check_database_connection)
        self.layout.addWidget(self.connection_check_button)
        self.layout.setAlignment(self.connection_check_button, Qt.AlignmentFlag.AlignLeft)

        self.tabs = QTabWidget(self)

        self.dashboard_widget = self.create_dashboard_view()
        self.reservations_widget = self.create_reservations_view()
        self.customers_widget = self.create_customers_view()
        self.vehicles_widget = self.create_vehicles_view()
        self.reports_widget = self.create_reports_view()

        self.tabs.addTab(self.dashboard_widget, "Dashboard")
        self.tabs.addTab(self.reservations_widget, "Reservations")
        self.tabs.addTab(self.customers_widget, "Customers")
        self.tabs.addTab(self.vehicles_widget, "Vehicles")
        self.tabs.addTab(self.reports_widget, "Reports")

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def open_login_window(self):
        """Otwórz okno logowania."""
        from gui.login_window import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()

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
            close_connection()  # Tylko w tym miejscu zamykamy połączenie
            self.close()
            self.open_login_window()

    def check_database_connection(self):
        """Sprawdza, czy połączenie z bazą danych jest aktywne."""
        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT 1")  # Proste zapytanie testowe
            QMessageBox.information(self, "Połączenie aktywne", "Połączenie z bazą danych jest aktywne.")
        except Exception as e:
            QMessageBox.warning(self, "Błąd połączenia", f"Brak aktywnego połączenia: {str(e)}")

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

    def create_customers_view(self):
        """Tworzy widok Klientów dla administratora."""
        widget = QWidget()
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setRowCount(0)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['ID użytkownika', 'Email', 'Rola'])
        self.load_users_to_table()

        layout.addWidget(self.table)
        widget.setLayout(layout)
        return widget

    def load_users_to_table(self):
        """Załaduj użytkowników do tabeli."""
        connection = get_connection()
        users = User.get_all(connection)  # Pobierz użytkowników z bazy danych
        
        self.table.setRowCount(len(users))

        for row, user in enumerate(users):
            self.table.setItem(row, 0, QTableWidgetItem(str(user.user_id)))
            self.table.setItem(row, 1, QTableWidgetItem(user.email))
            self.table.setItem(row, 2, QTableWidgetItem(user.role))

    def create_vehicles_view(self):
        """Tworzy widok Pojazdów dla administratora."""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Tutaj możesz zarządzać pojazdami"))
        widget.setLayout(layout)
        return widget

    def create_reports_view(self):
        """Tworzy widok Raportów dla administratora."""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Tutaj możesz przeglądać raporty"))
        widget.setLayout(layout)
        return widget

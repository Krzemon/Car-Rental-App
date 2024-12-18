from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTabWidget, QHBoxLayout, QPushButton, QFormLayout, QTableWidgetItem, QTableWidget, QLineEdit, QMessageBox
from PyQt6.QtCore import Qt
from database.db_connector import close_connection

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

        self.tabs = QTabWidget(self)

        self.dashboard_widget = self.create_dashboard_view()
        self.reservations_widget = self.create_reservations_view()
        self.customers_widget = self.create_customers_view()
        self.vehicles_widget = self.create_vehicles_view()
        self.reports_widget = self.create_reports_view()

        # Dodajemy zakładki i przypisujemy widoki
        self.tabs.addTab(self.dashboard_widget, "Dashboard")
        self.tabs.addTab(self.reservations_widget, "Reservations")
        self.tabs.addTab(self.customers_widget, "Customers")
        self.tabs.addTab(self.vehicles_widget, "Vehicles")
        self.tabs.addTab(self.reports_widget, "Reports")

        # Dodajemy zakładki do głównego układu
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def open_login_window(self):
        """Otwórz okno logowania."""
        from gui.login_window import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()

    def logout(self):
        """Funkcja logowania - użytkownik jest wylogowywany."""
        msg_box = QMessageBox.question(self, "Wylogowywanie", "Czy na pewno chcesz się wylogować?",
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)


        if msg_box == QMessageBox.StandardButton.Yes:
            close_connection()
            self.close()
            self.open_login_window()

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

        # Dodajemy tabelę do layoutu
        layout.addWidget(QLabel("Witamy w widoku rezerwacji"))
        widget.setLayout(layout)
        return widget

    def create_customers_view(self):
        """Tworzy widok klientów dla administratora."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        self.QLineEdit = QLineEdit()
        self.QLineEdit.setPlaceholderText("Szukaj użytkownika")
        layout.addWidget(self.QLineEdit)

        self.table = QTableWidget()
        self.table.setRowCount(5)
        self.table.setColumnCount(3) 
        self.table.setHorizontalHeaderLabels(["ID", "Imię", "Email"])

        # Wypełniamy tabelę przykładowymi danymi
        self.table.setItem(0, 0, QTableWidgetItem("1"))
        self.table.setItem(0, 1, QTableWidgetItem("John Doe"))
        self.table.setItem(0, 2, QTableWidgetItem("johndoe@example.com"))

        # Dodajemy tabelę do layoutu
        layout.addWidget(self.table)
        widget.setLayout(layout)
        return widget

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
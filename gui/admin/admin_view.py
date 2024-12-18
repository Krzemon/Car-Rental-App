# gui/admin/admin_view.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QTabWidget, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPushButton


class AdminView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Dashboard")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout(self)

        self.logout_button = QPushButton("Wyloguj", self)
        self.layout.addWidget(self.logout_button)
        self.layout.setAlignment(self.logout_button, Qt.AlignmentFlag.AlignRight)

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
        
        layout.addWidget(self.table)
        widget.setLayout(layout)
        return widget

    def load_users_to_table(self, users):
        """Załaduj użytkowników do tabeli."""
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

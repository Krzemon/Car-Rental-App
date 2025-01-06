from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from database.db_connector import initialize_connection, authenticate_user, get_connection
from PyQt6.QtGui import QFont
from gui.register_window import RegisterWindow
import psycopg2

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.app_title = "Car Rental System"
        self.setWindowTitle("Logowanie")
        self.setGeometry(100, 100, 300, 150)
        
        initialize_connection() # Inicjalizowanie połączenia z bazą danych przy starcie
        self.layout = QVBoxLayout()

        title_font = QFont("Lora", 12, QFont.Weight.Bold)
        self.title_label = QLabel("Aplikacja wypożyczalni samochodów")
        self.title_label.setFont(title_font)

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("E-mail")
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Hasło")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_button = QPushButton("Zaloguj", self)
        self.login_button.clicked.connect(self.login)
        self.register_button = QPushButton("Zarejestruj", self)
        self.register_button.clicked.connect(self.open_register_window)

        self.layout.addWidget(self.title_label)
        self.layout.addWidget(QLabel("Wpisz dane logowania:"))
        self.layout.addWidget(self.email_input)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.login_button)
        self.layout.addWidget(self.register_button)
        self.setLayout(self.layout)

    def login(self):
        email = self.email_input.text()
        password = self.password_input.text()
        if not email or not password:
            QMessageBox.warning(self, "Input Error", "Proszę wprowadzić e-mail i hasło.")
            return
        user = authenticate_user(email, password) # Weryfikacja danych logowania
        if user:
            self.open_role_window(user['role'])
        else:
            QMessageBox.warning(self, "Login Failed", "Logowanie nie powiodło się. Spróbuj ponownie.")

    def open_register_window(self):
        """Otwórz okno rejestracji."""
        self.register_window = RegisterWindow()
        self.register_window.show()
        self.close()

    def open_role_window(self, role):
        """W zależności od roli użytkownika otwórz odpowiednie okno."""
        if role == "customer":
            self.open_customer_window()
        elif role == "employee":
            self.open_worker_window()
        elif role == "admin":
            self.open_admin_window()

    def open_customer_window(self):
        from gui.customer.customer_window import CustomerWindow
        self.customer_window = CustomerWindow()
        self.customer_window.show()
        self.hide()

    def open_worker_window(self):
        from gui.employee.worker_window import WorkerWindow
        self.worker_window = WorkerWindow()
        self.worker_window.show()
        self.hide()

    def open_admin_window(self):
        from gui.admin.admin_window import AdminWindow
        self.admin_window = AdminWindow()
        self.admin_window.show()
        self.hide()

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from database.db_connector import initialize_connection, close_connection, authenticate_user

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 300, 250)

        # Inicjalizowanie połączenia z bazą danych przy starcie aplikacji
        initialize_connection()

        self.layout = QVBoxLayout()

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Email")

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.login)

        self.layout.addWidget(QLabel("Enter your credentials"))
        self.layout.addWidget(self.email_input)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.login_button)

        self.setLayout(self.layout)

    def closeEvent(self, event):
        """Zamyka połączenie z bazą danych, gdy aplikacja jest zamykana."""
        close_connection()
        event.accept()

    def login(self):
        email = self.email_input.text()
        password = self.password_input.text()

        if not email or not password:
            QMessageBox.warning(self, "Input Error", "Please fill in both fields.")
            return

        # Weryfikacja danych logowania
        user = authenticate_user(email, password)

        if user:
            # QMessageBox.information(self, "Success", f"Welcome, {user['role']}!")
            self.open_role_window(user['role'])
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid email or password.")

    def open_role_window(self, role):
        """W zależności od roli użytkownika otwórz odpowiednie okno."""
        if role == "customer":
            self.open_customer_window()
        elif role == "employee":
            self.open_worker_window()
        elif role == "admin":
            self.open_admin_window()

    def open_customer_window(self):
        from gui.customer_window import CustomerWindow
        self.customer_window = CustomerWindow()
        self.customer_window.show()
        self.close()

    def open_worker_window(self):
        from gui.worker_window import WorkerWindow
        self.worker_window = WorkerWindow()
        self.worker_window.show()
        self.close()

    def open_admin_window(self):
        from gui.admin_window import AdminWindow
        self.admin_window = AdminWindow()
        self.admin_window.show()
        self.close()


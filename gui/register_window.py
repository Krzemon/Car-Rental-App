from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from psycopg2 import errors
import re
from database.db_connector import get_connection
import traceback

class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rejestracja")

        self.first_name_input = QLineEdit(self)
        self.last_name_input = QLineEdit(self)
        self.address_input = QLineEdit(self)
        self.phone_input = QLineEdit(self)
        self.email_input = QLineEdit(self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.register_button = QPushButton("Zarejestruj", self)
        self.register_button.clicked.connect(self.register)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Imię:"))
        layout.addWidget(self.first_name_input)
        layout.addWidget(QLabel("Nazwisko:"))
        layout.addWidget(self.last_name_input)
        layout.addWidget(QLabel("Adres:"))
        layout.addWidget(self.address_input)
        layout.addWidget(QLabel("Numer telefonu:"))
        layout.addWidget(self.phone_input)
        layout.addWidget(QLabel("E-mail:"))
        layout.addWidget(self.email_input)
        layout.addWidget(QLabel("Hasło:"))
        layout.addWidget(self.password_input)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def validate_email(self, email):
        """
        Walidacja adresu e-mail.
        """
        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
            return False
        return True
    
    def register(self):
        """
        Rejestracja nowego użytkownika.
        """
        first_name = self.first_name_input.text().strip()
        last_name = self.last_name_input.text().strip()
        address = self.address_input.text().strip()
        phone_number = self.phone_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if not first_name or not last_name or not address or not phone_number or not email or not password:
            QMessageBox.warning(self, "Input Error", "Proszę wypełnić wszystkie pola.")
            return

        if not self.validate_email(email):
            QMessageBox.warning(self, "Invalid Email", "Proszę podać poprawny adres e-mail.")
            return

        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM projekt_bd1.users WHERE email = %s", (email,))
            if cursor.fetchone():
                QMessageBox.warning(self, "Email Exists", "Email jest już zarejestrowany.")
                return

            cursor.execute(
                """
                INSERT INTO projekt_bd1.users (email, password, role) 
                VALUES (%s, %s, %s) RETURNING user_id
                """,
                (email, password, 'customer')
            )

            result = cursor.fetchone()
            if result is None:
                raise Exception("Nie udało się uzyskać user_id po dodaniu użytkownika.")

            user_id = result['user_id']

            cursor.execute(
                """
                INSERT INTO projekt_bd1.customers (first_name, last_name, address, phone_number, email)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (first_name, last_name, address, phone_number, email)
            )

            cursor.execute(
                """
                UPDATE projekt_bd1.customers
                SET user_id = projekt_bd1.users.user_id
                FROM projekt_bd1.users
                WHERE projekt_bd1.customers.email = projekt_bd1.users.email
                AND projekt_bd1.customers.email = %s
                """,
                (email,)
            )

            conn.commit()
            QMessageBox.information(self, "Registration Successful", "Konto zostało pomyślnie utworzone.")

            self.close()
            self.open_login_window()

        except errors.UndefinedTable as e:
            QMessageBox.critical(self, "Database Error", "Tabela w bazie danych nie istnieje. Skontaktuj się z administratorem.")
        except Exception as e:
            if conn:
                conn.rollback()
            error_message = f"Wystąpił błąd podczas rejestracji: {str(e)}"
            print("Exception:", error_message)
            print("Traceback:", traceback.format_exc())
            QMessageBox.critical(self, "Database Error", error_message)

    def open_login_window(self):
        """Otwórz okno logowania po zakończeniu rejestracji."""
        from gui.login_window import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
import sys
from PyQt6.QtWidgets import QApplication
from gui.login_window import LoginWindow
from database.db_connector import initialize_connection, close_connection


def main():
    initialize_connection()

    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()

    exit_code = app.exec()

    # Zamknięcie połączenia przy wyjściu
    close_connection()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()

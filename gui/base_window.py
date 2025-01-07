from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QStatusBar, QTabWidget, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QFont, QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize, QTimer

from database.db_connector import close_connection, get_connection

font = QFont("Lora", 12, QFont.Weight.Bold)

class BaseWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Aplikacja wypożyczalni samochodów")
        self.setGeometry(100, 100, 1000, 600)
        self.setStyleSheet("background-color: #2f2f2f; color: white;")

        self.layout = QVBoxLayout(self)
        self.tool_layout = QHBoxLayout()

        title_font = QFont("Lora", 12, QFont.Weight.Bold)
        self.title_label = QLabel("Panel")
        self.title_label.setFont(title_font)

        self.tool_layout.addWidget(self.title_label)

        # Spacer
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.tool_layout.addItem(spacer)

        # Status połączenia
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

        # Tryb ciemny/jasny
        self.dark_light_mode_button = QPushButton()
        self.dark_light_mode_button.setIcon(QIcon("resources/images/mode.png"))
        self.dark_light_mode_button.setIconSize(QSize(32, 32))
        self.dark_light_mode_button.setToolTip("Włącz tryb ciemny")
        self.dark_light_mode_button.setFixedSize(40, 40)
        self.dark_light_mode_button.clicked.connect(self.toggle_dark_light_mode)
        self.tool_layout.addWidget(self.dark_light_mode_button, alignment=Qt.AlignmentFlag.AlignRight)

        # Przycisk wylogowania
        self.logout_button = QPushButton("Wyloguj", self)
        self.logout_button.clicked.connect(self.logout)
        self.tool_layout.addWidget(self.logout_button, alignment=Qt.AlignmentFlag.AlignRight)

        # Dodanie pasek narzędzi
        self.layout.addLayout(self.tool_layout)
        # self.status_bar = QStatusBar(self)
        # self.layout.addWidget(self.status_bar)

        self.is_dark_mode = True

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
        """Przełącz tryb ciemny/jasny."""
        if self.is_dark_mode:
            self.setStyleSheet("background-color: white; color: black;")
            self.dark_light_mode_button.setToolTip("Włącz tryb ciemny")
            # self.status_bar.showMessage("Włączono tryb jasny", 2000)
        else:
            self.setStyleSheet("background-color: #2f2f2f; color: white;")
            self.dark_light_mode_button.setToolTip("Włącz tryb jasny")
            # self.status_bar.showMessage("Włączono tryb ciemny", 2000)
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
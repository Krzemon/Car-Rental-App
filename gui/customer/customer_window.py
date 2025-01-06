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

        self.profile_widget = self.create_profile_view()
        self.cars_widget = self.create_cars_view()

        self.tabs.addTab(self.profile_widget, "Profil")
        self.tabs.addTab(self.cars_widget, "Samochody")


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

    def create_profile_view(self):
        """Tworzy widok profilu klienta."""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Witamy w profilu klienta"))
        layout.addWidget(QLabel("Tutaj możesz zarządzać swoimi rezerwacjami"))
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












    def rent_car(self):
        car_id = self.car_id_input.text()
        customer_id = self.customer_id_input.text()

        if not car_id or not customer_id:
            self.result_label.setText("Please enter valid car and customer IDs.")
            return

        conn = connect_to_db()
        cur = conn.cursor()

        # Check if the car is available
        cur.execute("SELECT status FROM cars WHERE car_id = %s", (car_id,))
        car = cur.fetchone()

        if car and car[0] == "available":
            rental_date = QDate.currentDate().toString("yyyy-MM-dd")
            cur.execute("""
                INSERT INTO rentals (customer_id, car_id, rental_date, return_date)
                VALUES (%s, %s, %s, NULL)
                """, (customer_id, car_id, rental_date))

            cur.execute("UPDATE cars SET status = 'rented' WHERE car_id = %s", (car_id,))
            conn.commit()
            self.result_label.setText(f"Car {car_id} rented successfully!")
        else:
            self.result_label.setText(f"Car {car_id} is not available.")

        cur.close()
        conn.close()

    def return_car(self):
        car_id = self.car_id_input.text()
        customer_id = self.customer_id_input.text()

        if not car_id or not customer_id:
            self.result_label.setText("Please enter valid car and customer IDs.")
            return

        conn = connect_to_db()
        cur = conn.cursor()

        # Check if the car is rented by the customer
        cur.execute("""
            SELECT rental_id, rental_date FROM rentals
            WHERE car_id = %s AND customer_id = %s AND return_date IS NULL
            """, (car_id, customer_id))
        rental = cur.fetchone()

        if rental:
            return_date = QDate.currentDate().toString("yyyy-MM-dd")
            rental_id = rental[0]

            cur.execute("""
                UPDATE rentals SET return_date = %s WHERE rental_id = %s
                """, (return_date, rental_id))

            cur.execute("UPDATE cars SET status = 'available' WHERE car_id = %s", (car_id,))
            conn.commit()
            self.result_label.setText(f"Car {car_id} returned successfully!")
        else:
            self.result_label.setText(f"Car {car_id} was not rented by customer {customer_id}.")

        cur.close()
        conn.close()
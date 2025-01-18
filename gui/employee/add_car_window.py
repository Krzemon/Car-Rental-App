from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QHBoxLayout, QLabel, QFrame, QSlider, QStatusBar, QTabWidget, QPushButton

from database.db_connector import get_connection

class AddCarWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dodaj Samochód")
        self.setGeometry(150, 150, 400, 300)
        self.form_layout = QFormLayout()

        self.make_input = QLineEdit()
        self.model_input = QLineEdit()
        self.year_input = QLineEdit()
        self.license_plate_input = QLineEdit()
        self.daily_rate_input = QLineEdit()
        self.vin_input = QLineEdit()
        self.status_input = QLineEdit()
        self.fuel_type_input = QLineEdit()
        self.insurance_status_input = QLineEdit()
        self.seat_count_input = QLineEdit()
        self.color_input = QLineEdit()
        self.type_input = QLineEdit()

        self.form_layout.addRow("Marka:", self.make_input)
        self.form_layout.addRow("Model:", self.model_input)
        self.form_layout.addRow("Rok:", self.year_input)
        self.form_layout.addRow("Numer rejestracyjny:", self.license_plate_input)
        self.form_layout.addRow("Dzienna stawka:", self.daily_rate_input)
        self.form_layout.addRow("VIN:", self.vin_input)
        self.form_layout.addRow("Status:", self.status_input)
        self.form_layout.addRow("Rodzaj paliwa:", self.fuel_type_input)
        self.form_layout.addRow("Status ubezpieczenia:", self.insurance_status_input)
        self.form_layout.addRow("Liczba miejsc:", self.seat_count_input)
        self.form_layout.addRow("Kolor:", self.color_input)
        self.form_layout.addRow("Typ:", self.type_input)
    
        self.add_button = QPushButton("Dodaj Samochód")
        self.add_button.clicked.connect(self.add_car_to_db)
        self.form_layout.addWidget(self.add_button)
        self.setLayout(self.form_layout)

    def add_car_to_db(self):
        make = self.make_input.text()
        model = self.model_input.text()
        year = self.year_input.text()
        license_plate = self.license_plate_input.text()
        daily_rate = self.daily_rate_input.text()
        vin = self.vin_input.text()
        status = self.status_input.text()
        fuel_type = self.fuel_type_input.text()
        insurance_status = self.insurance_status_input.text()
        seat_count = self.seat_count_input.text()
        color = self.color_input.text()
        type = self.type_input.text()


        if not make or not model or not year or not license_plate or not daily_rate or not vin or not status or not fuel_type or not insurance_status or not seat_count or not color or not type:
            print("Wszystkie pola muszą być wypełnione!")
            return
        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                "INSERT INTO projekt_bd1.cars (make, model, year, license_plate, daily_rate, vin, status, fuel_type, insurance_status, seat_count, color, type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (make, model, year, license_plate, daily_rate, vin, status, fuel_type, insurance_status, seat_count, color, type)
            )
            connection.commit()
            print("Samochód dodany do bazy!")
        except Exception as e:
            print(f"Błąd podczas dodawania samochodu: {e}")

        self.close()

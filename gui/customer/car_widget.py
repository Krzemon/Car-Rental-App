from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer

from database.db_connector import get_connection
import psycopg2

class CarWidget(QWidget):
    """ Widget reprezentujący samochód w interfejsie klienta. """
    def __init__(self, customer_id, car, parent=None):
        super().__init__(parent)
        self.current_customer_id = customer_id
        self.db_connection = get_connection()
        self.db_cursor = self.db_connection.cursor()
        
        self.car = car
        self.image_index = 0
        self.image_paths = [
            f"resources/images/cars/{car.make.lower().replace(' ', '-')}_{car.model.lower().replace(' ', '-').replace('.', '-')}_{car.year}a.jpg",
            f"resources/images/cars/{car.make.lower().replace(' ', '-')}_{car.model.lower().replace(' ', '-').replace('.', '-')}_{car.year}b.jpg"
        ]

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.image_label)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.switch_image)
        self.timer.start(3000)  # 3 sekundy
        self.update_image()

        description = f"{car.make} {car.model} ({car.year})"
        description_label = QLabel(description)
        description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(description_label)

        rent_button = QPushButton("Wypożycz")
        rent_button.clicked.connect(self.rent_car)
        layout.addWidget(rent_button)

    def switch_image(self):
        self.image_index = (self.image_index + 1) % len(self.image_paths)
        self.update_image()

    def update_image(self):
        pixmap = QPixmap(self.image_paths[self.image_index])
        # self.image_label.setPixmap(pixmap.scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio))
        self.image_label.setPixmap(pixmap.scaled(400, 250, Qt.AspectRatioMode.IgnoreAspectRatio))

    def rent_car(self):
        """ Wypożycza samochód: zmienia status na 'rented' oraz dodaje rekord do tabeli rentals."""
        car_id = self.car.car_id

        print(f"Wypożyczanie samochodu o ID {car_id} przez klienta o ID {self.current_customer_id}.")
        try:
            self.db_cursor.execute(
                "UPDATE projekt_bd1.cars SET status = 'rented' WHERE car_id = %s",
                (car_id,)
            )

            self.db_cursor.execute(
                "INSERT INTO projekt_bd1.rentals (customer_id, car_id) VALUES (%s, %s)",
                (self.current_customer_id, car_id)
            )

            self.db_cursor.execute(
                "UPDATE projekt_bd1.customers SET active_rental = TRUE WHERE customer_id = %s",
                (self.current_customer_id,)
            )
            self.db_connection.commit()

        except psycopg2.Error as e:
            print(f"Błąd podczas wypożyczania samochodu: {e}")
            self.db_connection.rollback()
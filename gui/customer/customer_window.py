from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QStatusBar, QTabWidget, QGridLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QFont, QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize, QTimer

from database.db_connector import get_connection
from gui.base_window import BaseWindow
from database.models import Car
import psycopg2
# from gui.customer.rent_car_view import RentCarView

class CustomerWindow(BaseWindow):
    def __init__(self, user_id):
        self.user_id = user_id
        super().__init__()
        self.title_label.setText("Panel Klienta")

        self.current_page = 0
        self.cars_per_page = 4
        # self.current_user_id = 
        connection = get_connection()
        cursor = connection.cursor()
        me_query = "SELECT customer_id FROM projekt_bd1.customers WHERE user_id=%s"
        cursor.execute(me_query, (self.user_id ,))
        self.customer_id = cursor.fetchone()['customer_id']
        self.cars = [car for car in Car.get_all(connection) if car.status == 'available']
        
        self.tabs = QTabWidget(self)
        self.cars_widget = self.create_cars_view()
        self.rentals_widget = self.create_rentals_view()
        self.faq_widget = self.create_faq_view()
        self.history_widget = self.create_history_view()

        self.tabs.addTab(self.cars_widget, "Samochody")
        self.tabs.addTab(self.rentals_widget, "Wypożyczenia")
        self.tabs.addTab(self.faq_widget, "FAQ")
        self.tabs.addTab(self.history_widget, "Historia")
        self.layout.addWidget(self.tabs)

        self.setLayout(self.layout)

    def create_rentals_view(self):
        pass

    def create_faq_view(self):
        pass

    def create_history_view(self):
        pass

    def create_cars_view(self):
        """Tworzy widok Pojazdów dla klienta."""
        widget = QWidget()

        layout = QVBoxLayout()
        widget.setLayout(layout)

        self.grid_layout = QGridLayout()
        layout.addLayout(self.grid_layout)

        pagination_layout = QHBoxLayout()
        layout.addLayout(pagination_layout)

        prev_button = QPushButton("Poprzednia strona")
        prev_button.clicked.connect(self.previous_page)
        pagination_layout.addWidget(prev_button)

        next_button = QPushButton("Następna strona")
        next_button.clicked.connect(self.next_page)
        pagination_layout.addWidget(next_button)

        self.update_grid()

        return widget

    def update_grid(self):
        """Aktualizuje widok siatki samochodów na podstawie bieżącej strony."""
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        start_index = self.current_page * self.cars_per_page
        end_index = start_index + self.cars_per_page
        cars_on_page = self.cars[start_index:end_index]

        for i, car in enumerate(cars_on_page):
            row = i // 2
            col = i % 2
            car.make = car.make.strip()
            car.model = car.model.strip()
            car_widget = CarWidget(self.customer_id, car)
            self.grid_layout.addWidget(car_widget, row, col)

    def next_page(self):
        if (self.current_page + 1) * self.cars_per_page < len(self.cars):
            self.current_page += 1
            self.update_grid()

    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_grid()

class CarWidget(QWidget):
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

        # Obraz samochodu
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.image_label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.switch_image)
        self.timer.start(3000)  # 3 sekundy
        self.update_image()

        # Opis samochodu
        description = f"{car.make} {car.model} ({car.year})"
        description_label = QLabel(description)
        description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(description_label)

        rent_button = QPushButton("Wypożycz")
        rent_button.clicked.connect(self.rent_car)
        layout.addWidget(rent_button)
        return_button = QPushButton("Zwróć")
        return_button.clicked.connect(self.return_car)
        layout.addWidget(return_button)

    def switch_image(self):
        self.image_index = (self.image_index + 1) % len(self.image_paths)
        self.update_image()

    def update_image(self):
        pixmap = QPixmap(self.image_paths[self.image_index])
        self.image_label.setPixmap(pixmap.scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio))

    def rent_car(self):
        """
        Wypożycza samochód: zmienia status na 'rented' oraz dodaje rekord do tabeli rentals.
        """
        car_id = self.car.car_id

        print(f"Wypożyczanie samochodu o ID {car_id} przez klienta o ID {self.current_customer_id}.")
        try:
            # self.db_connection.begin()

            self.db_cursor.execute(
                "UPDATE projekt_bd1.cars SET status = 'rented' WHERE car_id = %s",
                (car_id,)
            )

            # Sprawdzamy, czy status rzeczywiście się zmienił
            # if self.db_cursor.rowcount == 0:
            #     print("Samochód już jest wypożyczony lub nie istnieje.")
            #     self.db_connection.rollback()  # Wycofanie transakcji
            #     return

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

    def return_car(self, car_id):
        pass
    #     """Metoda do zwrotu samochodu (zmiana statusu na 'available')"""
    #     try:
    #         # Zaktualizowanie statusu na 'available' w bazie danych
    #         self.db_cursor.execute("UPDATE cars SET status = %s WHERE car_id = %s", ('available', car_id))
    #         self.db_connection.commit()  # Zatwierdzenie zmian
    #         print(f"Samochód o ID {car_id} został zwrócony.")
    #         # Odśwież widok po zwróceniu
    #         self.refresh_car_view()
    #     except psycopg2.Error as e:
    #         print(f"Błąd podczas zwrotu samochodu: {e}")
    #         self.db_connection.rollback()  # Rollback w przypadku błędu


            # def return_car(rental_id, customer_id, car_id):
            #     # 1. Zaktualizuj return_date w tabeli rentals
            #     cursor.execute(
            #         "UPDATE rentals SET return_date = CURRENT_DATE WHERE rental_id = %s",
            #         (rental_id,)
            #     )

            #     # 2. Ustaw kolumnę active_rental w tabeli customers na FALSE
            #     cursor.execute(
            #         "UPDATE customers SET active_rental = FALSE WHERE customer_id = %s",
            #         (customer_id,)
            #     )

            #     # 3. Ustaw status samochodu na 'available'
            #     cursor.execute(
            #         "UPDATE cars SET status = 'available' WHERE car_id = %s",
            #         (car_id,)
            #     )

            #     connection.commit()
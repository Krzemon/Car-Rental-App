from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget, QGridLayout, QPushButton, QTableWidget, QTableWidgetItem, QSpacerItem, QSizePolicy, QFrame
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt

from database.db_connector import get_connection
from gui.base_window import BaseWindow
from database.models import Car
import psycopg2
from gui.customer.car_widget import CarWidget
from datetime import date

class CustomerWindow(BaseWindow):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

        self.title_label.setText("Panel Klienta")

        self.current_page = 0
        self.cars_per_page = 4

        self.connection = get_connection()
        self.cursor = self.connection.cursor()
        my_id = "SELECT customer_id FROM projekt_bd1.customers WHERE user_id=%s"
        self.cursor.execute(my_id, (self.user_id ,))        
        self.customer_id = self.cursor.fetchone()['customer_id']
        
        self.cars = [car for car in Car.get_all(self.connection) if car.status == 'available']
        
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
# --------------------------------------------        
    def create_rentals_view(self):
        """Tworzy widok ostatniego wypożyczenia samochodu z przyciskiem zwrotu."""
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        # Nagłówek
        header_label = QLabel("Aktualnie wypożyczone", alignment=Qt.AlignmentFlag.AlignTop)
        header_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header_label)

        try:
            rentals = self.get_rentals(self.customer_id)
            rented = next((rental for rental in rentals if rental['status'] == 'rented'), None)

            if rented:
                car_id = rented['car_id']
                make = rented['make']
                model = rented['model']
                year = rented['year']
                status = rented['status']
                daily_rate = rented['daily_rate']

                license_plate = rented['license_plate']
                rental_date = rented['rental_date']

                today = date.today()
                days_difference = (today - rental_date).days + 1
                total_price = days_difference * daily_rate

                image_path = f"resources/images/cars/{make.lower().replace(' ', '-')}_{model.lower().replace(' ', '-').replace('.', '-')}_{year}a.jpg"
                image_label = QLabel()
                pixmap = QPixmap(image_path)
                if not pixmap.isNull():
                    pixmap = pixmap.scaled(800, 500, Qt.AspectRatioMode.KeepAspectRatio)
                    image_label.setPixmap(pixmap)
                else:
                    image_label.setText("Brak zdjęcia samochodu")

                image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                layout.addWidget(image_label)

                car_label = QLabel(f"{make} {model}")
                car_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
                car_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                layout.addWidget(car_label)

                # Dane szczegółowe samochodu
                details_layout = QHBoxLayout()
                details_label = QLabel(f"Numer rejestracyjny: {license_plate}\n"
                                    f"Data wypożyczenia: {rental_date}")
                details_label.setFont(QFont("Arial", 14))
                details_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                details_layout.addWidget(details_label)
                layout.addLayout(details_layout)

                spacer_det = QSpacerItem(0, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
                layout.addItem(spacer_det)

                # Dane odnosnie wypozyczenia
                rental_details_layout = QHBoxLayout()
                rental_details_label = QLabel(f"Wypożyczony od {days_difference} dni\n"
                                    f"Kwota zapłaty wynosi {total_price} PLN")
                rental_details_label.setFont(QFont("Arial", 14))
                rental_details_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                rental_details_layout.addWidget(rental_details_label)
                layout.addLayout(rental_details_layout)

                spacer = QSpacerItem(0, 50, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
                layout.addItem(spacer)

                return_button = QPushButton("Zwróć samochód")
                return_button.setFont(QFont("Arial", 12))
                return_button.clicked.connect(lambda: self.return_car(car_id))
                layout.addWidget(return_button)
            else:
                no_rented_label = QLabel("Brak wypożyczonego samochodu.")
                no_one_spacer = QSpacerItem(0, 50, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
                layout.addItem(no_one_spacer)
                no_rented_label.setStyleSheet("color: red;")
                layout.addWidget(no_rented_label)

        except psycopg2.Error as e:
            error_label = QLabel(f"Błąd podczas pobierania danych: {e}")
            error_label.setStyleSheet("color: red;")
            layout.addWidget(error_label)

        return widget

    def return_car(self, car_id):
        """
        Zwraca samochód: zmienia status na 'available', aktualizuje dane w tabeli rentals 
        i ustawia aktywne wypożyczenie klienta na FALSE.
        :param car_id: ID samochodu do zwrotu
        """
        try:
            rentals = self.get_rentals(self.customer_id)

            rented = next((rental for rental in rentals if rental['status'] == 'rented'), None)
            # SELECT r.car_id, c.make, c.model, c.status, c.license_plate, r.rental_date, r.return_date
            if rented:
                # Zaktualizowanie statusu samochodu na 'available'
                update_car_status = """
                    UPDATE projekt_bd1.cars 
                    SET status = 'available' 
                    WHERE car_id = %s
                """
                # Ustawienie daty zwrotu w tabeli rentals na bieżącą datę
                update_rental_return_date = """
                    UPDATE projekt_bd1.rentals 
                    SET return_date = CURRENT_DATE 
                    WHERE car_id = %s AND customer_id = %s AND return_date IS NULL
                """
                # Zaktualizowanie statusu aktywnego wypożyczenia klienta
                update_customer_status = """
                    UPDATE projekt_bd1.customers 
                    SET active_rental = FALSE 
                    WHERE customer_id = %s
                """

                self.cursor.execute(update_car_status, (car_id,))
                self.cursor.execute(update_rental_return_date, (car_id, self.customer_id))
                self.cursor.execute(update_customer_status, (self.customer_id,))

                self.connection.commit()

                print(f"Samochód o ID {car_id} został zwrócony pomyślnie.")

        except Exception as e:
            # Obsługa błędów
            print(f"Błąd podczas zwrotu samochodu: {e}")
            self.connection.rollback()
# --------------------------------------------        
    def create_faq_view(self):
        """Tworzy widok FAQ dla klienta."""

        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        header_label = QLabel("Często Zadawane Pytania (FAQ)", alignment=Qt.AlignmentFlag.AlignTop)
        header_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header_label)

        faq_layout = QGridLayout()
        layout.addLayout(faq_layout)

        # Nagłówki kolumn
        question_header = QLabel("Pytanie")
        question_header.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        answer_header = QLabel("Odpowiedź")
        answer_header.setFont(QFont("Arial", 14, QFont.Weight.Bold))

        faq_layout.addWidget(question_header, 0, 0)
        faq_layout.addWidget(answer_header, 0, 1)

        # Przykładowe pytania i odpowiedzi
        faq = [
            ("Czy mogę zarezerwować samochód na konkretny dzień?", "Tak, możesz zarezerwować samochód na konkretny dzień poprzez naszą stronę internetową."),
            ("Jakie dokumenty są wymagane do wypożyczenia samochodu?", "Potrzebujesz ważnego prawa jazdy oraz dokumentu tożsamości."),
            ("Czy są dostępne foteliki dziecięce?", "Tak, oferujemy foteliki dziecięce na życzenie."),
            ("Czy mogę anulować rezerwację?", "Tak, rezerwację można anulować do 24 godzin przed planowanym wypożyczeniem."),
            ("Czy samochody są ubezpieczone?", "Tak, wszystkie nasze samochody są objęte podstawowym ubezpieczeniem."),
            ("Czy mogę zwrócić samochód w innym miejscu?", "Tak, oferujemy możliwość zwrotu w innym miejscu za dodatkową opłatą.")
        ]

        # Dodanie pytań i odpowiedzi do grid layoutu z odstępami i liniami
        for i, (question, answer) in enumerate(faq):
            question_label = QLabel(question)
            question_label.setFont(QFont("Arial", 12))
            answer_label = QLabel(answer)
            answer_label.setFont(QFont("Arial", 12))
            answer_label.setWordWrap(True)

            faq_layout.addWidget(question_label, i * 2 + 1, 0)
            faq_layout.addWidget(answer_label, i * 2 + 1, 1)

            # Dodanie linii oddzielającej
            if i < len(faq) - 1:
                separator = QFrame()
                separator.setFrameShape(QFrame.Shape.HLine)
                separator.setFrameShadow(QFrame.Shadow.Sunken)
                faq_layout.addWidget(separator, i * 2 + 2, 0, 1, 2)

        # Dodanie pustego miejsca na dole, aby wypełnić przestrzeń
        spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addItem(spacer)

        return widget

# --------------------------------------------        
    def create_history_view(self):
        """Tworzy widok historii wypożyczeń w formie tabeli."""
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        header_label = QLabel("Historia Wypożyczeń", alignment=Qt.AlignmentFlag.AlignTop)
        header_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header_label)

        self.history_table = QTableWidget()

        layout.addWidget(self.history_table)

        self.history_table.setColumnCount(5)
        self.history_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.history_table.setHorizontalHeaderLabels(
            ['Data wypożyczenia', 'Data zwrotu', 'Samochód', 'Rejestracja', 'Rocznik']
        )
        self.load_to_table()
        self.history_table.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)

        return widget

    def load_to_table(self):
        """Ładuje dane do tabeli."""
        try:
            rentals = self.get_rentals(self.customer_id)
            self.history_table.setRowCount(len(rentals))

            for row, rental in enumerate(rentals):
                rental_date = rental['rental_date']
                return_date = rental['return_date']
                car_make = rental['make']
                car_model = rental['model']
                license_plate = rental['license_plate']
                car_year = rental['year']

                self.history_table.setItem(row, 0, QTableWidgetItem(str(rental_date)))
                self.history_table.setItem(row, 1, QTableWidgetItem(str(return_date)))
                self.history_table.setItem(row, 2, QTableWidgetItem(f"{car_make} {car_model}"))
                self.history_table.setItem(row, 3, QTableWidgetItem(license_plate))
                self.history_table.setItem(row, 4, QTableWidgetItem(str(car_year)))
            self.history_table.resizeColumnsToContents()
        except Exception as e:
            print(f"Błąd ładowania danych do tabeli: {e}")

# --------------------------------------------        
    def create_cars_view(self):
        """Tworzy widok Pojazdów dla klienta."""
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        # Nagłówek
        header_label = QLabel("Wypożyczalnia", alignment=Qt.AlignmentFlag.AlignTop)
        header_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header_label)

        cars_spacer = QSpacerItem(0, 50, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addItem(cars_spacer)
        
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

    def get_rentals(self, customer_id):
        """
        Pobiera ostatnie wypożyczenia klienta z bazy danych.
        :param customer_id: ID klienta
        :return: Krotka z danymi wypożyczenia (car_id, make, model, status) lub None
        """
        query = """
            SELECT r.car_id, c.make, c.model, c.status, c.license_plate, r.rental_date, r.return_date, c.year, c.daily_rate
            FROM projekt_bd1.rentals r 
            JOIN projekt_bd1.cars c ON r.car_id = c.car_id 
            WHERE r.customer_id = %s 
            ORDER BY r.rental_date DESC 
        """
        self.cursor.execute(query, (customer_id,))
        rows = self.cursor.fetchall()
        rentals = []
        for row in rows:
            rental = {
                'car_id': row.get('car_id'),
                'make': row.get('make'),
                'model': row.get('model'),
                'status': row.get('status'),
                'license_plate': row.get('license_plate'),
                'rental_date': row.get('rental_date'),
                'return_date': row.get('return_date'),
                'year': row.get('year'),
                'daily_rate': row.get('daily_rate')
            }
            rentals.append(rental)
        return rentals
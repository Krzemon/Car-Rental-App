from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget, QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from database.db_connector import get_connection
from gui.base_window import big_font, light_font

desc_1 = "Generuje raport w postaci tabeli najpopularniejszych samochodów wypożyczanych przez klientów w danym okresie czasu."
desc_2 = "Generuje raport w postaci tabeli podsumowującej wynajmy dla każdego klienta."
desc_3 = "Generuje raport w postaci tabeli miesięcznego przychodu z wypożyczeń."

class ReportView:
    """ Klasa odpowiedzialna za generowanie raportów. """
    def __init__(self):
        self.connection = get_connection()
        self.report_description = QLabel(desc_1)
        self.report_description.setFont(light_font)
        self.report_description.setWordWrap(True)

        self.views = [
            {
                "title": "Popularne samochody",
                "columns": ["Car ID", "Car Name", "Rental Count"],
                "data": self._get_popular_cars()
            },
            {
                "title": "Podsumowanie wynajmu klienta",
                "columns": ["Customer ID", "Customer Name", "Total Rentals"],
                "data": self._get_customer_rentals_summary()
            },
            {
                "title": "Miesięczny przychód",
                "columns": ["Miesiąc", "Przychód"],
                "data": self._get_monthly_revenue()
            },
        ]

    def _get_popular_cars(self):
        """
        Pobiera dane z widoku popular_cars.
        :return: Lista danych.
        """
        return [
            (c.car_id, c.car_name, c.rental_count)
            for c in PopularCar.get_all(self.connection)
        ]

    def _get_customer_rentals_summary(self):
        """
        Pobiera dane z widoku customer_rentals_summary.
        :return: Lista danych.
        """
        return [
            (s.customer_id, s.customer_name, s.total_rentals)
            for s in CustomerRentalSummary.get_all(self.connection)
        ]

    def _get_monthly_revenue(self):
        """
        Pobiera dane dotyczące miesięcznego przychodu z wypożyczeń.
        :return: Lista danych.
        """
        return [
            (r.month, r.revenue)
            for r in MonthlyRevenue.get_all(self.connection)
        ]

    def create(self):
        """
        Tworzy widget z zakładkami dla raportów.
        :return: QWidget z zakładkami.
        """
        widget = QWidget()
        layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()
        
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_widget = QWidget()
        right_widget.setLayout(right_layout)
        right_widget.setFixedWidth(400)

        tabs = QTabWidget()
        for view in self.views:
            tab = self._create_tab(view["data"], view["columns"], view["title"])
            tabs.addTab(tab, view["title"])
        left_layout.addWidget(tabs)

        report_label = QLabel("Raporty", alignment=Qt.AlignmentFlag.AlignCenter)
        report_label.setFont(big_font)
        right_layout.addWidget(report_label)
        right_layout.addWidget(self.report_description)

        tabs.currentChanged.connect(self.on_tab_change)

        self.image_label = QLabel()
        pixmap = QPixmap("resources/images/cars_logo.png")
        scaled_pixmap = pixmap.scaled(360, 360) # Skalowanie obrazu
        self.image_label.setPixmap(scaled_pixmap)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.addWidget(self.image_label)

        layout.addLayout(left_layout)
        layout.addWidget(right_widget)
        widget.setLayout(layout)
        return widget
    
    def on_tab_change(self, index):
        """
        Funkcja wywoływana przy zmianie zakładki.
        :param index: Indeks aktualnie wybranej zakładki.
        """
        current_tab_title = self.views[index]["title"]
        
        if current_tab_title == "Popularne samochody":
            self.report_description.setText(desc_1)
        elif current_tab_title == "Podsumowanie wynajmu klienta":
            self.report_description.setText(desc_2)
        elif current_tab_title == "Miesięczny przychód":
            self.report_description.setText(desc_3)

    def _create_tab(self, data, columns, title):
        """
        Tworzy pojedynczy widget zakładki z tabelą.
        :param data: Dane do wyświetlenia (lista krotek).
        :param columns: Kolumny tabeli (lista stringów).
        :param title: Tytuł zakładki.
        :return: QWidget dla zakładki.
        """
        tab = QWidget()
        tab_layout = QVBoxLayout()

        # title_label = QLabel(title)
        # tab_layout.addWidget(title_label)

        table = QTableWidget()
        table.setRowCount(len(data))
        table.setColumnCount(len(columns))
        table.setHorizontalHeaderLabels(columns)

        for row_idx, row_data in enumerate(data):
            for col_idx, cell_data in enumerate(row_data):
                table.setItem(row_idx, col_idx, QTableWidgetItem(str(cell_data)))

        tab_layout.addWidget(table)
        tab.setLayout(tab_layout)
        return tab

#-------------------------------------------
class CustomerRentalSummary:
    """ Klasa reprezentująca podsumowanie wynajmu klienta. """
    def __init__(self, customer_id, customer_name, total_rentals):
        """
        Inicjalizuje obiekt CustomerRentalSummary.
        :param customer_id: ID klienta (int)
        :param customer_name: Imię i nazwisko klienta (str)
        :param total_rentals: Liczba wypożyczeń (int)
        """
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.total_rentals = total_rentals

    def __repr__(self):
        """ Reprezentacja obiektu jako string. """
        return f"CustomerRentalSummary(customer_id={self.customer_id}, customer_name='{self.customer_name}', total_rentals={self.total_rentals})"
    
    @classmethod
    def from_db_row(cls, row):
        """
        Tworzy obiekt CustomerRentalSummary na podstawie wiersza z bazy danych.
        :param row: Tuple lub RealDictRow (słownik)
        :return: Obiekt CustomerRentalSummary
        """
        if isinstance(row, dict):  # Obsługuje RealDictRow jako słownik
            return cls(
                customer_id=row.get('customer_id'),
                customer_name=row.get('customer_name'),
                total_rentals=row.get('total_rentals')
            )
        elif isinstance(row, (tuple, list)) and len(row) == 3:
            return cls(*row)
        else:
            raise ValueError(f"Nieprawidłowy wiersz: {row}")

    @classmethod
    def get_all(cls, connection):
        """
        Pobiera wszystkie dane z widoku customer_rentals_summary.
        :param connection: Obiekt połączenia do bazy danych
        :return: Lista obiektów CustomerRentalSummary
        """
        query = """
            SELECT customer_id, customer_name, total_rentals
            FROM projekt_bd1.customer_rentals_summary
        """
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            return [cls.from_db_row(row) for row in rows]
        finally:
            cursor.close()
#--------------------------------------------
class PopularCar:
    """ Klasa reprezentująca popularny samochód. """
    def __init__(self, car_id, car_name, rental_count):
        """
        Inicjalizuje obiekt PopularCar.
        :param car_id: ID samochodu (int)
        :param car_name: Nazwa samochodu (str)
        :param rental_count: Liczba wypożyczeń (int)
        """
        self.car_id = car_id
        self.car_name = car_name
        self.rental_count = rental_count

    def __repr__(self):
        return f"PopularCar(car_id={self.car_id}, car_name='{self.car_name}', rental_count={self.rental_count})"
    
    @classmethod
    def from_db_row(cls, row):
        """
        Tworzy obiekt PopularCar na podstawie wiersza z bazy danych.
        :param row: Tuple lub RealDictRow (słownik)
        :return: Obiekt PopularCar
        """
        if isinstance(row, dict):  # Obsługuje RealDictRow jako słownik
            return cls(
                car_id=row.get('car_id'),
                car_name=row.get('car_name'),
                rental_count=row.get('rental_count')
            )
        elif isinstance(row, (tuple, list)) and len(row) == 3:
            return cls(*row)
        else:
            raise ValueError(f"Nieprawidłowy wiersz: {row}")

    @classmethod
    def get_all(cls, connection):
        """
        Pobiera wszystkie dane z widoku popular_cars.
        :param connection: Obiekt połączenia do bazy danych
        :return: Lista obiektów PopularCar
        """
        query = """
            SELECT car_id, car_name, rental_count
            FROM projekt_bd1.popular_cars
        """
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            return [cls.from_db_row(row) for row in rows]
        finally:
            cursor.close()

#--------------------------------------------
class MonthlyRevenue:
    """ Klasa reprezentująca miesięczny przychód. """
    def __init__(self, month, revenue):
        """
        Inicjalizuje obiekt MonthlyRevenue.
        :param month: Miesiąc w formacie 'YYYY-MM' (str)
        :param revenue: Przychód w danym miesiącu (float)
        """
        self.month = month
        self.revenue = revenue

    def __repr__(self):
        return f"MonthlyRevenue(month='{self.month}', revenue={self.revenue})"
    
    @classmethod
    def from_db_row(cls, row):
        """
        Tworzy obiekt MonthlyRevenue na podstawie wiersza z bazy danych.
        Obsługuje zarówno krotki, jak i obiekty przypominające słowniki.
        :param row: Tuple lub RealDictRow (słownik)
        :return: Obiekt MonthlyRevenue
        """
        if isinstance(row, dict):  # Obsługuje RealDictRow jako słownik
            return cls(
                month=row.get('month'),
                revenue=row.get('revenue')
            )
        elif isinstance(row, (tuple, list)) and len(row) == 2:
            return cls(row[0], row[1])
        else:
            raise ValueError(f"Nieprawidłowy wiersz: {row}")

    @classmethod
    def get_all(cls, connection):
        """
        Pobiera dane z widoku monthly_revenue.
        :param connection: Obiekt połączenia do bazy danych
        :return: Lista obiektów MonthlyRevenue
        """
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT month, revenue FROM projekt_bd1.monthly_revenue")
            rows = cursor.fetchall()

            monthly_revenue_data = [cls.from_db_row(row) for row in rows]
            return monthly_revenue_data
        except Exception as e:
            print(f"Error fetching monthly revenue: {e}")
            return []
        finally:
            cursor.close()
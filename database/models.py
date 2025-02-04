class User:
    def __init__(self, user_id, email, role, status, created_at):
        """
        Inicjalizuje obiekt User.
        :param user_id: ID użytkownika (int)
        :param email: E-mail użytkownika (str)
        :param role: Rola użytkownika (str)
        """
        self.user_id = user_id
        self.email = email
        self.role = role
        self.status = status
        self.created_at = created_at

    def __repr__(self):
        """
        Zwraca reprezentację obiektu User w czytelnej formie.
        """
        return f"User(user_id={self.user_id}, email='{self.email}', role='{self.role}', status='{self.status}', created_at='{self.created_at}')"
    
    @classmethod
    def from_db_row(cls, row):
        """
        Tworzy obiekt User na podstawie wiersza z bazy danych.
        Obsługuje zarówno krotki, jak i obiekty przypominające słowniki.
        :param row: Tuple lub RealDictRow (słownik)
        :return: Obiekt User
        """
        if isinstance(row, dict):  # Obsługa RealDictRow jako słownika
            return cls(
                user_id=row.get('user_id'),
                email=row.get('email'),
                role=row.get('role'),
                status=row.get('status'),
                created_at=row.get('created_at')
            )
        elif isinstance(row, (tuple, list)) and len(row) == 5:
            return cls(*row)
        else:
            raise ValueError(f"Nieprawidłowy wiersz: {row}")

    @classmethod
    def get_all(cls, connection):
        """
        Pobiera wszystkich użytkowników z bazy danych.
        :param connection: Obiekt połączenia do bazy danych
        :return: Lista obiektów User
        """
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT user_id, email, role, status, created_at FROM projekt_bd1.users")
            rows = cursor.fetchall()

            users = [cls.from_db_row(row) for row in rows]
            return users
        except Exception as e:
            print(f"Error fetching users: {e}")
            return []
        finally:
            cursor.close()

# --------------------------------------------

class Employee:
    def __init__(self, employee_id, first_name, last_name, address, phone_number, email):
        """
        Inicjalizuje obiekt Employee.
        :param employee_id: ID pracownika (int)
        :param first_name: Imię pracownika (str)
        :param last_name: Nazwisko pracownika (str)
        :param address: Adres pracownika (str)
        :param phone_number: Numer telefonu pracownika (str)
        :param email: E-mail pracownika (str)
        """
        self.employee_id = employee_id
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.phone_number = phone_number
        self.email = email

    def __repr__(self):
        """
        Zwraca reprezentację obiektu Employee w czytelnej formie.
        """
        return (f"Employee(employee_id={self.employee_id}, first_name='{self.first_name}', "
                f"last_name='{self.last_name}', address='{self.address}', "
                f"phone_number='{self.phone_number}', email='{self.email}')")

    @classmethod
    def from_db_row(cls, row):
        """
        Tworzy obiekt Employee na podstawie wiersza z bazy danych.
        :param row: Tuple lub RealDictRow (słownik)
        :return: Obiekt Employee
        """
        if isinstance(row, dict):
            return cls(
                employee_id=row.get('employee_id'),
                first_name=row.get('first_name'),
                last_name=row.get('last_name'),
                address=row.get('address'),
                phone_number=row.get('phone_number'),
                email=row.get('email')
            )
        elif isinstance(row, (tuple, list)) and len(row) == 6:
            return cls(*row)
        else:
            raise ValueError(f"Nieprawidłowy wiersz: {row}")

    @classmethod
    def get_all(cls, connection):
        """
        Pobiera wszystkich pracowników z bazy danych.
        :param connection: Obiekt połączenia do bazy danych
        :return: Lista obiektów Employee
        """
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT employee_id, first_name, last_name, address, phone_number, email FROM projekt_bd1.employees")
            rows = cursor.fetchall()

            employees = [cls.from_db_row(row) for row in rows]
            return employees
        except Exception as e:
            print(f"Error fetching employees: {e}")
            return []
        finally:
            cursor.close()

# --------------------------------------------

class Customer:
    def __init__(self, customer_id, first_name, last_name, address, phone_number, email):
        """
        Inicjalizuje obiekt Customer.
        :param customer_id: ID klienta (int)
        :param first_name: Imię klienta (str)
        :param last_name: Nazwisko klienta (str)
        :param address: Adres klienta (str)
        :param phone_number: Numer telefonu klienta (str)
        :param email: E-mail klienta (str)
        """
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.phone_number = phone_number
        self.email = email

    def __repr__(self):
        """
        Zwraca reprezentację obiektu Customer w czytelnej formie.
        """
        return (f"Customer(customer_id={self.customer_id}, first_name='{self.first_name}', "
                f"last_name='{self.last_name}', address='{self.address}', "
                f"phone_number='{self.phone_number}', email='{self.email}')")
    
    @classmethod
    def from_db_row(cls, row):
        """
        Tworzy obiekt Customer na podstawie wiersza z bazy danych.
        :param row: Tuple lub RealDictRow (słownik)
        :return: Obiekt Customer
        """
        if isinstance(row, dict):  # Obsługa RealDictRow jako słownika
            return cls(
                customer_id=row.get('customer_id'),
                first_name=row.get('first_name'),
                last_name=row.get('last_name'),
                address=row.get('address'),
                phone_number=row.get('phone_number'),
                email=row.get('email')
            )
        elif isinstance(row, (tuple, list)) and len(row) == 6:
            return cls(*row)
        else:
            raise ValueError(f"Nieprawidłowy wiersz: {row}")

    @classmethod
    def get_all(cls, connection):
        """
        Pobiera wszystkich klientów z bazy danych.
        :param connection: Obiekt połączenia do bazy danych
        :return: Lista obiektów Customer
        """
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT customer_id, first_name, last_name, address, phone_number, email FROM projekt_bd1.customers")
            rows = cursor.fetchall()

            customers = [cls.from_db_row(row) for row in rows]
            return customers
        except Exception as e:
            print(f"Error fetching customers: {e}")
            return []
        finally:
            cursor.close()

# --------------------------------------------

class Car:
    def __init__(self, car_id, make, model, year, license_plate, daily_rate, vin, status, fuel_type, insurance_status, seat_count, color, _type):
        """
        Inicjalizuje obiekt Car.
        :param car_id: ID samochodu (int)
        :param make: Marka samochodu (str)
        :param model: Model samochodu (str)
        :param year: Rok produkcji samochodu (int)
        :param license_plate: Numer rejestracyjny samochodu (str)
        :param daily_rate: Dzienna stawka wynajmu samochodu (float)
        :param vin: Numer VIN samochodu (str)
        :param status: Status dostępnosci (str)
        :param fuel_type: Rodzaj paliwa (str)
        :param insurance_status: Status ubezpieczenia (str)
        :param seat_count: Liczba miejsc w samochodzie (int)
        :param color: E-mail klienta (str)
        :param type: Typ samochodu (str)
        """
        self.car_id = car_id
        self.make = make
        self.model = model
        self.year = year
        self.license_plate = license_plate
        self.daily_rate = daily_rate
        self.vin = vin
        self.status = status
        self.fuel_type = fuel_type
        self.insurance_status = insurance_status
        self.seat_count = seat_count
        self.color = color
        self.type = _type

    def __repr__(self):
        """
        Zwraca reprezentację obiektu Car w czytelnej formie.
        """
        return (f"Car(car_id={self.car_id}, make='{self.make}', model='{self.model}', "
                f"year={self.year}, license_plate='{self.license_plate}', daily_rate={self.daily_rate}, "
                f"vin='{self.vin}', status='{self.status}', fuel_type='{self.fuel_type}', "
                f"insurance_status='{self.insurance_status}', seat_count={self.seat_count}, color='{self.color}', type='{self.type}')")
    
    @classmethod
    def from_db_row(cls, row):
        """
        Tworzy obiekt Car na podstawie wiersza z bazy danych.
        :param row: Tuple lub RealDictRow (słownik)
        :return: Obiekt Car
        """
        if isinstance(row, dict):  # Obsługa RealDictRow jako słownika
            return cls(
                car_id=row.get('car_id'),
                make=row.get('make'),
                model=row.get('model'),
                year=row.get('year'),
                license_plate=row.get('license_plate'),
                daily_rate=row.get('daily_rate'),
                vin=row.get('vin'),
                status=row.get('status'),
                fuel_type=row.get('fuel_type'),
                insurance_status=row.get('insurance_status'),
                seat_count=row.get('seat_count'),
                color=row.get('color'),
                _type=row.get('type')
            )
        elif isinstance(row, (tuple, list)) and len(row) == 13:
            return cls(*row)
        else:
            raise ValueError(f"Nieprawidłowy wiersz: {row}")

    @classmethod
    def get_all(cls, connection):
        """
        Pobiera wszystkie samochody z bazy danych.
        :param connection: Obiekt połączenia do bazy danych
        :return: Lista obiektów Car
        """
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT car_id, make, model, year, license_plate, daily_rate, vin, status, fuel_type, insurance_status, seat_count, color, type FROM projekt_bd1.cars")
            rows = cursor.fetchall()

            cars = [cls.from_db_row(row) for row in rows]
            return cars
        except Exception as e:
            print(f"Error fetching cars: {e}")
            return []
        finally:
            cursor.close()


# --------------------------------------------
class Rental:
    def __init__(self, rental_id, customer_id, car_id, rental_date, return_date, customer_name, phone_number, car_name, rental_status):
        """
        Inicjalizuje obiekt rental.
        :param rental_id: ID wypożyczenia (int)
        :param customer_id: ID klienta (int)
        :param car_id: ID samochodu (int)
        :param rental_date: Data wypożyczenia (str)
        :param return_date: Data zwrotu (str)
        :param customer_name: Imię i nazwisko klienta (str)
        :param phone_number: Numer telefonu klienta (str)
        :param car_name: Nazwa samochodu (str)
        :param rental_status: Status wypożyczenia (str)
        """
        self.rental_id = rental_id
        self.customer_id = customer_id
        self.car_id = car_id
        self.rental_date = rental_date
        self.return_date = return_date
        self.customer_name = customer_name
        self.phone_number = phone_number
        self.car_name = car_name
        self.rental_status = rental_status

    def __repr__(self):
        """
        Zwraca reprezentację obiektu Rental w czytelnej formie.
        """
        return (f"Rental(rental_id={self.rental_id}, customer_id={self.customer_id}, car_id={self.car_id}, "
                f"rental_date='{self.rental_date}', return_date='{self.return_date}', customer_name='{self.customer_name}', "
                f"phone_number='{self.phone_number}', car_name='{self.car_name}', rental_status='{self.rental_status}')")
        
    @classmethod
    def from_db_row(cls, row):
        """
        Tworzy obiekt Rental na podstawie wiersza z bazy danych.
        :param row: Tuple lub RealDictRow (słownik)
        :return: Obiekt Rental
        """
        if isinstance(row, dict):  # Obsługuje RealDictRow jako słownik
            return cls(
                rental_id=row.get('rental_id'),
                customer_id=row.get('customer_id'),
                car_id=row.get('car_id'),
                rental_date=row.get('rental_date'),
                return_date=row.get('return_date'),
                customer_name=row.get('customer_name'),
                phone_number=row.get('phone_number'),
                car_name=row.get('car_name'),
                rental_status=row.get('rental_status')
            )
        elif isinstance(row, (tuple, list)) and len(row) == 9:
            return cls(*row)
        else:
            raise ValueError(f"Nieprawidłowy wiersz: {row}")

    @classmethod
    def get_all(cls, connection):
        """
        Pobiera wszystkie wypożyczenia z bazy danych z widoku rental_status.
        :param connection: Obiekt połączenia do bazy danych
        :return: Lista obiektów Rental
        """
        cursor = connection.cursor()
        try:
            # Zapytanie do widoku rental_status
            cursor.execute("""
                SELECT rental_id, customer_id, car_id, rental_date, return_date, customer_name, phone_number, car_name, rental_status
                FROM projekt_bd1.rental_status
            """)
            rows = cursor.fetchall()

            rentals = [cls.from_db_row(row) for row in rows]
            return rentals
        except Exception as e:
            print(f"Error fetching rentals: {e}")
            return []
        finally:
            cursor.close()

# --------------------------------------------
class Payment:
    def __init__(self, payment_id, rental_id, payment_date, amount, status):
        """
        Inicjalizuje obiekt rental.
        :param payment_id: ID płatności (int)
        :param rental_id: ID wypożyczenia (int)
        :param payment_date: Data płatności (str)
        :param amount: Kwota płatności (float)
        :param status: Status płatności (str)
        """
        self.payment_id = payment_id
        self.rental_id = rental_id
        self.payment_date = payment_date
        self.amount = amount
        self.status = status

    def __repr__(self):
        """
        Zwraca reprezentację obiektu Payment w czytelnej formie.
        """
        return (f"Payment(payment_id={self.payment_id}, rental_id={self.rental_id}, "
                f"payment_date='{self.payment_date}', amount={self.amount}, status='{self.status}')")
    
    @classmethod
    def from_db_row(cls, row):
        """
        Tworzy obiekt Payment na podstawie wiersza z bazy danych.
        :param row: Tuple lub RealDictRow (słownik)
        :return: Obiekt Payment
        """
        if isinstance(row, dict):  # Obsługuje RealDictRow jako słownik
            return cls(
                payment_id=row.get('payment_id'),
                rental_id=row.get('rental_id'),
                payment_date=row.get('payment_date'),
                amount=row.get('amount'),
                status=row.get('status')
            )
        elif isinstance(row, (tuple, list)) and len(row) == 5:
            return cls(*row)
        else:
            raise ValueError(f"Nieprawidłowy wiersz: {row}")
        
    @classmethod
    def get_all(cls, connection):
        """
        Pobiera wszystkie płatności z bazy danych.
        :param connection: Obiekt połączenia do bazy danych
        :return: Lista obiektów Payment
        """
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT payment_id, rental_id, payment_date, amount, status FROM projekt_bd1.payments")
            rows = cursor.fetchall()

            payments = [cls.from_db_row(row) for row in rows]
            return payments
        except Exception as e:
            print(f"Error fetching payments: {e}")
            return []
        finally:
            cursor.close()
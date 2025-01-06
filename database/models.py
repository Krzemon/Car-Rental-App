class User:
    def __init__(self, user_id, email, role):
        """
        Inicjalizuje obiekt User.
        :param user_id: ID użytkownika (int)
        :param email: E-mail użytkownika (str)
        :param role: Rola użytkownika (str)
        """
        self.user_id = user_id
        self.email = email
        self.role = role

    def __repr__(self):
        """
        Zwraca reprezentację obiektu User w czytelnej formie.
        """
        return f"User(user_id={self.user_id}, email='{self.email}', role='{self.role}')"
    
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
                role=row.get('role')
            )
        elif isinstance(row, (tuple, list)) and len(row) == 3:  # Obsługa krotek/list
            user_id, email, role = row
            return cls(user_id, email, role)
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
            cursor.execute("SELECT user_id, email, role FROM projekt_bd1.users")
            rows = cursor.fetchall()

            users = [cls.from_db_row(row) for row in rows]
            return users
        except Exception as e:
            print(f"Error fetching users: {e}")
            return []
        finally:
            cursor.close()

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
        elif isinstance(row, (tuple, list)) and len(row) == 6:  # Obsługa krotek/list
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


class Car:
    def __init__(self, car_id, make, model, year, license_plate, daily_rate, vin, status, fuel_type, insurance_status, seat_count, color):
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

    def __repr__(self):
        """
        Zwraca reprezentację obiektu Car w czytelnej formie.
        """
        return (f"Car(car_id={self.car_id}, make='{self.make}', model='{self.model}', "
                f"year={self.year}, license_plate='{self.license_plate}', daily_rate={self.daily_rate}, "
                f"vin='{self.vin}', status='{self.status}', fuel_type='{self.fuel_type}', "
                f"insurance_status='{self.insurance_status}', seat_count={self.seat_count}, color='{self.color}')")
    
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
                color=row.get('color')
            )
        elif isinstance(row, (tuple, list)) and len(row) == 6:  # Obsługa krotek/list
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
            cursor.execute("SELECT car_id, make, model, year, license_plate, daily_rate, vin, status, fuel_type, insurance_status, seat_count, color FROM projekt_bd1.cars")
            rows = cursor.fetchall()

            cars = [cls.from_db_row(row) for row in rows]
            return cars
        except Exception as e:
            print(f"Error fetching cars: {e}")
            return []
        finally:
            cursor.close()
-- Wstawianie danych do tabeli users
INSERT INTO projekt_bd1.users (email, password, role) VALUES
    ('prys@poczta', 'admin', 'admin'),
        ('mpawlik@poczta', 'haslo', 'employee'),
    ('jkowalski@poczta', 'haslo', 'customer');

-- Wstawianie danych do tabeli cars
INSERT INTO projekt_bd1.customers (first_name, last_name, address, phone_number, email)
    VALUES ('Andrzej', 'Nowak','Krakow', '+48111222333', 'pnowak@poczta');

UPDATE projekt_bd1.customers
    SET user_id = users.user_id
    FROM users
    WHERE customers.email = users.email;

-- Wstawianie danych do tabeli cars
INSERT INTO projekt_bd1.employees (first_name, last_name, address, phone_number, email)
    VALUES ('Bogdan', 'Grabowski','Krakow', '+48666777888', 'bgrabowski@poczta');

INSERT INTO projekt_bd1.employees (first_name, last_name, address, phone_number, email)
    VALUES ('Przemysław', 'Ryś','Krakow', '+48111000111', 'prys@poczta');

UPDATE projekt_bd1.employees
    SET user_id = users.user_id
    FROM users
    WHERE employees.email = users.email;

-- Wstawianie pełnych danych dla wszystkich samochodów
INSERT INTO projekt_bd1.cars (make, model, year, license_plate, daily_rate, vin, status, fuel_type, insurance_status, seat_count, color, type)
VALUES 
    ('Audi', 'A4', 2015, 'KR12345', 20.00, '1HGCM82633A123456', 'available', 'petrol', 'insured', 5, 'black', 'sedan'),
    ('Porsche', 'Panamera Turbo E-hybryda', 2024, 'KR23455', 50.00, '2HGCM82633A123456', 'available', 'hybrid', 'insured', 5, 'orange', 'sedan'),
    ('Ford', 'F-150', 2021, 'KR33455', 35.00, '2HGCM82633A323456', 'available', 'petrol', 'insured', 5, 'red', 'van'),
    ('Hyundai', 'IONIQ 5', 2022, 'KR33555', 32.00, '2HYCM82633A323446', 'available', 'electric', 'insured', 5, 'beige', 'suv'),
    ('Mercedes-Benz', 'C63s AMG E', 2023, 'KR44444', 60.00, '2HYCG72633A363444', 'available', 'petrol', 'insured', 5, 'gray', 'sedan'),
    ('Subaru', 'WRX', 2022, 'KR43355', 40.00, '2HGDM82633A321455', 'available', 'petrol', 'insured', 5, 'orange', 'sedan'),
    ('Volkswagen', 'ID.7', 2024, 'KR23455', 35.00, '2BGNM82677A333456', 'available', 'electric', 'insured', 5, 'gray', 'sedan'),
    ('Volkswagen', 'ID.7', 2024, 'KR44455', 35.00, '2BGNM82677A333456', 'available', 'electric', 'insured', 5, 'gray', 'sedan'),
    ('BMW', 'M3 E46 Coupe', 2002, 'KR98275', 50.00, '2BGNM03677K733416', 'available', 'petrol', 'insured', 4, 'gray', 'coupe'),
    ('Ford', 'Focus ST', 2012, 'KR22275', 35.00, '2BGNM036A1K73G416', 'available', 'diesel', 'insured', 5, 'orange', 'hatchback'),
    ('Jaguar', 'F-Type Convertible', 2021, 'KR21574', 75.00, '2AGGM026A1F73G416', 'available', 'petrol', 'insured', 2, 'white', 'cabriolet'),
    ('Mercedes-Benz', 'C-Class Estate', 2022, 'KR21363', 50.00, '2HCDM026A1F74G416', 'available', 'diesel', 'insured', 5, 'blue', 'estate'),
    ('Tesla', 'Model Y', 2021, 'KR27763', 75.00, '2HCYM025A1F74R4T6', 'available', 'electric', 'insured', 5, 'gray', 'suv'),
    ('Volkswagen', 'Transporter T6', 2016, 'KR42363', 50.00, '2HCDM026F1G44G416', 'available', 'diesel', 'insured', 9, 'gray', 'van'),
    ('Mercedes-Benz', 'Vito E-Cell ', 2011, 'KR24677', 60.00, '2HCDM026T3W34G496', 'available', 'electric', 'insured', 2, 'white', 'van'),
    ('Kia', 'Sorento', 2021, 'KR82679', 80.00, '2HCSM02ST3I34G496', 'available', 'petrol', 'insured', 7, 'blue', 'suv');
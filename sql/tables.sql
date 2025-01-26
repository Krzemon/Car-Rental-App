CREATE SCHEMA projekt_bd1;
SET SEARCH_PATH TO projekt_bd1;

-----------    TABLES    --------------------

-- Tabela reprezentująca encję użytkowników
CREATE TABLE IF NOT EXISTS projekt_bd1.users (
    user_id SERIAL PRIMARY KEY, -- Klucz główny
    email VARCHAR(255) UNIQUE NOT NULL CHECK (email LIKE '%@%'), -- Email z ograniczeniem
    password VARCHAR(255) NOT NULL, -- Hasło
    role VARCHAR(10) CHECK (role IN ('customer', 'employee', 'admin')) NOT NULL, -- Rola użytkownika
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'banned', 'deleted')), -- Status konta
    created_at DATE DEFAULT CURRENT_DATE -- Data utworzenia konta
);

-- Tabela reprezentująca encję samochodów
CREATE TABLE IF NOT EXISTS projekt_bd1.cars (
    car_id SERIAL PRIMARY KEY, -- Klucz główny
    make VARCHAR(64) NOT NULL, -- Marka
    model VARCHAR(64) NOT NULL, -- Model
    year INT NOT NULL, -- Rok produkcji
    license_plate VARCHAR(50) UNIQUE NOT NULL,  -- Numer rejestracyjny
    daily_rate DECIMAL(10, 2) NOT NULL, -- Stawka dzierżawy dzienna
    vin VARCHAR(17) NOT NULL, -- Numer identyfikacyjny pojazdu
    status VARCHAR(32) NOT NULL CHECK (status IN ('available', 'rented')), -- Status pojazdu
    fuel_type VARCHAR(32) NOT NULL CHECK (fuel_type IN ('petrol', 'electric', 'diesel', 'hybrid')), -- Rodzaj paliwa
    insurance_status VARCHAR(32) NOT NULL DEFAULT 'uninsured' CHECK (insurance_status IN ('insured', 'uninsured', 'expired')), -- Status ubezpieczenia
    seat_count INT NOT NULL, -- Liczba miejsc
    color VARCHAR(32) NOT NULL, -- Kolor
    type VARCHAR(16) CHECK (type IN ('coupe', 'hatchback', 'cabriolet', 'estate', 'sedan', 'suv', 'van')), -- Typ pojazdu
    CONSTRAINT unique_vin UNIQUE (vin) -- Unikalny numer VIN
);

-- Tabela reprezentująca encję klientów
CREATE TABLE IF NOT EXISTS projekt_bd1.customers (
    customer_id SERIAL PRIMARY KEY, -- Klucz główny
    first_name VARCHAR(32) NOT NULL, -- Imię
    last_name VARCHAR(32) NOT NULL, -- Nazwisko
    address VARCHAR(64) NOT NULL, -- Adres
    phone_number VARCHAR(12) NOT NULL, -- Numer telefonu
    email VARCHAR(255) UNIQUE NOT NULL CHECK (email LIKE '%@%'), -- Email z ograniczeniem
    user_id INT, -- Obce odniesienie do tabeli users
    active_rental BOOLEAN DEFAULT FALSE, -- Flaga określająca aktywne wynajęcie
    CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(user_id) -- Klucz obcy
);

-- Tabela reprezentująca relację (między klientami a samochodami) wypożyczenia
CREATE TABLE IF NOT EXISTS projekt_bd1.rentals (
    rental_id SERIAL PRIMARY KEY, -- Klucz główny
    customer_id INT NOT NULL REFERENCES projekt_bd1.customers(customer_id), -- klucz obcy z tabeli customer
    car_id INT NOT NULL REFERENCES projekt_bd1.cars(car_id), -- klucz obcy z tabeli cars
    rental_date DATE NOT NULL DEFAULT CURRENT_DATE, -- Data wypożyczenia
    return_date DATE DEFAULT NULL -- Data zwrotu
);

-- Tabela reprezentująca encję pracowników
CREATE TABLE IF NOT EXISTS projekt_bd1.employees (
    employee_id SERIAL PRIMARY KEY, -- Klucz główny
    first_name VARCHAR(32) NOT NULL, -- Imię
    last_name VARCHAR(32) NOT NULL, -- Nazwisko
    address VARCHAR(64) NOT NULL, -- Adres
    phone_number VARCHAR(12) NOT NULL, -- Numer telefonu
    email VARCHAR(255) UNIQUE NOT NULL CHECK (email LIKE '%@%'), -- Email z ograniczeniem
    user_id INT, -- Klucz obcy z tabeli users
);
ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES projekt_bd1.users(user_id);

-- Tabela reprezentująca encję płatności
CREATE TABLE IF NOT EXISTS projekt_bd1.payments (
    payment_id SERIAL PRIMARY KEY, -- Klucz główny
    rental_id INT NOT NULL, -- Klucz obcy z tabeli rentals
    payment_date DATE, -- Data płatności
    amount DECIMAL(10, 2), -- Kwota
    status VARCHAR(10) CHECK (status IN ('paid', 'unpaid')), -- Status płatności
    CONSTRAINT fk_rental FOREIGN KEY (rental_id) REFERENCES rentals (rental_id)
        ON DELETE CASCADE
);

--------------------------------------------------------------------------------
-----------    WIDOKI    --------------------

-- Widok, który łączy dane o wypożyczeniach, klientach i samochodach
CREATE OR REPLACE VIEW projekt_bd1.rental_status AS
SELECT
    r.rental_id,
    r.customer_id,
    r.car_id,
    r.rental_date,
    r.return_date,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.phone_number AS phone_number,
    ca.make || ' ' || ca.model AS car_name,
    -- Jeśli return_date jest NULL, status to "Wypożyczony", w przeciwnym razie "Zwrócony"
    CASE
        WHEN r.return_date IS NULL THEN 'Wypożyczony'
        ELSE 'Zwrócony'
        END AS rental_status
FROM
    projekt_bd1.rentals r
        JOIN
    projekt_bd1.customers c ON r.customer_id = c.customer_id
        JOIN
    projekt_bd1.cars ca ON r.car_id = ca.car_id;

-- Widok, który podsumowuje wypożyczenia klientów
CREATE OR REPLACE VIEW projekt_bd1.customer_rentals_summary AS
SELECT
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    COUNT(r.rental_id) AS total_rentals
FROM projekt_bd1.rentals r
JOIN projekt_bd1.customers c ON r.customer_id = c.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY total_rentals DESC;

--  Widok, który podsumowuje popularność samochodów
CREATE OR REPLACE VIEW projekt_bd1.popular_cars AS
SELECT
    c.car_id,
    c.make || ' ' || c.model AS car_name,
    COUNT(r.rental_id) AS rental_count
FROM projekt_bd1.rentals r
         JOIN projekt_bd1.cars c ON r.car_id = c.car_id
GROUP BY c.car_id, c.make, c.model
ORDER BY rental_count DESC;

-- Widok, który podsumowuje przychody miesięczne
CREATE OR REPLACE VIEW projekt_bd1.monthly_revenue AS
SELECT
    TO_CHAR(r.rental_date, 'YYYY-MM') AS month,  -- Konwertujemy datę na tekstowy format YYYY-MM
    SUM((r.return_date - r.rental_date) * c.daily_rate) AS revenue
FROM projekt_bd1.rentals r
         JOIN projekt_bd1.cars c ON r.car_id = c.car_id
GROUP BY TO_CHAR(r.rental_date, 'YYYY-MM')
ORDER BY month;

-- SELECT * FROM projekt_bd1.customer_rentals_summary;
-- SELECT * FROM projekt_bd1.popular_cars;
-- SELECT * FROM projekt_bd1.monthly_revenue;


--------------------------------------------------------------------------------
-----------    TRIGGERY    --------------------

-- Wyzwalacz sprawdzający daty wypożyczenia i zwrotu:
-- Zapewnia, że data zwrotu nie może być wcześniejsza niż data wypożyczenia.
CREATE OR REPLACE FUNCTION validate_rental_dates()
    RETURNS TRIGGER AS $$
BEGIN
    IF NEW.return_date < NEW.rental_date THEN
        RAISE EXCEPTION 'Data zwrotu (%), nie może być wcześniejsza niż data wypożyczenia (%)',
            NEW.return_date, NEW.rental_date;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_validate_rental_dates
    BEFORE INSERT OR UPDATE ON projekt_bd1.rentals
    FOR EACH ROW
EXECUTE FUNCTION validate_rental_dates();

-- Funkcja triggera
CREATE OR REPLACE FUNCTION create_payment_trigger()
    RETURNS TRIGGER AS $$
DECLARE
    rental_duration INT;
    daily_rate DECIMAL(10, 2);
BEGIN
    IF NEW.return_date IS NOT NULL AND OLD.return_date IS NULL THEN
        -- Obliczanie różnicy dni + 1, ponieważ uwzględniamy pierwszy dzień wypożyczenia
        rental_duration := (NEW.return_date - NEW.rental_date) + 1;

        -- Pobranie daily_rate z tabeli cars
        SELECT c.daily_rate
        INTO daily_rate
        FROM projekt_bd1.cars c
        WHERE c.car_id = NEW.car_id;

        -- Tworzenie nowego rekordu w tabeli payments bez ustawienia payment_date
        INSERT INTO projekt_bd1.payments (rental_id, amount, status)
        VALUES (NEW.rental_id, rental_duration * daily_rate, 'unpaid');
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Dodanie triggera do tabeli rentals (pierwszy trigger)
CREATE TRIGGER after_return_date_set
    AFTER UPDATE OF return_date
    ON projekt_bd1.rentals
    FOR EACH ROW
EXECUTE FUNCTION create_payment_trigger();


-- Funkcja triggera dla aktualizacji payment_date
CREATE OR REPLACE FUNCTION update_payment_date_trigger()
    RETURNS TRIGGER AS $$
BEGIN
    -- Sprawdzenie, czy status zmienia się na 'paid'
    IF NEW.status = 'paid' AND OLD.status = 'unpaid' THEN
        -- Aktualizacja payment_date na aktualną datę
        UPDATE projekt_bd1.payments
        SET payment_date = NOW()
        WHERE rental_id = NEW.rental_id AND status = 'unpaid';  -- Tylko dla rekordów o statusie 'unpaid'
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Dodanie triggera do tabeli payments (drugi trigger)
CREATE TRIGGER after_status_change_to_paid
    AFTER UPDATE OF status
    ON projekt_bd1.payments
    FOR EACH ROW
EXECUTE FUNCTION update_payment_date_trigger();
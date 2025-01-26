import json
import psycopg2
from psycopg2.extras import RealDictCursor

_connection = None

def load_database_config():
    """Ładuje konfigurację bazy danych z pliku JSON."""
    try:
        with open('config/database_config.json', 'r') as config_file:
            config = json.load(config_file)
            return config
    except FileNotFoundError:
        print("Plik konfiguracyjny nie został znaleziony.")
        return None
    except json.JSONDecodeError:
        print("Błąd wczytywania pliku konfiguracyjnego.")
        return None

def initialize_connection():
    """Inicjalizuje połączenie z bazą danych."""
    global _connection
    DATABASE_CONFIG = load_database_config()

    if DATABASE_CONFIG is None:
        print("Nie udało się wczytać konfiguracji bazy danych.")
        return

    if _connection is None or _connection.closed != 0:
        try:
            _connection = psycopg2.connect(**DATABASE_CONFIG, cursor_factory=RealDictCursor)
            print("Połączono z bazą danych.")
        except psycopg2.Error as e:
            print(f"Błąd podczas nawiązywania połączenia: {e}")
            _connection = None

def get_connection():
    """Zwraca połączenie z bazą danych."""
    global _connection
    if _connection is None or _connection.closed != 0:
        raise ConnectionError("Połączenie z bazą danych nie zostało poprawnie zainicjalizowane.")
    return _connection

def close_connection():
    """Zamyka połączenie z bazą danych."""
    global _connection
    if _connection and _connection.closed == 0:
        try:
            _connection.close()
            print("Połączenie z bazą danych zostało zamknięte.")
        except Exception as e:
            print(f"Błąd podczas zamykania połączenia: {e}")
        finally:
            _connection = None

def authenticate_user(email, password):
    """
    Sprawdza, czy dane logowania są poprawne.
    param email: adres e-mail użytkownika
    param password: hasło użytkownika
    return: dane użytkownika lub None, jeśli uwierzytelnianie się nie powiodło
    """
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            query = """
                SELECT user_id, email, role, password
                FROM projekt_bd1.users
                WHERE email = %s AND password = %s
            """
            cursor.execute(query, (email, password))
            user = cursor.fetchone()
            return user
    except Exception as e:
        print(f"Błąd podczas uwierzytelniania użytkownika: {e}")
        return None

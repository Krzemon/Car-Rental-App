from database.db_connector import get_connection
from database.models import User

def get_all_users():
    """Funkcja pobierająca wszystkich użytkowników z bazy danych."""
    connection = get_connection()
    cursor = connection.cursor()
    
    cursor.execute("SELECT user_id, email, role FROM users")
    users_data = cursor.fetchall()
    
    # Zamiana danych z bazy na obiekty User
    users = [User(user_id, email, role) for user_id, email, role in users_data]
    
    # Zamknięcie połączenia
    cursor.close()
    connection.close()

    return users
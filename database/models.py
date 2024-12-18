class User:
    def __init__(self, user_id, email, role):
        self.user_id = user_id
        self.email = email
        self.role = role

    def __repr__(self):
        return f"User(user_id={self.user_id}, email='{self.email}', role='{self.role}')"

    def to_dict(self):
        """Zwraca dane użytkownika w postaci słownika, np. do serializacji."""
        return {
            "user_id": self.user_id,
            "email": self.email,
            "role": self.role
        }

    @classmethod
    def from_db_row(cls, row):
        """Tworzy obiekt User na podstawie wiersza z bazy danych (np. krotka)."""
        user_id, email, role = row
        return cls(user_id, email, role)

    @classmethod
    def get_all(cls, connection):
        """Pobiera wszystkich użytkowników z bazy danych."""
        cursor = connection.cursor()
        cursor.execute("SELECT user_id, email, role FROM projekt_bd1.users")
        rows = cursor.fetchall()
        return [cls.from_db_row(row) for row in rows]
# from database.models import User
# from database.db_connector import get_connection

# class AdminController:
#     def __init__(self):
#         self.connection = get_connection()

#     def get_all_users(self):
#         """Pobiera wszystkich użytkowników z bazy danych."""
#         return User.get_all(self.connection)

#     def add_user(self, email, password, role):
#         """Dodaje użytkownika do bazy danych."""
#         cursor = self.connection.cursor()
#         cursor.execute("INSERT INTO projekt_bd1.users (email, password, role) VALUES (%s, %s, %s)", (email, password, role))
#         self.connection.commit()

#     def delete_user(self, user_id):
#         """Usuwa użytkownika z bazy danych."""
#         cursor = self.connection.cursor()
#         cursor.execute("DELETE FROM projekt_bd1.users WHERE user_id = %s", (user_id,))
#         self.connection.commit()

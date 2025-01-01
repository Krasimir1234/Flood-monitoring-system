import sqlite3
from typing import List, Union, Optional


class X(object):
    singleton_instance = None

    def __init__(self):

        try:
            self.connection = sqlite3.connect("flood_monitor.db")
            print("Successfully connected to SQLite database")
        except sqlite3.Error as e:
            print(f"Error connecting to SQLite database: {e}")

    @staticmethod
    def get_instance():
        if X.singleton_instance is None:
            X.singleton_instance = X()

        return X.singleton_instance


    def create_user(self, full_name: str, email_address: str, username: str, password: str):
        try:
            cursor = self.connection.cursor()
            query = """
                INSERT INTO users (name, email, username, password) 
                VALUES (?, ?, ?, ?)
            """
            cursor.execute(query, (full_name, email_address, username, password))
            self.connection.commit()
            print("User successfully created.")
            return {"status": "success", "message": "User successfully created."}
        except sqlite3.Error as e:
            print(f"Error on adding user: {e}")
            return {"status": "error", "message": str(e)}
        finally:
            cursor.close()


    def get_users(self):
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM users"
            cursor.execute(query)
            users = cursor.fetchall()
            print(f"Retrieved users: {users}")
            return users

        except sqlite3.Error as e:
            print(f"Error on fetching users: {e}")
            return []

        finally:
            cursor.close()


    def remove_user(self, user_id: int):
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM users WHERE user_id = ?"
            cursor.execute(query, (user_id,))
            self.connection.commit()
            print(f"User with ID {user_id} successfully removed.")
            return {"status": "success", "message": f"User with ID {user_id} successfully removed."}

        except sqlite3.Error as e:
            print(f"Error on removing user: {e}")
            return {"status": "error", "message": str(e)}

        finally:
            cursor.close()

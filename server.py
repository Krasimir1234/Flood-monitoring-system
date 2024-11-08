from typing import List, Union, Optional
from mysql.connector import connect, Error
# from flask import jsonify -> Files if needed

class X(object):
    singleton_instance = None

    def __init__(self):
        # MySQL connection configuration
        try:
            self.connection = connect(
                host="localhost",
                user="root",
                password="root17",
                database="flood_monitor"
            )
            print("Successfully connected with MySQL server")   
        except Error as e:
            print(e)

    @staticmethod
    def get_instance():
        if X.singleton_instance is None:
            X.singleton_instance = X()

        return X.singleton_instance


    # CREATE A USER
    def create_user(self, new_user):
        try:
            cursor = self.connection.cursor()
            query = f"INSERT INTO userInfo(full_name, email_adress) VALUES ('{new_user.full_name}', '{new_user.email_adress}')"
            cursor.execute(query)
            self.connection.commit()
            print("User successfully created.")
        except Error as e:
            print(f"Error on adding user: {e}")
        finally: 
            cursor.close()




# TODO: finish operations on users in regards to the DB
"""
    # GET USER
    def get_users(self, Xid):
        users = []
        try:
            cursor = self.connection.cursor()
            query = f"SELECT ui.id, ui.full_name, ui.email_adress FROM userInfo as ui INNER JOIN User AS us ON us.userId = ui.id WHERE us.XID = {Xid}"
            cursor.execute(query)
            for user_data in cursor.fetchall():
                users.append(User(user_id=user_data[0], full_name=user_data[1], email_adress=user_data[2]))

            return users

        except Error as e:
            print(f"Error on fetching users: {e}")


    # REMOVE USER
    def remove_users(self, user_id):
        try:
            cursor = self.connection.cursor()
            query = f"DELETE FROM Xid WHERE id = {user_id}"
            cursor.execute(query)
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error on removing Editor: {e}")
            return False
        finally: 
            cursor.close()

"""
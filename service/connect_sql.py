import mysql.connector
from mysql.connector import Error

class DatabaseConnection:
    def __init__(self, host="localhost", database="EmployeeManagement", user="root", password="123456"):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None

    def connect(self):
        """Establish connection to the MySQL database."""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                print("Connected to the database.")
        except Error as e:
            print(f"Error: '{e}' occurred while connecting to the database")

    def close_connection(self):
        """Close the connection to the MySQL database."""
        if self.connection.is_connected():
            self.connection.close()
            print("The database connection has been closed.")

    def execute_query(self, query, data=None):
        cursor = self.connection.cursor()
        try:
            if data:
                cursor.execute(query, data)
            else:
                cursor.execute(query)
            self.connection.commit()  # Lưu thay đổi
            print("Query executed and committed successfully.")
        except Error as e:
            print(f"Error: '{e}' occurred during query execution")
            self.connection.rollback()  # Khôi phục thay đổi
            print("Transaction rolled back.")
        finally:
            cursor.close()
    def fetch_one(self, query, data=None):
        """Fetch a single result from a SQL query."""
        cursor = self.connection.cursor(dictionary=True)
        try:
            if data:
                cursor.execute(query, data)
            else:
                cursor.execute(query)

            result = cursor.fetchone()  # Lấy một bản ghi
            cursor.fetchall()  # Đọc hết kết quả để tránh lỗi "Unread result found"
            
            return result if result else {}
        except Error as e:
            print(f"Error: '{e}' occurred during data fetch")
            return {}
        finally:
            cursor.close()  # Đảm bảo rằng con trỏ luôn được đóng
    def fetch_all(self, query):
        """Fetch all results from a SQL query."""
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"Error: '{e}' occurred during data fetch")
            return []
        finally:
            cursor.close()
    def commit(self):
        if self.connection and self.connection.is_connected():
            self.connection.commit()
            print("Commit successful.")
        else:
            print("No active connection to commit.")
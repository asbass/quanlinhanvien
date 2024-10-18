import csv
from enity.Payroll import Payroll
from enity.employee import Employee
from mysql.connector import Error
from service.connect_sql import DatabaseConnection
class PayrollList: 
    def __init__(self, filename='Payroll.csv'):
        self.db = DatabaseConnection()
        self.db.connect()  # Connect to the database
        self.Payroll = []
    
    def add_payroll(self, emp_id, month, year, day_off, basic_salary, reward, net_salary):
        try:
            # Tạo một đối tượng Payroll mới
            new_payroll = Payroll(emp_id, month, year, day_off, basic_salary, reward, net_salary)
            
            # Thêm bảng lương vào cơ sở dữ liệu
            query = '''
                INSERT INTO Payroll (payroll_id, emp_id, month, year, day_off, basic_salary, reward, net_salary)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            '''
            self.db.execute_query(query, (
                str(new_payroll.payroll_id), 
                new_payroll.emp_id, 
                new_payroll.month, 
                new_payroll.year, 
                new_payroll.day_off, 
                new_payroll.basic_salary, 
                new_payroll.reward, 
                new_payroll.net_salary
            ))
            print("Payroll record added successfully.")
        except Error as e:
            print(f"Error: '{e}' occurred while adding payroll")

    def load_payrolls(self):
        """Load all payroll records from the database."""
        query = 'SELECT * FROM payroll;'
        records = self.db.fetch_all(query)
        self.payrolls = [Payroll(**record) for record in records]  # Assuming Payroll constructor can accept keyword arguments
        return self.payrolls

    def close_connection(self):
        """Close the database connection."""
        self.db.close_connection()  # Close the connection when no longer in use
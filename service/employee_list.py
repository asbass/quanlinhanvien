from service.connect_sql import DatabaseConnection
from enity.employee import Employee

class EmployeeList:
    def __init__(self):
        self.db = DatabaseConnection()
        self.db.connect()  # Connect to the database

        self.employees = []
        self.load_employees_from_db()
        self.departments = []  # Khởi tạo danh sách phòng ban
        self.department_id = []  # Khởi tạo danh sách ID phòng ban
        print( self.employees)
    def add_employee(self, name, age, department, position):
        # Tìm department_id và position_id từ tên phòng ban và chức vụ
        department_query = "SELECT dept_id FROM Department WHERE name = %s"
        position_query = "SELECT position_id FROM Positions WHERE name = %s"

        department_result = self.db.fetch_one(department_query, (department,))
        position_result = self.db.fetch_one(position_query, (position,))

        department_id = department_result['dept_id']
        position_id = position_result['position_id']

        # Thêm nhân viên mới vào danh sách
        new_employee = Employee(name, age, department_id, position_id)
        self.employees.append(new_employee)
        
        # Thêm vào cơ sở dữ liệu
        query = """
            INSERT INTO Employee (emp_id, name, age, department_id, position_id) 
            VALUES (%s, %s, %s, %s, %s)
        """
        data = (str(new_employee.emp_id), new_employee.name, new_employee.age, new_employee.department, new_employee.position)
        self.db.execute_query(query, data)
    def update_employee(self, emp_id, name, age, department, position):
        emp_id_str = str(emp_id)
        # Debugging: Print the current employee IDs
        print("Current employee IDs:", self.get_employee_ids())

        employee = self.get_employee_by_id(emp_id_str)
        
        if not employee:
            print("No employee found with emp_id:", emp_id_str)
            return

        # Update employee attributes
        employee.name = name
        employee.age = age
        employee.department = department
        employee.position = position

        # Get department_id and position_id from the new department and position names
        department_id = self.get_department_id_by_name(department)
        position_id = self.get_position_id_by_name(position)

        # Update the employee in the database
        query = """
            UPDATE Employee
            SET name = %s, age = %s, department_id = %s, position_id = %s
            WHERE emp_id = %s
        """
        data = (name, age, department_id, position_id, emp_id_str)

        try:
            self.db.execute_query(query, data)
            print(f"Employee {emp_id_str} updated successfully.")
        except Exception as e:
            print("Error updating employee:", e)

    def get_employee_ids(self):
        """Retrieve employee IDs from the database."""
        query = "SELECT emp_id FROM Employee"
        results = self.db.fetch_all(query)  # Assuming this returns a list of dictionaries

        # Extract IDs from the results
        return [result['emp_id'] for result in results]
    def get_position(self, employee_name):
        for employee in self.employees:
            if employee.name == employee_name:  # So sánh với tên
                print(employee.position)
                return employee.position  # Trả về chức vụ nếu tìm thấy
        return ''  # Nếu không tìm thấy, trả về chuỗi rỗng
    def delete_employee(self, emp_id):
        emp_id_str = str(emp_id)  # Chuyển đổi emp_id sang chuỗi nếu cần

        # Kiểm tra xem nhân viên có tồn tại hay không
        check_query = "SELECT * FROM Employee WHERE emp_id = %s"
        existing_employee = self.db.fetch_one(check_query, (emp_id_str,))  # Sử dụng fetch_one để kiểm tra

        if not existing_employee:
            print("Không tìm thấy nhân viên với emp_id:", emp_id_str)
            return
    
        # Truy vấn xóa
        query = "DELETE FROM Employee WHERE emp_id = %s"
        try:
            self.db.execute_query(query, (emp_id_str,))
            print(f"Đã xóa nhân viên có emp_id: {emp_id_str} thành công.")

            # Cập nhật danh sách nhân viên trong bộ nhớ
            self.employees = [emp for emp in self.employees if str(emp.emp_id) != emp_id_str]
        except Exception as e:
            print("Lỗi khi xóa nhân viên:", e)
    def get_employees(self):
        # Lấy danh sách các phòng ban
        query = "SELECT * FROM Employee"
        return self.db.fetch_all(query)
    def get_employee_by_id(self, emp_id):
        """Retrieve employee information by ID from the database."""
        query = "SELECT * FROM Employee WHERE emp_id = %s"
        result = self.db.fetch_one(query, (emp_id,))  # Fetch a single record

        if result:
            # Assuming Employee constructor takes all the necessary fields
            department_name = self.get_department_name_by_id(result['department_id'])
            position_name = self.get_position_name_by_id(result['position_id'])
            
            # Create an Employee object with the retrieved data
            return Employee(result['name'], result['age'], department_name, position_name)
        
        return None  # Return None if no employee found
    def save_to_db(self):
        """Save the current employee list to the database."""
        for emp in self.employees:
            query = """
                INSERT INTO Employee (name, age, department_id, position_id)
                VALUES (%s, %s, %s, %s)
            """
            data = (emp.name, emp.age, emp.department, emp.position)
            self.db.execute_query(query, data)


    def load_employees_from_db(self):
            """Load employees from the database."""
            query = "SELECT * FROM Employee"
            rows = self.db.fetch_all(query)
            for row in rows:
                # Lấy tên phòng ban và chức vụ từ ID
                department_name = self.get_department_name_by_id(row['department_id'])
                position_name = self.get_position_name_by_id(row['position_id'])

                emp = Employee(row['name'], row['age'], department_name, position_name)
                self.employees.append(emp)
    def get_department_name_by_id(self, department_id):
        query = "SELECT name FROM Department WHERE dept_id = %s"
        result = self.db.fetch_one(query, (department_id,))
        return result['name'] if result else None

    def get_position_name_by_id(self, position_id):
        query = "SELECT name FROM Positions WHERE position_id = %s"
        result = self.db.fetch_one(query, (position_id,))
        return result['name'] if result else None
    def get_department_id_by_name(self, department_name):
        query = "SELECT dept_id FROM Department WHERE name = %s"
        result = self.db.fetch_one(query, (department_name,))
        return result['dept_id'] if result else None
    def get_employee_names(self):
        query = "SELECT name FROM Employee"  # Query to fetch employee names
        results = self.db.fetch_all(query)  # Fetch all records
        return [row['name'] for row in results] if results else []
    def get_position_id_by_name(self, position_name):
        query = "SELECT position_id FROM Positions WHERE name = %s"
        result = self.db.fetch_one(query, (position_name,))
        return result['position_id'] if result else None
    def close_connection(self):
        self.db.close_connection()  # Đóng kết nối khi không còn sử dụng
    def get_employee_id_by_name(self, name):
        # Truy vấn để lấy emp_id dựa trên name
        query = "SELECT emp_id FROM Employee WHERE name = ?"
        result = self.db.fetch_one(query, (name,))  # Lấy một bản ghi

        if result:
            return result['emp_id']  # Trả về emp_id nếu tìm thấy
        else:
            print("Không tìm thấy nhân viên với tên:", name)
            return None  # Trả về None nếu không tìm thấy


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
    def add_employee(self, name, age, department, position):
        # Tìm department_id và position_id từ tên phòng ban và chức vụ
        department_id = self.get_department_id_by_name(department)
        position_id = self.get_position_id_by_name(position)
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
        print(f"Inserting employee: {new_employee.name}")  # Debug
    def update_employee(self, emp_id, name, age, department, position):
        emp_id_str = str(emp_id)
        # Debugging: Print the current employee IDs

        employee = self.get_employee_by_id(emp_id_str)

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
        except Exception as e:
            print("Error updating employee:", e)

    def get_employee_ids(self):
        """Retrieve employee IDs from the database."""
        query = "SELECT emp_id FROM Employee"
        results = self.db.fetch_all(query)  # Assuming this returns a list of dictionaries
        # Extract IDs from the results
        return [result['emp_id'] for result in results]
    def get_employee_name(self):
        query = "SELECT name FROM Employee"
        results = self.db.fetch_all(query)  # Assuming this returns a list of dictionaries
        # Extract IDs from the results
        return [result['name'] for result in results]
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
    def get_employeezs(self):
        return self.employees 
    def get_employees(self):
        self.db.close_connection()
        self.db.connect()
        # Lấy danh sách các phòng ban
        query = "SELECT * FROM employee"
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
        
        self.employees.clear()  # Xóa danh sách nhân viên cũ
        
        for row in rows:
            # Lấy tên phòng ban và chức vụ từ ID
            department_name = self.get_department_name_by_id(row['department_id'])
            position_name = self.get_position_name_by_id(row['position_id'])
            # Tạo đối tượng nhân viên với đầy đủ thông tin
            emp = {
                'emp_id': row['emp_id'],
                'name': row['name'],
                'age': row['age'],
                'department_name': department_name,  # Lưu tên phòng ban
                'position_name': position_name      # Lưu tên chức vụ
            }
            # Thêm nhân viên vào danh sách
            self.employees.append(emp)
        return self.employees
    def get_department_name_by_id(self, department_id):
        query = "SELECT name FROM Department WHERE dept_id = %s"
        result = self.db.fetch_one(query, (department_id,))
        return result['name'] if result else None

    def get_position_name_by_id(self, position_id):
        query = "SELECT name FROM Positions WHERE position_id = %s"
        result = self.db.fetch_one(query, (position_id,))
        return result['name'] if result else None
    def get_position_id_from_employee(self, emp_id):
        query = "SELECT position_id FROM Employee WHERE emp_id = %s"
        result = self.db.fetch_one(query, (emp_id,))
        return result['position_id'] if result else None
    def get_department_id_by_name(self, department_name):
        self.db.close_connection()
        self.db.connect()
        query = "SELECT dept_id FROM Department WHERE name = %s"
        result = self.db.fetch_one(query, (department_name,))
        return result['dept_id'] if result else None
    def get_employee_names(self):
        query = "SELECT name FROM Employee"  # Query to fetch employee names
        results = self.db.fetch_all(query)  # Fetch all records
        return [row['name'] for row in results] if results else []
    def get_position_id_by_name(self, position_name):
        self.db.close_connection()
        self.db.connect()
        query = "SELECT position_id FROM Positions WHERE name = %s"
        result = self.db.fetch_one(query, (position_name,))
        return result['position_id'] if result else None
    def close_connection(self):
        self.db.close_connection()  # Đóng kết nối khi không còn sử dụng
    def get_employee_id_by_name(self, name):
        # Truy vấn để lấy emp_id dựa trên name
        query = "SELECT emp_id, position_id FROM Employee WHERE name = %s"
        result = self.db.fetch_one(query, (name,))
        print("da duoc load lai")
        print(name)
        if result:
            return result  # Trả về một từ điển chứa emp_id và position_id
        else:
            print("Không tìm thấy nhân viên với tên:", name)  # Xem xét thêm thông tin
            return None
    def get_employee_name_by_id(self, emp_id):
        # Truy vấn để lấy emp_id dựa trên name
        query = "SELECT name FROM Employee WHERE emp_id = %s"
        result = self.db.fetch_one(query, (emp_id,))  # Lưu ý cú pháp với %s nếu sử dụng MySQL connector
    
        return result['name'] if result else None
    def get_employee_info(self, employee_name):
        query = "SELECT * FROM Employee WHERE name = %s"  # Truy vấn để lấy thông tin nhân viên
        return self.db.fetch_one(query, (employee_name,))  # Trả về thông tin của nhân viên
    def get_all_employees(self):
        """Lấy tất cả nhân viên từ cơ sở dữ liệu."""
        query = "SELECT name FROM Employee"
        results = self.db.fetch_all(query)  # Lấy tất cả kết quả từ bảng Employee

        print("Kết quả truy vấn:", results)  # In kết quả ra để kiểm tra
        if results:  # Kiểm tra xem có kết quả không
            # Sử dụng khóa để truy cập tên nhân viên
            return [{"name": row['name']} for row in results]  # Trả về danh sách các từ điển chứa tên nhân viên
        else:

            print("Không có nhân viên nào trong cơ sở dữ liệu.")
            return []  # Trả về danh sách rỗng nếu không có nhân viên


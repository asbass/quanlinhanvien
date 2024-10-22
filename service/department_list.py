from enity.department import Department  # Chắc chắn rằng đường dẫn nhập đúng
from mysql.connector import Error
from service.connect_sql import DatabaseConnection
from enity.Payroll import Payroll
class departmentList:  # Đặt tên lớp  với chữ cái đầu viết hoa theo quy tắc PEP 8
    def __init__(self):
        self.db = DatabaseConnection()  # Khởi tạo kết nối với cơ sở dữ liệu
        self.db.connect()  # Kết nối đến cơ sở dữ liệu
    def add_department(self,name):
        try:
            # Tạo một đối tượng Payroll mới
            new_department = Department(name)
            
            # Thêm bảng lương vào cơ sở dữ liệu
            query = '''
                INSERT INTO Department (dept_id,name)
                VALUES (%s, %s);
            '''
            self.db.execute_query(query, (
                str(new_department.dept_id), 
                new_department.name
            ))
            print("bảng phòng ban thêm thành công record added successfully.")
        except Error as e:
            print(f"Error: '{e}' occurred while adding payroll")
    def get_department_name(self, department_id):
        query = "SELECT name FROM Department WHERE dept_id = ?"
        self.db.execute_query(query, (department_id,))
        print(department_id)
    def update_department(self, department_id, name):
        try:
            # Cập nhật thông tin phòng ban
            query = "UPDATE Department SET name = %s WHERE dept_id = %s"  # Sửa lỗi cú pháp SQL
            self.db.execute_query(query, (name, department_id))
        except Error as e:
            print(f"Error: '{e}' occurred while updating department")
    def del_department(self, department_id):
         # Xóa phòng ban khỏi cơ sở dữ liệu
            query = "DELETE FROM Department WHERE dept_id = %s"  # Sửa tên trường cho phù hợp
            self.db.execute_query(query, (department_id,))
    def get_departments(self):
        # Lấy danh sách các phòng ban
        self.db.close_connection()
        self.db.connect()
        query = "SELECT * FROM Department"
        return self.db.fetch_all(query)
    def get_department_by_id(self, dept_id):
        query = "SELECT * FROM Department WHERE dept_id = %s"
        return self.fetch_one(query, (dept_id,))

    def get_department_names(self):
            departments = self.get_departments()
            return [department['name'] for department in departments if 'name' in department]  # Safety check for 'name'
    
    # Other methods...

    def close_connection(self):
        self.db.close_connection()  # Đóng kết nối khi không còn sử dụng

    def load_departments(self):
        print("Loading departments from database...")
        try:
            # Lấy danh sách các phòng ban từ cơ sở dữ liệu
            query = "SELECT * FROM Department"
            departments = self.db.fetch_all(query)

            # In thông tin phòng ban
            for department in departments:
                print(f"Department ID: {department['dept_id']}, Name: {department['name']}")  # Sửa tên trường cho phù hợp

            print('Departments loaded successfully')
        except Error as e:
            print(f"Error: '{e}' occurred while loading departments")

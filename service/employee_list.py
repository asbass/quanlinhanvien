import csv
from enity.employee import Employee

class EmployeeList:
    def __init__(self, filename='employees.csv'):
        self.filename = filename
        self.employees = []
        self.load_Employee()  # Tải danh sách nhân viên từ tệp CSV khi khởi tạo
        self.departments = []  # Khởi tạo danh sách phòng ban
        self.department_id = []  # Khởi tạo danh sách ID phòng ban
        print( self.employees)
    def add_employee(self, name, age, department, position):
        new_employee = Employee(name, age, department, position)
        self.employees.append(new_employee)
        self.save_to_csv()  # Save to CSV whenever an employee is deleted

    def get_employee_names(self):
        """Trả về danh sách tên nhân viên."""
        return [employee.name for employee in self.employees]
    def update_employee(self, index, name, age, department, position):
        if 0 <= index < len(self.employees):
            self.employees[index].name = name
            self.employees[index].age = age
            self.employees[index].department = department
            self.employees[index].position = position
        self.save_to_csv()  # Save to CSV whenever an employee is deleted

    def get_employee_ids(self):
        # Trả về danh sách ID nhân viên
        return [employee.emp_id for employee in self.employees]
    def get_position(self, employee_name):
        for employee in self.employees:
            if employee.name == employee_name:  # So sánh với tên
                print(employee.position)
                return employee.position  # Trả về chức vụ nếu tìm thấy
        return ''  # Nếu không tìm thấy, trả về chuỗi rỗng
    def delete_employee(self, index):
        if 0 <= index < len(self.employees):
            del self.employees[index]
            self.save_to_csv()  # Lưu vào tệp CSV mỗi khi xóa nhân viên
    
    def get_employees(self):
        return self.employees
    def get_employee_by_name(self, name):
        for emp in self.employees:
            if emp.name == name:
                return emp
        return None

    def get_employee_names(self):
        return [employee.name for employee in self.employees]
    def get_employee_by_id(self, emp_id):
        return any(emp["emp_id"] == emp_id for emp in self.employees)
    
    def save_to_csv(self):
        with open(self.filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Tên", "Tuổi", "Phòng Ban", "Vị Trí", "Lương"])  # Tiêu đề
            for emp in self.employees:
                writer.writerow([emp.emp_id, emp.name, emp.age, emp.department, emp.position])  # Dữ liệu nhân viên
                print(emp.emp_id)


    def load_Employee(self):
        print("Đang tải danh sách nhân viên từ tệp CSV...")
        try:
            with open(self.filename, mode="r", encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    emp = Employee(
                        name=row['Tên'],
                        age=row['Tuổi'],
                        department=row['Phòng Ban'],
                        position=row['Vị Trí']
                    )
                    self.employees.append(emp)
                    emp.emp_id = int(row['ID'])  # Đặt ID từ tệp CSV

            if self.employees:
                Employee._id_counter = max(emp.emp_id for emp in self.employees) + 1
            else:
                Employee._id_counter = 1
            print("Đã tải thành công danh sách nhân viên.")
        except FileNotFoundError:
            print("Tệp không tồn tại, không làm gì cả.")
        except KeyError as e:
            print(f"KeyError: {e} - Kiểm tra lại tên cột trong tệp CSV.")
        except Exception as e:
            print(f"Đã xảy ra lỗi: {e}")

    def get_employee_info(self, name):
        """Trả về thông tin nhân viên theo tên."""
        for employee in self.employees:
            if employee.name == name:
                # Trả về thông tin dưới dạng dictionary hoặc tuple
                return {
                    'ID': employee.emp_id,
                    'Tên': employee.name,
                    'Tuổi': employee.age,
                    'Phòng Ban': employee.department,
                    'Vị Trí': employee.position
                }
        return None  # Trả về None nếu không tìm thấy nhân viên
    def clear_employee_list(self):
            """Xóa tất cả nhân viên trong danh sách."""
            self.employees.clear()  # Sửa ở đây: sử dụng self.employees thay vì self.employee_list
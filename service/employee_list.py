import csv
from enity.employee import Employee

class EmployeeList:
    def __init__(self, filename='employees.csv'):
        self.filename = filename
        self.employees = []
        self.load_Employee()  # Tải danh sách nhân viên từ tệp CSV khi khởi tạo
        self.departments = []  # Khởi tạo danh sách phòng ban
        self.department_id = []  # Khởi tạo danh sách ID phòng ban

    def add_employee(self, name, age, department, position):
        new_employee = Employee(name, age, department, position)
        self.employees.append(new_employee)
        self.save_to_csv()  # Lưu vào tệp CSV mỗi khi thêm nhân viên
    def get_employee_names(self):
        """Trả về danh sách tên nhân viên."""
        return [employee.name for employee in self.employees]
    def update_employee(self, index, name, age, department, position):
        if 0 <= index < len(self.employees):
            self.employees[index].name = name
            self.employees[index].age = age
            self.employees[index].department = department
            self.employees[index].position = position
            self.save_to_csv()  # Lưu vào tệp CSV mỗi khi sửa nhân viên
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

    def save_to_csv(self):
        with open(self.filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Tên", "Tuổi", "Phòng Ban", "Vị Trí", "Lương"])  # Tiêu đề
            for emp in self.employees:
                writer.writerow([emp.emp_id, emp.name, emp.age, emp.department, emp.position])  # Dữ liệu nhân viên


    def load_Employee(self):
        print("Đang tải danh sách nhân viên từ tệp CSV...")  # Thông báo
        try:
            with open(self.filename, mode="r", encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    emp = Employee(row['Tên'], row['Tuổi'], row['Phòng Ban'], row['Vị Trí'])
                    self.employees.append(emp)
                print("Đã tải thành công danh sách nhân viên.")  # Thông báo tải thành công
        except FileNotFoundError:
            print("Tệp không tồn tại, không làm gì cả.")  # Thông báo nếu tệp không tồn tại
        except KeyError as e:
            print(f"KeyError: {e} - Kiểm tra lại tên cột trong tệp CSV.")  # Thông báo lỗi nếu tên cột không đúng
        except Exception as e:
            print(f"Đã xảy ra lỗi: {e}")  # Thông báo lỗi khác
    def get_employee_info(self, name):
        """Trả về thông tin chi tiết của nhân viên dựa trên tên."""
        for employee in self.employees:
            if employee.name == name:  # So sánh với tên
                return {
                    'emp_id': employee.emp_id,      # Lấy ID
                    'name': employee.name,          # Lấy tên
                    'position': employee.position    # Lấy vị trí
                }
        print(f"Không tìm thấy thông tin cho nhân viên: {name}")  # Thông báo nếu không tìm thấy
        return None  # Nếu không tìm thấy, trả về None.

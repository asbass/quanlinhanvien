import csv
from enity.employee import Employee

class EmployeeList:
    def __init__(self, filename='employees.csv'):
        self.filename = filename
        self.employees = []
        self.load_from_csv()  # Tải danh sách nhân viên từ tệp CSV khi khởi tạo

    def add_employee(self, name, age, department, position, salary):
        new_employee = Employee(name, age, department, position, salary)
        self.employees.append(new_employee)
        self.save_to_csv()  # Lưu vào tệp CSV mỗi khi thêm nhân viên

    def update_employee(self, index, name, age, department, position, salary):
        if 0 <= index < len(self.employees):
            self.employees[index].name = name
            self.employees[index].age = age
            self.employees[index].department = department
            self.employees[index].position = position
            self.employees[index].salary = salary
            self.save_to_csv()  # Lưu vào tệp CSV mỗi khi sửa nhân viên

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
                writer.writerow([emp.emp_id, emp.name, emp.age, emp.department, emp.position, emp.salary])  # Dữ liệu nhân viên


    def load_from_csv(self):
        print("Đang tải danh sách nhân viên từ tệp CSV...")  # Thông báo
        try:
            with open(self.filename, mode="r", encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    emp = Employee(row['Tên'], row['Tuổi'], row['Phòng Ban'], row['Vị Trí'], row['Lương'])
                    self.employees.append(emp)
                print("Đã tải thành công danh sách nhân viên.")  # Thông báo tải thành công
                self.display_employees()
        except FileNotFoundError:
            print("Tệp không tồn tại, không làm gì cả.")  # Thông báo nếu tệp không tồn tại
        except KeyError as e:
            print(f"KeyError: {e} - Kiểm tra lại tên cột trong tệp CSV.")  # Thông báo lỗi nếu tên cột không đúng
        except Exception as e:
            print(f"Đã xảy ra lỗi: {e}")  # Thông báo lỗi khác
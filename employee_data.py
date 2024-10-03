class Employee:
    def __init__(self, emp_id, name, position, age, salary):
        self.emp_id = emp_id         # ID nhân viên
        self.name = name             # Họ tên nhân viên
        self.position = position     # Chức vụ
        self.age = age               # Tuổi
        self.salary = salary         # Lương

    def display_info(self):
        """Hiển thị thông tin nhân viên."""
        return {
            "ID": self.emp_id,
            "Họ Tên": self.name,
            "Chức Vụ": self.position,
            "Tuổi": self.age,
            "Lương": self.salary
        }

    def update_salary(self, new_salary):
        """Cập nhật lương của nhân viên."""
        self.salary = new_salary

    def promote(self, new_position):
        """Thăng chức cho nhân viên."""
        self.position = new_position
employee1 = Employee(emp_id="001", name="Nguyễn Văn A", position="Nhân viên", age=30, salary=5000000)
employee2 = Employee(emp_id="002", name="Trần Thị B", position="Quản lý", age=35, salary=7000000)
employee3 = Employee(emp_id="003", name="Lê Văn C", position="Kỹ sư", age=28, salary=6000000)
employee4 = Employee(emp_id="004", name="Phạm Thị D", position="Nhân viên", age=25, salary=4000000)
employee5 = Employee(emp_id="005", name="Đặng Văn E", position="Giám đốc", age=40, salary=12000000)
employees = [employee1, employee2, employee3, employee4, employee5]

# Hiển thị thông tin của tất cả nhân viên
for emp in employees:
    print(emp.display_info())
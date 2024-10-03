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
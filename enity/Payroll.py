import uuid

class Payroll:
    def __init__(self, emp_id, month, year, day_off, basic_salary, reward, net_salary, payroll_id=None):
        # Tự động tạo UUID nếu payroll_id không được cung cấp
        self.payroll_id = payroll_id if payroll_id else str(uuid.uuid4())
        self.emp_id = emp_id
        self.month = month
        self.year = year
        self.day_off = day_off
        self.basic_salary = basic_salary
        self.reward = reward
        self.net_salary = net_salary

    def __str__(self):
        return (f"Payroll ID: {self.payroll_id}, Employee ID: {self.emp_id}, "
                f"Month: {self.month}, Year: {self.year}, Day Off: {self.day_off}, "
                f"Basic Salary: {self.basic_salary}, Reward: {self.reward}, "
                f"Net Salary: {self.net_salary}")

# Ví dụ sử dụng
payroll_entry = Payroll(emp_id='d8cad11c-4c94-4d93-9754-db0c230eeea0', 
                        month=1, 
                        year=2024, 
                        day_off=1, 
                        basic_salary=50000000.0, 
                        reward=100000.0, 
                        net_salary=5833333.0)

print(payroll_entry)
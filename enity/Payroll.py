import uuid

class Payroll:
    def __init__(self, emp_id, name, position, month, year, day_off, basic_salary, reward, net_salary, payroll_id=None):
        # Tự động tạo UUID nếu payroll_id không được cung cấp
        self.payroll_id = payroll_id if payroll_id else uuid.uuid4()
        self.emp_id = emp_id
        self.name = name
        self.position = position
        self.month = month
        self.year = year
        self.day_off = day_off
        self.basic_salary = basic_salary
        self.reward = reward
        self.net_salary = net_salary

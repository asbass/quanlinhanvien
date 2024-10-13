class Payroll:
    def __init__(self, Employee, dayoff=0, reward=0, punish=0, total=0):
        self.emp_id = Employee.emp_id
        self.name = Employee.name
        self.position = Employee.position
        self.dayoff = dayoff
        self.reward = reward
        self.punish = punish
        self.total = total
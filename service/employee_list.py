from enity.employee import Employee

class EmployeeList:
    def __init__(self):
        self.employees = []

    def add_employee(self, name, age, department, position, salary):
        new_employee = Employee(name, age, department, position, salary)
        self.employees.append(new_employee)

    def update_employee(self, index, name, age, department, position, salary):
        if 0 <= index < len(self.employees):
            self.employees[index].name = name
            self.employees[index].age = age
            self.employees[index].department = department
            self.employees[index].position = position
            self.employees[index].salary = salary

    def delete_employee(self, index):
        if 0 <= index < len(self.employees):
            del self.employees[index]

    def get_employees(self):
        return self.employees

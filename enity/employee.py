class Employee:
    _id_counter = 1

    def __init__(self, name, age, department, position, salary):
        self.emp_id = Employee._id_counter
        self.name = name
        self.age = age
        self.department = department
        self.position = position
        self.salary = salary
        Employee._id_counter += 1

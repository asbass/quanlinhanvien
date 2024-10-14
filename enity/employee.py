class Employee:
    _id_counter = 1

    def __init__(self, name, age, department, position):
        self.emp_id = Employee._id_counter
        self.name = name
        self.position = position
        self.age = age
        self.department = department
        
        Employee._id_counter += 1
    def __repr__(self):
        return f"Employee(ID: {self.emp_id}, Name: {self.name}, Age: {self.age}, Department: {self.department}, Position: {self.position})"
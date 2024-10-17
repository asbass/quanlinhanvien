import uuid

class Employee:
    def __init__(self, name, age, department, position):
        self.emp_id = uuid.uuid4()  # Tạo UUID cho emp_id
        self.name = name
        self.position = position
        self.age = age
        self.department = department

    def __repr__(self):
        return f"Employee(ID: {self.emp_id}, Name: {self.name}, Age: {self.age}, Department: {self.department}, Position: {self.position})"

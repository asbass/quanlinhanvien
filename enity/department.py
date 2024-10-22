import uuid

class Department:
    def __init__(self, name):
        self.dept_id = uuid.uuid4()  # Tạo UUID cho dept_id
        self.name = name
    def __repr__(self):
        return f"Department(ID: {self.dept_id}, Name: {self.name})"
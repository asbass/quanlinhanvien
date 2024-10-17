import uuid

class Position:
    def __init__(self, name, salary_multiplier):
        self.position_id = str(uuid.uuid4())  # Tạo UUID cho position_id và chuyển đổi thành chuỗi
        self.name = name
        self.salary_multiplier = salary_multiplier

    def __repr__(self):
        return (f"Position(ID: {self.position_id}, Name: {self.name}, "
                f"Salary Multiplier: {self.salary_multiplier})")
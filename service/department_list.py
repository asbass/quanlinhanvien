from enity.department import Department

class DepartmentList:
    def __init__(self):
        self.departments = []

    def add_department(self, name):
        new_department = Department(name)
        self.departments.append(new_department)

    def update_department(self, index, name):
        if 0 <= index < len(self.departments):
            self.departments[index].name = name

    def delete_department(self, index):
        if 0 <= index < len(self.departments):
            del self.departments[index]

    def get_departments(self):
        return self.departments

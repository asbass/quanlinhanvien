import csv
from enity.department import Department

class departmentList:
    def __init__(self, filename='department.csv'):
        self.filename = filename
        self.department = []
        self.load_to_csv()
    def add_department(self, name):
        new_department = Department(name)
        self.department.append(new_department)
        self.save_to_csv()
    def update_department(self, index, name):
        if 0 <=index < len(self.department):
            self.department[index].name = name
        self.save_to_csv()
    def del_department(self, index):
        if 0 <= index < len(self.department):
            del self.department[index]
        self.save_to_csv()
    def get_department(self):
        return self.department
    def save_to_csv(self):
        with open(self.filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["ID","Tên"])
            for dep in self.department:
                writer.writerow([dep.dept_id, dep.name])
    def load_to_csv(self):
        print("loading")
        try:
            with open(self.filename, mode="r", encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    dep = Department(row['Tên'])
                    self.department.append(dep)
                print('sucessfully')
        except FileNotFoundError:
            print("file not found")
        except KeyError as e:
            print(f"keyError: {e} - kiem tra ten cot")
        except Exception as e:
            print(f"error: {e}")
    
        
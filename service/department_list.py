import csv
from enity.department import Department

class departmentList:
    def __init__(self, filename='department.csv'):
        self.filename = filename
        self.department = []
        self.load_departments()
        
    def add_department(self, name,positions):
        new_department = Department(name,positions)
        self.department.append(new_department)
        self.save_to_csv()
    def update_department(self, index, name,positions):
        if 0 <=index < len(self.department):
            self.department[index].name = name
            self.department[index].positions = positions
        self.save_to_csv()
    def del_department(self, index):
        if 0 <= index < len(self.department):
            del self.department[index]
        self.save_to_csv()
    def get_department(self):
        return self.department
    def get_department_names(self):
        return [department.name for department in self.department]
    def save_to_csv(self):
        with open(self.filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["ID","Tên","Trưởng phòng"])
            for dep in self.department:
                writer.writerow([dep.dept_id, dep.name,dep.positions])
    def load_departments(self):
        print("Đang tải")
        try:
            with open(self.filename, mode="r", encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    dep = Department(row['Tên'], row['Trưởng phòng'])
                    self.department.append(dep)
                print('Thành Công')
        except FileNotFoundError:
            print("Không Tìm Thấy File")
        except KeyError as e:
            print(f"keyError: {e} - Kiểm tra tên cột")
        except Exception as e:
            print(f"error: {e}")
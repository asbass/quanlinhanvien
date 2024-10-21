import csv
from enity.Payroll import Payroll
from enity.employee import Employee
class PayrollList: 
    def __init__(self, filename='Payroll.csv'):
        self.filename = filename
        self.Payroll = []
        self.load_Payroll()
    
    def update_payroll(self, index, dayoff, reward, punish, total):
        if 0<= index < len(self.Payroll):
            self.Payroll[index].dayoff = dayoff
            self.Payroll[index].reward = reward
            self.Payroll[index].punish = punish
            self.Payroll[index].total = total
        self.save_to_csv()

    def save_to_csv(self):
        with open('payroll.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Tên', 'Vị trí', 'Tháng', 'Năm', 'Lương cơ bản', 'Thưởng', 'Ngày Nghỉ', 'Lương thực nhận'])

            for payroll in self.Payroll:
                writer.writerow([
                    payroll.emp_id,
                    payroll.name,  # Ghi tên nhân viên
                    payroll.position,  # Ghi vị trí nhân viên
                    payroll.month,
                    payroll.year,
                    payroll.basic_salary,
                    payroll.reward,
                    payroll.day_off,
                    payroll.net_salary
                ])

    def get_Payroll(self):
        return self.Payroll
    def load_Payroll(self):
        print("Đang tải danh sách lương từ tệp CSV...")  # Thông báo
        try:
            with open(self.filename, mode="r", encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    pay = Payroll(row['ID'], row['Tên'], row['Vị trí'], row['Tháng'], row['Năm'], row['Lương cơ bản'], row['Thưởng'], row['Ngày Nghỉ'], row['Lương thực nhận'])
                    self.Payroll.append(pay)
                print("Đã tải thành công danh sách lương.")  # Thông báo tải thành công
        except FileNotFoundError:
            print("Tệp không tồn tại, không làm gì cả.")  # Thông báo nếu tệp không tồn tại
        except KeyError as e:
            print(f"KeyError: {e} - Kiểm tra lại tên cột trong tệp CSV.")  # Thông báo lỗi nếu tên cột không đúng
        except Exception as e:
            print(f"Đã xảy ra lỗi: {e}")  # Thông báo lỗi khác    
    def add_payroll(self, employee: Employee, month, year, day_off, basic_salary, reward, net_salary):
        """Thêm một bảng lương mới vào danh sách."""
        new_payroll = Payroll(
            emp_id=employee.emp_id,
            name=employee.name,  # Lưu tên nhân viên
            position=employee.position,  # Lưu vị trí nhân viên
            month=month,
            year=year,
            day_off=day_off,
            basic_salary=basic_salary,
            reward=reward,
            net_salary=net_salary
        )
        print(f"ID: {employee.emp_id}, Name: {employee.name}, Position: {employee.position}, Month: {month}, Year: {year}, Basic Salary: {basic_salary}, Reward: {reward}, Day Off: {day_off}, Net Salary: {net_salary}")
        # Thêm bảng lương mới vào danh sách
        self.Payroll.append(new_payroll)
        self.save_to_csv()  # Gọi phương thức lưu vào file
        print("Bảng lương mới đã được thêm thành công!")

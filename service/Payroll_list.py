import csv
from enity.Payroll import Payroll

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
        with open(self.filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["ID","Tên","Vị Trí","Ngày Nghỉ","Thưởng","Phạt","Tổng"])
            for Pay in self.Payroll:
                writer.writerow([Pay.emp_id, Pay.name,Pay.position,Pay.dayoff,Pay.reward,Pay.punish,Pay.total,])

    def get_Payroll(self):
        return self.Payroll
    
    def load_Payroll(self):
        print('Đang tải//')
        try:
            with open(self.filename, mode="r", encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    pay = Payroll(row['ID'], row['Tên'],row['Vị Trí'], row['Ngày Nghỉ'],row['Thưởng'], row['Phạt'], row['Tổng'])
                    self.Payroll.append(pay)
                print('Thành Công//')
        except FileNotFoundError:
            print("Không Tìm Thấy File")
        except KeyError as e:
            print(f"keyError: {e} - Kiểm tra tên cột")
        except Exception as e:
            print(f"error: {e}")
        
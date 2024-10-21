from collections import defaultdict
from datetime import datetime
from enity.working_time import WokingTime
from service.employee_list import EmployeeList
import datetime
class WorkingTimeService:
    def __init__(self):
        self.working_time_list = []
        self.employee_list = EmployeeList()
    
    def add_working_time(self, emp_id, time, status, reason, typeOff, typeTime):
        new_working_time = WokingTime(emp_id, time, status, reason, typeOff, typeTime)
        self.working_time_list.append(new_working_time)  # Sửa từ self.working_time thành self.working_time_list
        print(self.working_time_list)
    
    def delete_working_time(self, index):
        if 0 <= index < len(self.working_time_list):
            del self.working_time_list[index]
    
    def update_working_time(self, index, emp_id=None, time=None, status=None, reason=None, typeOff=None, typeTime=None):
        if 0 <= index < len(self.working_time_list):  # Kiểm tra chỉ số hợp lệ
            if emp_id is not None:
                self.working_time_list[index].emp_id = emp_id
            if time is not None:
                self.working_time_list[index].time = time
            if status is not None:
                self.working_time_list[index].status = status
            if reason is not None:
                self.working_time_list[index].reason = reason
            if typeOff is not None:
                self.working_time_list[index].typeOff = typeOff
            if typeTime is not None:
                self.working_time_list[index].typeTime = typeTime
    
    def get_working_time(self, working_time_id):
        # Lấy thông tin của một mục làm việc theo ID
        for wt in self.working_time_list:
            if wt.working_time_id == working_time_id:
                return wt
        return None  # Trả về None nếu không tìm thấy

    def list_working_times(self):
        # Liệt kê tất cả các mục làm việc
        return self.working_time_list
    
    def list_working_time_by_year(self, year: int):
        # Tạo một dictionary để lưu tổng số ngày nghỉ cho từng nhân viên, từng tháng, và trạng thái OFF, OT, WFH
        result = defaultdict(lambda: {
            "months": {month: {"OFF": 0, "OT": 0, "WFH": 0} for month in range(1, 13)},
            "total": {"OFF": 0, "OT": 0, "WFH": 0}
        })

        for working_time in self.working_time_list:
            # Lọc theo năm (định dạng dd/mm/yyyy)
            work_year = datetime.datetime.strptime(working_time.time, '%d/%m/%Y').year
            if work_year == year:
                print(working_time.emp_id)
                emp_id = working_time.emp_id
                work_month = datetime.datetime.strptime(working_time.time, '%d/%m/%Y').month
                off_type = working_time.typeOff
                time_type = working_time.typeTime

                print(work_month)
                print(off_type)
                # Tính số ngày nghỉ dựa trên AM/PM/D
                if time_type in ["AM", "PM"]:
                    day_value = 0.5
                else:
                    day_value = 1

                print(day_value)
                # Cộng dồn số ngày nghỉ cho từng trạng thái OFF, OT, WFH
                result[emp_id]["months"][work_month][off_type] += day_value
                result[emp_id]["total"][off_type] += day_value

                print(f"Result after update: {result[emp_id]['months'][work_month]}")
                print(f"Result after update: {result[emp_id]["total"][off_type]}")
                print(emp_id)

        # Kiểm tra xem nhân viên có trong kết quả không
        for employee in self.employee_list.get_employees():
            emp_id = employee.emp_id 
            if emp_id not in result:
                result[emp_id]  # Thêm một mục mặc định cho nhân viên không có dữ liệu

        # In ra thông tin cho từng nhân viên
        for employee in self.employee_list.get_employees():
            emp_id = employee.emp_id 
            print(f"Employee: {employee.name}")
            print("Monthly totals:")
            for month, totals in result[emp_id]["months"].items():
                print(f" Month {month}: {totals}")
            print("Yearly total:", result[emp_id]["total"])
            print("\n")

        return result

    def get_off_days_by_employee(self, emp_id):
        # Lọc danh sách ngày nghỉ theo emp_id
        return [wt.time for wt in self.working_time_list if wt.emp_id == emp_id]

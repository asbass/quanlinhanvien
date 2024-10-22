from collections import defaultdict
from datetime import datetime
from enity.working_time import WorkingTime
from service.connect_sql import DatabaseConnection
from service.department_list import departmentList
from service.employee_list import EmployeeList
import datetime
import uuid
class WorkingTimeService:
    def __init__(self):
        self.db = DatabaseConnection()
        self.working_time_list = []
        self.db.connect()
        self.load_working_time_from_db()
        # self.employee_list = EmployeeList()
        # self.department_list = departmentList()
    
    def load_working_time_from_db(self):
        """Load working time from the database."""
        query = "SELECT * FROM workingtime"
        rows = self.db.fetch_all(query)
        for row in rows:
            workingTime = WorkingTime(row['working_time_id'], row['emp_id'], row['time'], row['status'], row['reason'],row['type_off'], row['type_time'])
            print(workingTime)
            self.working_time_list.append(workingTime)

    def add_working_time(self, emp_id, time, status, reason, typeOff, typeTime):
        date = datetime.datetime.strptime(time, '%d/%m/%Y')
        date_time = datetime.datetime(date.year, date.month, date.day, 8, 0, 0)
        format_date = date_time.strftime('%Y-%m-%d %H:%M:%S')
        new_working_time = WorkingTime(uuid.uuid4(), emp_id, format_date, status, reason, typeOff, typeTime)
        self.working_time_list.append(new_working_time) 
        query = """
            INSERT INTO workingtime (working_time_id, emp_id, reason, status, time, type_off, type_time) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        data = (str(new_working_time.working_time_id),str(new_working_time.emp_id), new_working_time.reason, new_working_time.status, format_date, new_working_time.type_off, new_working_time.type_time)
        self.db.execute_query(query, data)
        print(self.working_time_list)
    
    def delete_working_time(self, working_time_id):
        working_time_id_str = str(working_time_id)  # Chuyển đổi emp_id sang chuỗi nếu cần

        working_time_exist = self.get_working_time_by_id(working_time_id_str)
        if not working_time_exist:
            print("No working time found with working_time_id_str:", working_time_id_str)
            return
    
        # Truy vấn xóa
        query = "DELETE FROM workingtime WHERE working_time_id = %s"
        try:
            self.db.execute_query(query, (working_time_id_str,))
            print(f"Đã xóa thời gian làm việc có working_time_id: {working_time_id_str} thành công.")

            # Cập nhật danh sách nhân viên trong bộ nhớ
            self.working_time_list = [working_time for working_time in self.working_time_list if str(working_time.working_time_id) != working_time_id_str]
        except Exception as e:
            print("Lỗi khi xóa thời gian làm việc:", e)
        
    def get_working_time(self):
        # Lấy danh sách các phòng ban
        query = "SELECT * FROM workingtime"
        data = self.db.fetch_all(query)
        return [WorkingTime(**working_time) for working_time in data]
    
    def update_working_time(self, working_time_id, emp_id=None, time=None, status=None, reason=None, typeOff=None, typeTime=None):
        working_time_id_str = str(working_time_id)
        # Debugging: Print the current employee IDs
        print("Current working time IDs:", self.get_working_time_ids())

        working_time = self.get_working_time_by_id(working_time_id_str)
        if not working_time:
            print("No working time found with working_time_id_str:", working_time_id_str)
            return

        # Update employee attributes
        working_time.emp_id = emp_id
        working_time.time = time
        working_time.status = status
        working_time.reason = reason
        working_time.type_off = typeOff
        working_time.type_time = typeTime
        date = datetime.datetime.strptime(time, '%d/%m/%Y')
        date_time = datetime.datetime(date.year, date.month, date.day, 8, 0, 0)
        format_date = date_time.strftime('%Y-%m-%d %H:%M:%S')
        # Update the employee in the database
        query = """
            UPDATE workingtime
            SET emp_id = %s, time = %s, status = %s, reason = %s, type_off = %s, type_time = %s
            WHERE working_time_id = %s
        """
        data = (emp_id, format_date, status, reason, typeOff, typeTime, working_time_id_str)

        try:
            self.db.execute_query(query, data)
            print(f"Working time {working_time_id_str} updated successfully.")
        except Exception as e:
            print("Error updating Working time:", e)

    def get_working_time_by_id(self, emp_id):
        """Retrieve working time information by ID from the database."""
        query = "SELECT * FROM workingtime WHERE working_time_id = %s"
        result = self.db.fetch_one(query, (emp_id,))  # Fetch a single record

        if result:
            return WorkingTime(result['working_time_id'],result['emp_id'], result['time'],result['status'], result['reason'],result['type_off'], result['type_time'])
        
        return None
    
    def get_working_time_ids(self):
        """Retrieve working time IDs from the database."""
        query = "SELECT working_time_id FROM workingtime"
        results = self.db.fetch_all(query)  # Assuming this returns a list of dictionaries

        # Extract IDs from the results
        return [result['working_time_id'] for result in results]
    # def get_working_time(self, working_time_id):
    #     # Lấy thông tin của một mục làm việc theo ID
    #     for wt in self.working_time_list:
    #         if wt.working_time_id == working_time_id:
    #             return wt
    #     return None  # Trả về None nếu không tìm thấy

    # def list_working_times(self):
    #     # Liệt kê tất cả các mục làm việc
    #     return self.working_time_list
    
    # def list_working_time_by_year(self, year: int):
    #     # Tạo một dictionary để lưu tổng số ngày nghỉ cho từng nhân viên, từng tháng, và trạng thái OFF, OT, WFH
    #     result = defaultdict(lambda: {
    #         "months": {month: {"OFF": 0, "OT": 0, "WFH": 0} for month in range(1, 13)},
    #         "total": {"OFF": 0, "OT": 0, "WFH": 0}
    #     })

    #     for working_time in self.working_time_list:
    #         # Lọc theo năm (định dạng dd/mm/yyyy)
    #         work_year = datetime.datetime.strptime(working_time.time, '%d/%m/%Y').year
    #         if work_year == year:
    #             print(working_time.emp_id)
    #             emp_id = working_time.emp_id
    #             work_month = datetime.datetime.strptime(working_time.time, '%d/%m/%Y').month
    #             off_type = working_time.typeOff
    #             time_type = working_time.typeTime

    #             print(work_month)
    #             print(off_type)
    #             # Tính số ngày nghỉ dựa trên AM/PM/D
    #             if time_type in ["AM", "PM"]:
    #                 day_value = 0.5
    #             else:
    #                 day_value = 1

    #             print(day_value)
    #             # Cộng dồn số ngày nghỉ cho từng trạng thái OFF, OT, WFH
    #             result[emp_id]["months"][work_month][off_type] += day_value
    #             result[emp_id]["total"][off_type] += day_value

    #             print(f"Result after update: {result[emp_id]['months'][work_month]}")
    #             print(f"Result after update: {result[emp_id]["total"][off_type]}")
    #             print(emp_id)

    #     # Kiểm tra xem nhân viên có trong kết quả không
    #     for employee in self.employee_list.get_employees():
    #         emp_id = employee.emp_id 
    #         if emp_id not in result:
    #             result[emp_id]  # Thêm một mục mặc định cho nhân viên không có dữ liệu

    #     # In ra thông tin cho từng nhân viên
    #     for employee in self.employee_list.get_employees():
    #         emp_id = employee.emp_id 
    #         print(f"Employee: {employee.name}")
    #         print("Monthly totals:")
    #         for month, totals in result[emp_id]["months"].items():
    #             print(f" Month {month}: {totals}")
    #         print("Yearly total:", result[emp_id]["total"])
    #         print("\n")

    #     return result

    # def get_off_days_by_employee(self, emp_id):
    #     # Lọc danh sách ngày nghỉ theo emp_id
    #     return [wt.time for wt in self.working_time_list if wt.emp_id == emp_id]

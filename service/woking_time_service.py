from enity.working_time import WokingTime
from service import employee_list
from service.connect_sql import DatabaseConnection
class WorkingTimeService:
    def __init__(self):
        self.working_time_list = []
        self.employee_list = employee_list
        self.db = DatabaseConnection()  # Khởi tạo kết nối với cơ sở dữ liệu
        self.db.connect()  # Connect to the database
        
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
    def get_days_off(self, emp_id, month, year):
        query = """
            SELECT COUNT(*) AS days_off
            FROM WorkingTime
            WHERE emp_id = %s 
            AND MONTH(time) = %s 
            AND YEAR(time) = %s
        """
        result = self.db.fetch_one(query, (emp_id, month, year))  # Truyền đủ tham số
        
        # Trả về số ngày nghỉ, sử dụng 'days_off' thay vì 'name'
        return result['days_off'] if result else 0  # Trả về 0 nếu không có kết quả

    def list_working_times(self):
        # Liệt kê tất cả các mục làm việc
        return self.working_time_list
    def get_off_days_by_employee(self, emp_id):
        # Lọc danh sách ngày nghỉ theo emp_id
        return [wt.time for wt in self.working_time_list if wt.emp_id == emp_id]
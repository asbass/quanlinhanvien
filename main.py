import tkinter as tk
from tkinter import ttk
from template.app_employee import EmployeeApp
from template.app_department import DepartmentApp
from template.app_working_time import WokingTimeApp
from template.app_payroll import PayrollApp
from template.app_positions import PositonsApp
from service.employee_list import EmployeeList
class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quản Lý Nhân Viên và Phòng Ban")
        self.geometry("1300x800")
        self.employee_list = EmployeeList()
        # Tạo tab control
        self.tab_control = ttk.Notebook(self)

        # Khởi tạo các tab
        self.employee_tab = EmployeeApp(self.tab_control)  # Khởi tạo EmployeeApp trước
        self.department_tab = DepartmentApp(self.tab_control)
        self.positon_tab = PositonsApp(self.tab_control)
        self.Payroll_tab = PayrollApp(self.tab_control)
        self.WokingTimeApp_tab = WokingTimeApp(self.tab_control)
        # Thêm các tab vào tab_control
        self.tab_control.add(self.employee_tab, text="Nhân Viên")
        self.tab_control.add(self.department_tab, text="Phòng Ban")
        self.tab_control.add(self.Payroll_tab, text="Bảng lương")
        self.tab_control.add(self.positon_tab,text ="chức vụ")
        self.tab_control.add(self.WokingTimeApp_tab,text ="ngày nghỉ")
        # Đặt tab_control vào giao diện
        self.tab_control.pack(expand=1, fill="both")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)


    def on_closing(self):
        # Đóng kết nối trong các tab
        self.department_tab.close_connection()  # Đóng kết nối trong DepartmentApp
        self.employee_tab.close_connection()    # Nếu EmployeeApp cũng cần
        self.positon_tab.close_connection()
        # self.working_time_tab.close_connection() # Nếu WokingTimeApp cũng cần
        self.Payroll_tab.close_connection()     # Nếu PayrollApp cũng cần
        self.destroy()                          # Đóng ứng dụng

    def update_employee_list_in_employee_app(self):
        employee_list = self.employee_tab.employee_list.get_employees()  # Truy cập từ department_tab
        print(f"Employee list in update_employee_list_in_employee_app: {employee_list}")  # Debug
        self.Payroll_tab.update_employee_list(employee_list)
        self.Payroll_tab.update_employee_position()
        # self.Payroll_tab.load_employee_list()
    # def update_employee_list_in_employee_app(self):
    #     # Lấy danh sách nhân viên từ EmployeeApp
    #     employee_list = self.employee_tab.employee_list.get_employees()  
    #     # Cập nhật danh sách nhân viên trong PayrollApp
    #     # self.Payroll_tab.update_employee_list(employee_list)
    #     self.Payroll_tab.load_employee_list()
    # def update_employee_list_in_employee_app(self):
    #     # Lấy danh sách nhân viên từ EmployeeApp        
    #     # Cập nhật danh sách nhân viên trong PayrollApp
    #     self.Payroll_tab.update_employee_list()
if __name__ == "__main__":
    app = MainApp()
    
    app.mainloop()

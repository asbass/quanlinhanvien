import tkinter as tk
from tkinter import ttk
from template.app_employee import EmployeeApp
from template.app_department import DepartmentApp
from template.app_working_time import WokingTimeApp
from template.app_payroll import PayrollApp
from service.employee_list import EmployeeList
from template.app_positions import PositonsApp
class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quản Lý Nhân Viên và Phòng Ban")
        self.geometry("1300x800")
        self.ss = EmployeeList()

        # Tạo tab control
        self.tab_control = ttk.Notebook(self)

        # Khởi tạo các tab
        self.employee_tab = EmployeeApp(self.tab_control)  # Khởi tạo EmployeeApp trước
        self.department_tab = DepartmentApp(self.tab_control)
        self.working_time_tab = WokingTimeApp(self.tab_control)
        self.Payroll_tab = PayrollApp(self.tab_control)
        self.Position_tab = PositonsApp(self.tab_control)
        # Thêm các tab vào tab_control
        self.tab_control.add(self.employee_tab, text="Nhân Viên")
        self.tab_control.add(self.department_tab, text="Phòng Ban")
        self.tab_control.add(self.working_time_tab, text="Thời gian làm việc")
        self.tab_control.add(self.Payroll_tab, text="Bảng lương")
        self.tab_control.add(self.Position_tab, text="Chức Vụ")
        # Đặt tab_control vào giao diện
        self.tab_control.pack(expand=1, fill="both")

    def update_employee_list_in_employee_app(self):
        employee_list = self.employee_tab.employee_list.get_employee_names()  # Truy cập từ department_tab
        self.Payroll_tab.update_employee_list(employee_list)
    def update_department_list_in_department_app(self):
        # Lấy danh sách phòng ban và cập nhật danh sách
        department_list = self.department_tab.department_list.get_department_names()
        self.employee_tab.update_department_list(department_list)
    def update_Postion_list_in_position_app(self):
        postion_list = self.Position_tab.position_list.get_position_names()
        self.employee_tab.update_positon_list(postion_list)
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()

import tkinter as tk
from tkinter import ttk
from template.app_employee import EmployeeApp
from template.app_department import DepartmentApp
from template.app_payroll import PayrollApp

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quản Lý Nhân Viên và Phòng Ban")
        self.geometry("1300x800")

        # Tạo tab control
        self.tab_control = ttk.Notebook(self)
        self.department_tab = DepartmentApp(self.tab_control)
        self.employee_tab = EmployeeApp(self.tab_control)
        self.Payroll_tab = PayrollApp(self.tab_control)
        self.tab_control.add(self.employee_tab, text="Nhân Viên")
        self.tab_control.add(self.department_tab, text="Phòng Ban")
        self.tab_control.add(self.Payroll_tab, text="Bảng lương")
        self.tab_control.pack(expand=1, fill="both")
    def update_department_list_in_employee_app(self):
        department_list = self.department_tab.department_list.get_department()  # Truy cập từ department_tab
        self.employee_tab.update_department_list(department_list)
    def update_employee_list_in_employee_app(self):
        employee_list = self.employee_tab.employee_list.get_employees()  # Truy cập từ department_tab
        self.department_tab.update_employee_list(employee_list)   
        self.Payroll_tab.update_employee_list(employee_list)
        self.Payroll_tab.on_employee_selected(employee_list)
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()

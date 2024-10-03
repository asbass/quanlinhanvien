import tkinter as tk
from tkinter import ttk
from template.app_employee import EmployeeApp
from template.app_department import DepartmentApp

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quản Lý Nhân Viên và Phòng Ban")
        self.geometry("800x600")

        # Tạo tab control
        self.tab_control = ttk.Notebook(self)
        self.employee_tab = EmployeeApp(self.tab_control)
        self.department_tab = DepartmentApp(self.tab_control)

        self.tab_control.add(self.employee_tab, text="Nhân Viên")
        self.tab_control.add(self.department_tab, text="Phòng Ban")
        self.tab_control.pack(expand=1, fill="both")

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()

import tkinter as tk
from tkinter import messagebox, ttk
from service.woking_time_service import WorkingTimeService
from service.employee_list import EmployeeList
import datetime
from tkcalendar import Calendar
import os
from PIL import Image, ImageTk
from template.app_dashboard_woking_time_tab import DashboardWokingTime
from template.app_manager_working_time_tab import ManagerWorkingTimeTab

class WokingTimeApp(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.working_time = WorkingTimeService()
        self.employee_list = EmployeeList() 
        label = tk.Label(self, text="Quản lý thời gian làm việc")
        label.pack(padx=5, pady=5)

        # Tạo notebook cho các tab
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        # Tạo các tab từ các class khác
        self.tab1 = DashboardWokingTime(self.notebook)
        self.tab2 = ManagerWorkingTimeTab(self.notebook)

        # Thêm các tab vào notebook
        self.notebook.add(self.tab1, text="Bảng điều khiển")
        self.notebook.add(self.tab2, text="Thời gian làm việc")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
from service.employee_list import EmployeeList
from service.Payroll_list import PayrollList
from service.connect_sql import DatabaseConnection

class EmployeeCharts(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.employee_list = EmployeeList()
        self.payroll_list = PayrollList()
        self.db = DatabaseConnection()
        self.db.connect()  # Kết nối với cơ sở dữ liệu
        self.create_widgets()

    def create_widgets(self):
        """Tạo các widget cho giao diện."""
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(pady=20, padx=20)

        self.create_chart_frames()

        # Tạo các biểu đồ
        self.create_employee_count_by_department_chart()
        self.create_total_salary_by_department_chart()
        self.create_salary_trend_chart()
        self.create_employee_trend_chart()

    def create_chart_frames(self):
        """Tạo các frame cho biểu đồ và chia đều chúng trong frame chính."""
        self.bar_chart_frame = tk.Frame(self.main_frame)
        self.bar_chart_frame.grid(row=0, column=0, padx=10, pady=5, sticky='nsew')  
        self.main_frame.grid_columnconfigure(0, weight=1)  

        self.line_chart_frame = tk.Frame(self.main_frame)
        self.line_chart_frame.grid(row=0, column=1, padx=10, pady=5, sticky='nsew')  
        self.main_frame.grid_columnconfigure(1, weight=1)  


        # Đặt trọng số cho hàng để các frame có thể mở rộng cùng nhau
        self.main_frame.grid_rowconfigure(0, weight=1)

    def create_employee_count_by_department_chart(self):
        """Biểu đồ cột: Số Nhân Viên Theo Phòng Ban."""
        result = self.employee_list.employee_count_by_department_chart()
        if result:
            departments = [row['department'] for row in result]
            counts = [row['count'] for row in result]

            fig, ax = plt.subplots(figsize=(4, 2.5))  # Kích thước nhỏ hơn
            ax.bar(departments, counts, color='skyblue')
            ax.set_xlabel('Phòng Ban')
            ax.set_ylabel('Số Nhân Viên')
            ax.set_title('Số Nhân Viên Theo Phòng Ban')

            plt.tight_layout()  # Tự động điều chỉnh kích thước biểu đồ
            self.add_canvas_to_frame(fig, self.bar_chart_frame)

    def create_total_salary_by_department_chart(self):
        """Biểu đồ cột: Tổng Lương Theo Phòng Ban."""
        result = self.employee_list.total_salary_by_department_chart()
        if result:
            departments = [row['name'] for row in result]
            total_salaries = [row['total_salary'] for row in result]

            fig, ax = plt.subplots(figsize=(4, 2.5))  # Kích thước nhỏ hơn
            ax.bar(departments, total_salaries, color='orange')
            ax.set_xlabel('Phòng Ban')
            ax.set_ylabel('Tổng Lương')
            ax.set_title('Tổng Lương Theo Phòng Ban')

            plt.tight_layout()  # Tự động điều chỉnh kích thước biểu đồ
            self.add_canvas_to_frame(fig, self.bar_chart_frame)

    def create_salary_trend_chart(self):
        """Biểu đồ đường: Thay Đổi Lương Theo Thời Gian."""
        result = self.payroll_list.salary_trend_chart()
        if result:
            months = [row['month'] for row in result]
            avg_salaries = [row['avg_salary'] for row in result]

            fig, ax = plt.subplots(figsize=(4, 2.5))  # Kích thước nhỏ hơn
            ax.plot(months, avg_salaries, marker='o', color='green')
            ax.set_xlabel('Tháng')
            ax.set_ylabel('Lương Trung Bình')
            ax.set_title('Thay Đổi Lương Theo Thời Gian')

            plt.tight_layout()  # Tự động điều chỉnh kích thước biểu đồ
            self.add_canvas_to_frame(fig, self.line_chart_frame)

    def create_employee_trend_chart(self):
        """Biểu đồ đường: Thay Đổi Số Nhân Viên Theo Thời Gian."""
        result = self.payroll_list.employee_trend_chart()
        if result:
            months = [row['month'] for row in result]
            counts = [row['count'] for row in result]

            fig, ax = plt.subplots(figsize=(4, 2.5))  # Kích thước nhỏ hơn
            ax.plot(months, counts, marker='o', color='blue')
            ax.set_xlabel('Tháng')
            ax.set_ylabel('Số Nhân Viên')
            ax.set_title('Thay Đổi Số Nhân Viên Theo Thời Gian')

            plt.tight_layout()  # Tự động điều chỉnh kích thước biểu đồ
            self.add_canvas_to_frame(fig, self.line_chart_frame)

    def add_canvas_to_frame(self, fig, frame):
        """Thêm canvas biểu đồ vào frame."""
        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        canvas.draw()

    def close_connection(self):
        """Đóng kết nối với cơ sở dữ liệu."""
        self.employee_list.close_connection()
        self.payroll_list.close_connection()

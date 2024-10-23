import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
from service.employee_list import EmployeeList
from service.Payroll_list import PayrollList
from service.connect_sql import DatabaseConnection
import mplcursors  # Thêm dòng này

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
        # Tạo một canvas cho việc cuộn
        self.canvas = tk.Canvas(self)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        # Thiết lập canvas và frame có thể cuộn
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Đặt layout cho canvas và scrollbar
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.create_chart_frames()

        # Tạo các biểu đồ
        self.create_employee_count_by_department_chart()
        self.create_total_salary_by_department_chart()
        # self.create_salary_trend_chart()
        # self.create_employee_trend_chart()

    def create_chart_frames(self):
        """Tạo các frame cho biểu đồ và chia đều chúng trong frame chính."""    
        # Frame cho biểu đồ cột số nhân viên và tổng lương
        self.bar_chart_frame_1 = tk.Frame(self.scrollable_frame)
        self.bar_chart_frame_1.grid(row=0, column=0, padx=10, pady=5, sticky='nsew')  
        self.scrollable_frame.grid_columnconfigure(0, weight=1)  # Chia cột đều

        self.bar_chart_frame_2 = tk.Frame(self.scrollable_frame)
        self.bar_chart_frame_2.grid(row=0, column=1, padx=10, pady=5, sticky='nsew')  
        self.scrollable_frame.grid_columnconfigure(1, weight=1)  # Chia cột đều

        # Frame cho biểu đồ đường
        self.line_chart_frame_1 = tk.Frame(self.scrollable_frame)
        self.line_chart_frame_1.grid(row=1, column=0, padx=10, pady=5, sticky='nsew')
        self.scrollable_frame.grid_columnconfigure(0, weight=1)  # Đặt trọng số cột cho biểu đồ đường

        self.line_chart_frame_2 = tk.Frame(self.scrollable_frame)
        self.line_chart_frame_2.grid(row=1, column=1, padx=10, pady=5, sticky='nsew')
        self.scrollable_frame.grid_columnconfigure(1, weight=1)  # Đặt trọng số cột cho biểu đồ đường

        # Đặt trọng số cho hàng để các frame có thể mở rộng cùng nhau
        self.scrollable_frame.grid_rowconfigure(0, weight=1)  # Đặt trọng số cho hàng 0 (biểu đồ cột)
        self.scrollable_frame.grid_rowconfigure(1, weight=1)  # Đặt trọng số cho hàng 1 (biểu đồ đường)

    def create_employee_count_by_department_chart(self):
        """Biểu đồ cột: Số Nhân Viên Theo Phòng Ban."""
        result = self.employee_list.employee_count_by_department_chart()
        if result:
            departments = [row['department'] for row in result]
            counts = [row['count'] for row in result]

            fig, ax = plt.subplots(figsize=(6, 5))  # Kích thước nhỏ hơn
            bars = ax.bar(departments, counts, color='skyblue')  # Gán đối tượng thanh cho biến 'bars'
            ax.set_xlabel('Phòng Ban')
            ax.set_ylabel('Số Nhân Viên')
            ax.set_title('Số Nhân Viên Theo Phòng Ban')
            ax.set_xticks(range(len(departments)))  # Thiết lập vị trí tick
            ax.set_xticklabels(departments, rotation=45, ha='right', fontsize=5)
            ax.xaxis.set_visible(False)  # Ẩn trục hoành


            # Thêm tính năng hiển thị tooltip khi di chuột vào cột
            cursor = mplcursors.cursor(bars, hover=True)
            cursor.connect("add", lambda sel: sel.annotation.set_text(departments[sel.index]))
            plt.tight_layout()  # Tự động điều chỉnh kích thước biểu đồ
            self.add_canvas_to_frame(fig, self.bar_chart_frame_1)  # Thêm vào frame cột 1


    def create_total_salary_by_department_chart(self):
        """Biểu đồ cột: Tổng Lương Theo Phòng Ban."""
        result = self.employee_list.total_salary_by_department_chart()
        if result:
            departments = [row['name'] for row in result]
            total_salaries = [row['total_salary'] for row in result]

            fig, ax = plt.subplots(figsize=(6, 5))  # Kích thước nhỏ hơn
            bars =ax.bar(departments, total_salaries, color='orange')
            ax.set_xlabel('Phòng Ban')
            ax.set_ylabel('Tổng Lương')
            ax.set_title('Tổng Lương Theo Phòng Ban')
            ax.set_xticks(range(len(departments)))  # Thiết lập vị trí tick
            ax.set_xticklabels(departments, rotation=45, ha='right', fontsize=5)
            ax.xaxis.set_visible(False)  # Ẩn trục hoành
            # Thêm tính năng hiển thị tooltip khi di chuột vào cột
            cursor = mplcursors.cursor(bars, hover=True)
            cursor.connect("add", lambda sel: sel.annotation.set_text(departments[sel.index]))
            plt.tight_layout()  # Tự động điều chỉnh kích thước biểu đồ
            self.add_canvas_to_frame(fig, self.bar_chart_frame_2)  # Thêm vào frame cột 2


    # def create_salary_trend_chart(self):
    #     """Biểu đồ đường: Thay Đổi Lương Theo Thời Gian."""
    #     result = self.payroll_list.salary_trend_chart()
    #     if result:
    #         months = [row['month'] for row in result]
    #         avg_salaries = [row['avg_salary'] for row in result]

    #         fig, ax = plt.subplots(figsize=(6, 5))  # Kích thước nhỏ hơn
    #         ax.plot(months, avg_salaries, marker='o', color='green')
    #         ax.set_xlabel('Tháng')
    #         ax.set_ylabel('Lương Trung Bình')
    #         ax.set_title('Thay Đổi Lương Theo Thời Gian')

    #         plt.tight_layout()  # Tự động điều chỉnh kích thước biểu đồ
    #         self.add_canvas_to_frame(fig, self.line_chart_frame_1)  # Thêm vào frame hàng 1 cột 1


    # def create_employee_trend_chart(self):
    #     """Biểu đồ đường: Thay Đổi Số Nhân Viên Theo Thời Gian."""
    #     result = self.payroll_list.employee_trend_chart()
    #     if result:
    #         months = [row['month'] for row in result]
    #         counts = [row['count'] for row in result]

    #         fig, ax = plt.subplots(figsize=(6, 5))  # Kích thước nhỏ hơn
    #         ax.plot(months, counts, marker='o', color='blue')
    #         ax.set_xlabel('Tháng')
    #         ax.set_ylabel('Số Nhân Viên')
    #         ax.set_title('Thay Đổi Số Nhân Viên Theo Thời Gian')

    #         plt.tight_layout()  # Tự động điều chỉnh kích thước biểu đồ
    #         self.add_canvas_to_frame(fig, self.line_chart_frame_2)

    def add_canvas_to_frame(self, fig, frame):
        """Thêm canvas biểu đồ vào frame."""
        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        canvas.draw()

    def close_connection(self):
        """Đóng kết nối với cơ sở dữ liệu."""
        self.employee_list.close_connection()
        self.payroll_list.close_connection()
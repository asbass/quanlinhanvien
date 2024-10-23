import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
from service.employee_list import EmployeeList
from service.Payroll_list import PayrollList
from service.connect_sql import DatabaseConnection
import mplcursors  # Thêm dòng này
from decimal import Decimal

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
        self.create_highest_salary_treeview()
        self.create_statistics_treeview()
        # Thêm label cho nhân viên có lương cao nhất theo phòng ban

        # Tạo treeview cho nhân viên có lương cao nhất
        self.create_chart_frames()

        # Tạo các biểu đồ
        self.create_employee_count_by_department_chart()
        self.create_total_salary_by_department_chart()
        # self.create_salary_trend_chart()
        # self.create_employee_trend_chart()
    def create_statistics_treeview(self):
        """Tạo Treeview để hiển thị thống kê."""
        self.statistics_frame = tk.Frame(self.scrollable_frame)
        self.statistics_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky='nsew')

        # Tạo Treeview
        self.statistics_treeview = ttk.Treeview(self.statistics_frame, columns=('Statistic', 'Value'), show='headings')
        self.statistics_treeview.heading('Statistic', text='Thống kê')
        self.statistics_treeview.heading('Value', text='Giá trị')
        
        # Thay đổi kích thước cột
        self.statistics_treeview.column('Statistic', anchor='center', width=200)
        self.statistics_treeview.column('Value', anchor='center', width=100)
        # Thêm Treeview vào frame
        self.statistics_treeview.pack(fill=tk.BOTH, expand=True)
        # Gọi hàm để cập nhật dữ liệu thống kê
        self.update_statistics_treeview()
    def update_statistics_treeview(self):
        """Cập nhật dữ liệu vào Treeview thống kê."""
        # Xóa dữ liệu cũ
        for row in self.statistics_treeview.get_children():
            self.statistics_treeview.delete(row)

        # Tổng tất cả phòng, tổng tất cả nhân viên
        total_departments = self.employee_list.get_total_departments()
        self.statistics_treeview.insert('', 'end', values=('Tổng số phòng', total_departments['total_departments']))

        total_employees = self.employee_list.get_total_employees()
        self.statistics_treeview.insert('', 'end', values=('Tổng số nhân viên', total_employees['total_employees']))
        # Nhân viên có lương cao nhất
        highest_salary = self.employee_list.get_highest_salary()
        if highest_salary:
            # Lấy thông tin từ từ điển
            name = highest_salary['name']  # Lấy tên
            salary = highest_salary['salary']  # Lấy lương

            print(f"Name: {name}, Salary before conversion: {salary}")

            # Kiểm tra và chuyển đổi kiểu dữ liệu salary nếu cần
            if isinstance(salary, str):
                try:
                    salary = float(salary)
                except ValueError:
                    print(f"Cannot convert salary: {salary}")
                    salary = 0.0
            elif isinstance(salary, Decimal):
                salary = float(salary)
            elif not isinstance(salary, (int, float)):
                print(f"Unexpected type for salary: {type(salary)}")
                salary = 0.0

            self.statistics_treeview.insert('', 'end', values=('Nhân viên có lương cao nhất', f"Tên: {name}, Lương: {salary:.2f}"))
        else:
            self.statistics_treeview.insert('', 'end', values=('Nhân viên có lương cao nhất', 'Không có dữ liệu'))

    def create_highest_salary_treeview(self):
        self.highest_salary_frame = tk.Frame(self.scrollable_frame)
        self.highest_salary_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky='nsew')
            # Tiêu đề cho Treeview
        title_label = tk.Label(self.highest_salary_frame, text="Nhân viên có lương cao nhất theo phòng ban")
        title_label.pack(pady=(0, 5))  # Thêm khoảng cách bên dưới tiêu đề
        # Tạo Treeview
        self.highest_salary_treeview = ttk.Treeview(self.highest_salary_frame, columns=('Employee', 'Department', 'Salary'), show='headings')
        self.highest_salary_treeview.heading('Employee', text='Nhân viên')
        self.highest_salary_treeview.heading('Department', text='Phòng ban')
        self.highest_salary_treeview.heading('Salary', text='Lương')

        # Thay đổi kích thước cột
        self.highest_salary_treeview.column('Employee', anchor='center', width=200)
        self.highest_salary_treeview.column('Department', anchor='center', width=150)
        self.highest_salary_treeview.column('Salary', anchor='center', width=100)

        # Thêm Treeview vào frame
        self.highest_salary_treeview.pack(fill=tk.BOTH, expand=True)
        self.update_highest_salary_treeview()
    def update_highest_salary_treeview(self):
        """Cập nhật Treeview với thông tin về nhân viên có lương cao nhất trong phòng ban."""
        self.highest_salary_treeview.delete(*self.highest_salary_treeview.get_children())
        highest_salary_by_department = self.employee_list.get_highest_salary_by_department()
        if highest_salary_by_department:
            for emp in highest_salary_by_department:
                formatted_salary = f"{emp['salary']:,.0f} VND"
                self.highest_salary_treeview.insert('', 'end', values=(emp['name'], emp['department_name'],formatted_salary))
        else:
            self.highest_salary_treeview.insert('', 'end', values=('Không có dữ liệu', '', ''))


    def create_chart_frames(self):
        # Frame cho biểu đồ cột số nhân viên và tổng lương
        self.bar_chart_frame_1 = tk.Frame(self.scrollable_frame)
        self.bar_chart_frame_1.grid(row=2, column=0, padx=10, pady=5, sticky='nsew')  
        self.scrollable_frame.grid_columnconfigure(0, weight=1)  # Chia cột đều

        self.bar_chart_frame_2 = tk.Frame(self.scrollable_frame)
        self.bar_chart_frame_2.grid(row=2, column=1, padx=10, pady=5, sticky='nsew')  
        self.scrollable_frame.grid_columnconfigure(1, weight=1)  # Chia cột đều

        # # Frame cho biểu đồ đường
        # self.line_chart_frame_1 = tk.Frame(self.scrollable_frame)
        # self.line_chart_frame_1.grid(row=4, column=0, padx=10, pady=5, sticky='nsew')
        # self.scrollable_frame.grid_columnconfigure(0, weight=1)  # Đặt trọng số cột cho biểu đồ đường

        # self.line_chart_frame_2 = tk.Frame(self.scrollable_frame)
        # self.line_chart_frame_2.grid(row=4, column=1, padx=10, pady=5, sticky='nsew')
        # self.scrollable_frame.grid_columnconfigure(1, weight=1)  # Đặt trọng số cột cho biểu đồ đường

        # Đặt trọng số cho hàng để các frame có thể mở rộng cùng nhau
        self.scrollable_frame.grid_rowconfigure(3, weight=1)  # Đặt trọng số cho hàng 0 (biểu đồ cột)
        # self.scrollable_frame.grid_rowconfigure(1, weight=1)  # Đặt trọng số cho hàng 1 (biểu đồ đường)

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
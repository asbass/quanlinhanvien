import datetime
from tkinter import ttk
from tkcalendar import Calendar
import os
from PIL import Image, ImageTk
import tkinter as tk
from service.employee_list import EmployeeList
from service.woking_time_service import WorkingTimeService

class DashboardWokingTime(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.working_time = WorkingTimeService()
        self.employee_list = EmployeeList() 
        
        # Tạo Frame để chứa các thành phần
        self.content_frame = tk.Frame(self)
        self.content_frame.grid(row=0, column=0, padx=10, pady=10)

       # Nội dung của tab Employee List
        tk.Label(self.content_frame, text="Nhân viên nghỉ và làm việc tại nhà:").grid(row=0, column=0, padx=(0, 0), pady=(0, 0))
        self.selected_date_label = tk.Label(self.content_frame, text=f"{datetime.datetime.now().date()}")
        self.selected_date_label.grid(row=0, column=1, sticky='w', padx=(5, 0))  # Đặt column=1 để nằm cạnh nhau

        icon_calendar_path = os.path.join(os.path.dirname(__file__), '..', 'image', 'calendar.png')
        image_icon_calendar = Image.open(icon_calendar_path)
        resized_image = image_icon_calendar.resize((25, 25), Image.Resampling.LANCZOS)
        self.icon_calendar = ImageTk.PhotoImage(resized_image)
        self.show_calendar_button = tk.Button(self.content_frame, image=self.icon_calendar, command=self.show_calendar_dialog)
        self.show_calendar_button.grid(row=0, column=1, sticky='w', padx=(70, 5))  # Thêm padx để nút không quá gần cạnh

            # Tạo Treeview
        self.tree_working_time = ttk.Treeview(self.content_frame, show="headings", height=15)
        self.tree_working_time.grid(row=1, column=0, columnspan=4, padx=(0, 5), pady=5,sticky='ew')  # Giảm padx cho sát bên trái

        # Định nghĩa các cột
        self.tree_working_time["columns"] = ("name", "type_off", "type_time", "reason")

        # Thiết lập tiêu đề cho các cột
        self.tree_working_time.heading("name", text="Tên")
        self.tree_working_time.heading("type_off", text="Loại nghỉ")
        self.tree_working_time.heading("type_time", text="Loại thời gian")
        self.tree_working_time.heading("reason", text="Lý do")

        # Đặt độ rộng cho các cột
        self.tree_working_time.column("name", anchor="center", width=150)
        self.tree_working_time.column("type_off", anchor="center", width=120)
        self.tree_working_time.column("type_time", anchor="center", width=120)
        self.tree_working_time.column("reason", anchor="center", width=250)
        self.load_data_working_time(datetime.datetime.now().date().strftime("%Y-%m-%d"))


        tk.Label(self.content_frame, text="Quản lý thời gian làm việc theo năm:").grid(row=4, column=0, padx=5, pady=5)

        self.year_combobox = ttk.Combobox(self.content_frame, values=self.get_years())
        self.year_combobox.grid(row=4, column=1, padx=5, pady=5)
        self.year_combobox.set(datetime.datetime.now().year)

        tk.Label(self.content_frame, text="Chọn tên:").grid(row=4, column=3, padx=5, pady=5)
        employee_names = self.employee_list.get_employee_names()
        self.emp_combobox = ttk.Combobox(self.content_frame, values=employee_names)
        self.emp_combobox.grid(row=4, column=4, padx=5, pady=5)
        if employee_names:
            self.emp_combobox.set(employee_names[0])
        
        # Tạo Treeview với số lượng hàng tối đa là 10
        self.tree = ttk.Treeview(self.content_frame, show="headings", height=10)  # Giới hạn 10 hàng
        self.tree.grid(row=6, column=0, columnspan=10)

        # Tạo cột tiêu đề
        columns = ["Tên"]
        for i in range(1, 13):
            columns.append(f"OFF_{i}")
            columns.append(f"WFH_{i}")
            columns.append(f"OT_{i}")
        columns.append("total_off")
        columns.append("total_wfh")
        columns.append("total_ot")

        self.tree["columns"] = columns

        # Cài đặt tiêu đề cho cột
        self.tree.heading("Tên", text="Tên")
        self.tree.column("Tên", anchor="center", width=130)

        for i in range(1, 13):
            self.tree.heading(f"OFF_{i}", text=f"Tháng {i} OFF", anchor="center")
            self.tree.column(f"OFF_{i}", anchor="center", width=90)

            self.tree.heading(f"WFH_{i}", text=f"Tháng {i} WFH", anchor="center")
            self.tree.column(f"WFH_{i}", anchor="center", width=90)

            self.tree.heading(f"OT_{i}", text=f"Tháng {i} OT", anchor="center")
            self.tree.column(f"OT_{i}", anchor="center", width=90)

        self.tree.heading("total_off", text="Tổng OFF")
        self.tree.column("total_off", anchor="center", width=90)

        self.tree.heading("total_wfh", text="Tổng WFH")
        self.tree.column("total_wfh", anchor="center", width=90)

        self.tree.heading("total_ot", text="Tổng OT")
        self.tree.column("total_ot", anchor="center", width=90)

        # Tạo dữ liệu mẫu
        self.load_data()

        # Điều chỉnh kích thước cho Treeview
        self.grid_rowconfigure(5, weight=1)
        self.grid_columnconfigure(5, weight=1)

    def load_data(self):
        # Lấy dữ liệu tóm tắt thời gian làm việc của nhân viên
        summaries = self.working_time.get_employee_working_time_summary()

        # Xóa tất cả các mục hiện có trong Treeview trước khi thêm mới
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Thêm dữ liệu vào Treeview
        for summary in summaries:
            row = [
                summary['name'],  # Tên nhân viên
            ]
            # Thêm số ngày OFF, WFH, OT theo tháng
            for month in range(1, 13):
                row.append(summary.get(f"thang_{month}_OFF", 0))
                row.append(summary.get(f"thang_{month}_WFH", 0))
                row.append(summary.get(f"thang_{month}_OT", 0))

            # Thêm tổng số ngày OFF, WFH, OT
            row.append(summary.get("Total_OFF", 0))
            row.append(summary.get("Total_WFH", 0))
            row.append(summary.get("Total_OT", 0))

            # Thêm hàng vào Treeview
            self.tree.insert("", "end", values=row)

    def get_years(self):
        return [str(year) for year in range(2024, datetime.datetime.now().year+1)]
    
    def show_calendar_dialog(self):
        # Tạo một cửa sổ con (Toplevel window)
        calendar_dialog = tk.Toplevel(self)
        calendar_dialog.title("Chọn Ngày")

        # Tạo lịch trong cửa sổ dialog
        calendar = Calendar(calendar_dialog, selectmode='day', year=2024, month=10, day=13)
        calendar.pack(pady=20)

        # Nút OK và Cancel trong cửa sổ dialog
        ok_button = tk.Button(calendar_dialog, text="OK", command=lambda: self.select_date(calendar, calendar_dialog))
        ok_button.pack(side=tk.LEFT, padx=10)

        cancel_button = tk.Button(calendar_dialog, text="Cancel", command=calendar_dialog.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=10)

    def select_date(self, calendar, dialog):
        selected_date = calendar.get_date()
        print(selected_date)
        date_obj = datetime.datetime.strptime(selected_date, "%m/%d/%y")
    
        # Định dạng lại ngày thành yyyy-mm-dd
        formatted_date = date_obj.strftime("%Y-%m-%d")
        print(f"Selected Date: {formatted_date}")
        self.selected_date_label.config(text=f"{formatted_date}")
        dialog.destroy()  
        self.load_data_working_time(formatted_date)  # Gọi hàm load dữ liệu với ngày đã chọn

    def load_data_working_time(self, date):
        working_times = self.working_time.get_employee_working_time_by_day(date)

        # Xóa tất cả các mục hiện có trong Treeview trước khi thêm mới
        for item in self.tree_working_time.get_children():
            self.tree_working_time.delete(item)
        employees = self.employee_list.get_employees()
        employee_dict = {emp['emp_id']: emp['name'] for emp in employees}
        # Thêm dữ liệu vào Treeview
        for wt in working_times:
            self.tree_working_time.insert("", "end", values=(employee_dict.get(wt.emp_id, "Unknown"), wt.type_off, wt.type_time, wt.reason))

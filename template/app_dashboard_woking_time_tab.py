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
        # Nội dung của tab Employee List
        # label = tk.Label(self, text="This is the Employee List tab")
        # label.pack(padx=20, pady=20)
        # tk.Label(self, text="Nhân viên nghỉ và làm việc tại nhà:").grid(row=1, column=0)
        # self.selected_date_label = tk.Label(self, text=f"{datetime.datetime.now().date()}")
        # self.selected_date_label.grid(row=1, column=1, sticky='w')
        # icon_calendar_path = os.path.join(os.path.dirname(__file__), '..', 'image', 'calendar.png')
        # image_icon_calendar = Image.open(icon_calendar_path)
        # resized_image = image_icon_calendar.resize((25, 25), Image.Resampling.LANCZOS)
        # self.icon_calendar = ImageTk.PhotoImage(resized_image)
        # self.show_calendar_button = tk.Button(self, image=self.icon_calendar, command=self.show_calendar_dialog)
        # self.show_calendar_button.grid(row=1, column=2, sticky='w', padx=(0, 5))

        # tk.Label(self, text="Quản lý thời gian làm việc theo năm:").grid(row=4, column=0, padx=5, pady=5)

        # self.year_combobox = ttk.Combobox(self, values=self.get_years())
        # self.year_combobox.grid(row=4, column=1, padx=5, pady=5)
        # self.year_combobox.set(datetime.datetime.now().year)

        # tk.Label(self, text="Chọn tên:").grid(row=4, column=3, padx=5, pady=5)
        # employee_names = self.employee_list.get_employee_names()
        # self.emp_combobox = ttk.Combobox(self, values=employee_names)
        # self.emp_combobox.grid(row=4, column=4, padx=5, pady=5)
        # if employee_names:
        #     self.emp_combobox.set(employee_names[0])
        
        # # Tạo Treeview với số lượng hàng tối đa là 10
        # self.tree = ttk.Treeview(self, show="headings", height=10)  # Giới hạn 10 hàng
        # self.tree.grid(row=6, column=0, columnspan=10)

        # # Tạo cột tiêu đề
        # columns = ["Tên"]
        # for i in range(1, 13):
        #     columns.append(f"OFF_{i}")
        #     columns.append(f"WFH_{i}")
        #     columns.append(f"OT_{i}")
        # columns.append("total_off")
        # columns.append("total_wfh")
        # columns.append("total_ot")

        # self.tree["columns"] = columns

        # # Cài đặt tiêu đề cho cột
        # self.tree.heading("Tên", text="Tên")
        # self.tree.column("Tên", anchor="center", width=130)

        # for i in range(1, 13):
        #     self.tree.heading(f"OFF_{i}", text=f"Tháng {i} OFF", anchor="center")
        #     self.tree.column(f"OFF_{i}", anchor="center", width=90)

        #     self.tree.heading(f"WFH_{i}", text=f"Tháng {i} WFH", anchor="center")
        #     self.tree.column(f"WFH_{i}", anchor="center", width=90)

        #     self.tree.heading(f"OT_{i}", text=f"Tháng {i} OT", anchor="center")
        #     self.tree.column(f"OT_{i}", anchor="center", width=90)

        # self.tree.heading("total_off", text="Tổng OFF")
        # self.tree.column("total_off", anchor="center", width=90)

        # self.tree.heading("total_wfh", text="Tổng WFH")
        # self.tree.column("total_wfh", anchor="center", width=90)

        # self.tree.heading("total_ot", text="Tổng OT")
        # self.tree.column("total_ot", anchor="center", width=90)

        # # Tạo dữ liệu mẫu
        # self.load_data()

        # # Điều chỉnh kích thước cho Treeview
        # self.grid_rowconfigure(6, weight=1)
        # self.grid_columnconfigure(6, weight=1)

    # def load_data(self):
    #     year = 2024  # Hoặc có thể lấy năm từ một input khác
    #     self.tree.delete(*self.tree.get_children())  # Xóa dữ liệu cũ trong Treeview
        
    #     # Gọi phương thức để lấy dữ liệu
    #     working_time_data = self.working_time.list_working_time_by_year(year)
        
    #     for employee_id, data in working_time_data.items():
    #         # Giả sử employee có các thuộc tính như name và emp_id
    #         employee = self.employee_list.get_employee_by_id(employee_id)  
            
    #         # Kiểm tra nếu employee là None
    #         if employee is None:
    #             print(f"Warning: No employee found with ID {employee_id}.")
    #             continue  # Bỏ qua ID này nếu không tìm thấy nhân viên
            
    #         values = [employee.name] + [data["months"][month]["OFF"] for month in range(1, 13)] + \
    #                 [data["months"][month]["WFH"] for month in range(1, 13)] + \
    #                 [data["months"][month]["OT"] for month in range(1, 13)] + \
    #                 [data["total"]["OFF"], data["total"]["WFH"], data["total"]["OT"]]
    #         self.tree.insert("", "end", values=values)

    # def get_years(self):
    #     return [str(year) for year in range(2020, datetime.datetime.now().year+1)]
    
    # def show_calendar_dialog(self):
    #     # Tạo một cửa sổ con (Toplevel window)
    #     calendar_dialog = tk.Toplevel(self)
    #     calendar_dialog.title("Chọn Ngày")

    #     # Tạo lịch trong cửa sổ dialog
    #     calendar = Calendar(calendar_dialog, selectmode='day', year=2024, month=10, day=13)
    #     calendar.pack(pady=20)

    #     # Nút OK và Cancel trong cửa sổ dialog
    #     ok_button = tk.Button(calendar_dialog, text="OK", command=lambda: self.select_date(calendar, calendar_dialog))
    #     ok_button.pack(side=tk.LEFT, padx=10)

    #     cancel_button = tk.Button(calendar_dialog, text="Cancel", command=calendar_dialog.destroy)
    #     cancel_button.pack(side=tk.RIGHT, padx=10)

    # def select_date(self, calendar, dialog):
    #     selected_date = calendar.get_date()
    #     print(f"Selected Date: {selected_date}")
    #     self.selected_date_label.config(text=f"{selected_date}")
    #     dialog.destroy()   
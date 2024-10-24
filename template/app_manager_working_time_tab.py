import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import Calendar
import os
from PIL import Image, ImageTk

from service.employee_list import EmployeeList
from service.woking_time_service import WorkingTimeService

class ManagerWorkingTimeTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.working_time = WorkingTimeService()
        self.employee_list = EmployeeList()
        # self.load_employee_data()
        self.input_frame = tk.Frame(self)
        self.input_frame.pack(padx=10, pady=10)
        # Ô nhập Emp Name
        tk.Label(self.input_frame, text="Tên:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.emp_id_combobox = ttk.Combobox(self.input_frame)
        self.emp_id_combobox.grid(row=0, column=1, padx=5, pady=5)

        self.load_employee_data() 
        self.emp_id_combobox.bind("<<ComboboxSelected>>", self.on_combobox_select)
        today = datetime.datetime.now().strftime("%d/%m/%Y")
        tk.Label(self.input_frame, text="Chọn ngày:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.selected_date_label = tk.Label(self.input_frame, text=today)
        self.selected_date_label.grid(row=1, column=1)
        icon_calendar_path = os.path.join(os.path.dirname(__file__), '..', 'image', 'calendar.png')
        image_icon_calendar = Image.open(icon_calendar_path)
        resized_image = image_icon_calendar.resize((25, 25), Image.Resampling.LANCZOS)
        self.icon_calendar = ImageTk.PhotoImage(resized_image)
        self.show_calendar_button = tk.Button(self.input_frame, image=self.icon_calendar, command=self.show_calendar_dialog)
        self.show_calendar_button.grid(row=1, column=2, sticky='w', padx=(0, 5))

        # Ô nhập Status
        tk.Label(self.input_frame, text="Trạng thái:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.status_entry = ttk.Combobox(self.input_frame, values=["Đồng ý", "Từ chối", "None"])
        self.status_entry.grid(row=2, column=1, padx=5, pady=5)
        self.status_entry.set('None')

        # Ô nhập Reason
        tk.Label(self.input_frame, text="Lý do:").grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.reason_entry = tk.Entry(self.input_frame)
        self.reason_entry.grid(row=3, column=1, padx=5, pady=5)

        # Ô nhập Type Off
        tk.Label(self.input_frame, text="Loại nghỉ:").grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.typeOff_entry = ttk.Combobox(self.input_frame, values=["OFF", "OT", "WFH"])
        self.typeOff_entry.grid(row=4, column=1, padx=5, pady=5)
        self.typeOff_entry.set("OFF")

        # Ô nhập Type Time
        tk.Label(self.input_frame, text="Loại thời gian:").grid(row=5, column=0, padx=5, pady=5, sticky='w')
        self.typeTime_entry = ttk.Combobox(self.input_frame, values=["AM", "PM", "DAY"])
        self.typeTime_entry.grid(row=5, column=1, padx=5, pady=5)
        self.typeTime_entry.set("DAY")

        # Nút Thêm
        self.add_button = tk.Button(self.input_frame, text="Thêm", command=self.add_working_time)
        self.add_button.grid(row=6, column=0, pady=5, sticky='w')

        # Nút Xóa
        self.delete_button = tk.Button(self.input_frame, text="Xóa", command=self.delete_working_time)
        self.delete_button.grid(row=6, column=1, pady=5, sticky='w')

        # Nút Sửa
        self.edit_button = tk.Button(self.input_frame, text="Sửa", command=self.update_working_time)
        self.edit_button.grid(row=6, column=2, pady=5, sticky='w')

        # Tạo Treeview để hiển thị dữ liệu
        self.tree = ttk.Treeview(self, columns=("ID", "Name", "Time", "Status", "Reason", "Type Off", "Type Time"), show="headings", height=10)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Tên")
        self.tree.heading("Time", text="Thời gian")
        self.tree.heading("Status", text="Trạng thái")
        self.tree.heading("Reason", text="Lý do")
        self.tree.heading("Type Off", text="Loại nghỉ")
        self.tree.heading("Type Time", text="Loại thời gian")
        self.tree.pack(pady=10, fill='both', expand=True)
        self.tree.tag_configure("center", anchor="center")
        self.update_treeview()
        self.tree.bind("<Double-1>", self.on_tree_select)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)


    def load_employee_data(self):
        employees = self.employee_list.get_employees()
        self.employee_names = [employee['name'] for employee in employees]
        self.employee_ids = [employee['emp_id'] for employee in employees]

        self.emp_id_combobox['values'] = self.employee_names

        if self.employee_names:
            self.emp_id_combobox.set(self.employee_names[0]) 
            self.selected_emp_id = tk.StringVar(value=self.employee_ids[0])
    

    def select_date(self, calendar, dialog):
        selected_date = calendar.get_date()
        self.selected_date = datetime.datetime.strptime(selected_date, "%m/%d/%y").strftime("%d/%m/%Y")
        self.selected_date_label.config(text=self.selected_date)
        dialog.destroy()

    def on_combobox_select(self, event):
        self.working_time.get_employee_working_time_summary()
        selected_name = self.emp_id_combobox.get()
        selected_index = self.employee_names.index(selected_name)
        self.selected_emp_id.set(self.employee_ids[selected_index])  

    def add_working_time(self):
        emp_id = self.selected_emp_id.get()
        time = self.selected_date_label.cget("text")
        if self.status_entry.get() == "Đồng ý":
            status_display = "accept"
        elif self.status_entry.get() == "Từ chối":
            status_display = "decline"
        else:
            status_display = "none"
        status = status_display
        reason = self.reason_entry.get()
        typeOff = self.typeOff_entry.get()
        typeTime = self.typeTime_entry.get()
        try:
            # Kiểm tra định dạng ngày (dd/mm/yyyy)
            datetime.datetime.strptime(time, "%d/%m/%Y") 
            self.working_time.add_working_time(emp_id, time, status, reason, typeOff, typeTime)
            self.update_treeview()
            messagebox.showinfo("Thành công", "Thời gian làm việc đã được thêm.")
            self.clear_entries()  # Xóa các ô nhập liệu sau khi thêm
            # self.working_time.list_working_time_by_year(2024)
        except ValueError as e:
            messagebox.showerror("Lỗi", f"Định dạng ngày không hợp lệ: {str(e)}")

    def update_working_time(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh Báo", "Vui lòng chọn thời gian làm việc để sửa!")
            return
        selected_item_id = selected_item[0]
        working_time_values = self.tree.item(selected_item_id)["values"]  
        working_time_id = working_time_values[0]
        emp_id = self.selected_emp_id.get()
        time = self.selected_date_label.cget("text")
        status = self.status_entry.get()
        reason = self.reason_entry.get()
        typeOff = self.typeOff_entry.get()
        typeTime = self.typeTime_entry.get()
        try:
            # Call the update_employee method with the appropriate parameters
            self.working_time.update_working_time(working_time_id, emp_id, time, status, reason, typeOff,typeTime) 
            self.update_treeview()  # Refresh the interface
            self.clear_entries()  # Clear input fields
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
            print(str(e))


    def delete_working_time(self):
        selected_item = self.tree.selection()
        if selected_item:
            selected_item_id = selected_item[0]
            working_time_values = self.tree.item(selected_item_id)["values"]  
            working_time_id = working_time_values[0]
            self.working_time.delete_working_time(working_time_id)
            self.update_treeview()
            self.clear_entries()
        else:
            messagebox.showwarning("Cảnh Báo", "Vui lòng chọn nhân viên để xóa!")

    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            index = self.tree.index(selected_item)
            working_time = self.working_time.get_working_time()[index]
            indexEmp = self.employee_ids.index(str(working_time.emp_id))
            self.selected_emp_id.set(working_time.emp_id)
            self.emp_id_combobox.set(self.employee_names[indexEmp])
            self.selected_date_label.config(text=working_time.time.strftime("%d/%m/%Y"))
            if working_time.status == "accept":
                status_display = "Đồng ý"
            elif working_time.status == "decline":
                status_display = "Từ chối"
            else:
                status_display = "None"
            self.status_entry.delete(0, tk.END)
            self.status_entry.insert(0, status_display)
            self.reason_entry.delete(0, tk.END)
            self.reason_entry.insert(0, working_time.reason if working_time.reason is not None else "")
            self.typeOff_entry.delete(0, tk.END)
            self.typeOff_entry.insert(0, working_time.type_off)
            self.typeTime_entry.delete(0, tk.END)
            self.typeTime_entry.insert(0, working_time.type_time)

    def update_treeview(self):
        # Làm sạch Treeview trước khi cập nhật
        for item in self.tree.get_children():
            self.tree.delete(item)
        employees = self.employee_list.get_employees()
        for working_time in self.working_time.get_working_time():
            employee_name = "None" 
            for employee in employees:
                if employee['emp_id'] == str(working_time.emp_id):
                    employee_name = employee['name'] 
                    break
            if working_time.status == "accept":
                status_display = "Đồng ý"
            elif working_time.status == "decline":
                status_display = "Từ chối"
            else:
                status_display = None
            self.tree.insert("", "end", values=(working_time.working_time_id,
            employee_name , working_time.time.strftime("%d/%m/%Y"), status_display, working_time.reason, working_time.type_off, working_time.type_time))

    def clear_entries(self):
        # Xóa các ô nhập liệu
        self.reason_entry.delete(0, tk.END)

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

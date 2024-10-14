import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import datetime
from tkcalendar import Calendar
import os
from PIL import Image, ImageTk

from service.employee_list import EmployeeList
from service.woking_time_service import WorkingTimeService

class ManagerWorkingTimeTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.working_time = WorkingTimeService()
        self.employee_list = EmployeeList()  # Giả sử lớp này đã được định nghĩa

        # Lưu danh sách tên và id
        employees = self.employee_list.get_employees()
        
        # Lưu danh sách tên và id
        self.employee_names = [employee.name for employee in employees]  # Sử dụng thuộc tính name của đối tượng Employee
        self.employee_ids = [employee.emp_id for employee in employees]  # Sử dụng thuộc tính emp_id của đối tượng Employee

        # Ô nhập Emp Name
        tk.Label(self, text="Emp Name:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.emp_id_combobox = ttk.Combobox(self, values=self.employee_names)
        self.emp_id_combobox.grid(row=0, column=1, padx=5, pady=5)
        
        if self.employee_names:
            self.emp_id_combobox.set(self.employee_names[0])  # Đặt tên đầu tiên làm giá trị mặc định
            self.selected_emp_id = tk.StringVar(value=self.employee_ids[0])  # Đặt emp_id đầu tiên làm giá trị mặc định

        self.emp_id_combobox.bind("<<ComboboxSelected>>", self.on_combobox_select)

        # Ô nhập Time
        tk.Label(self, text="Time (DD/MM/YYYY):").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.selected_date_label = tk.Label(self, text=f"{datetime.datetime.now().strftime('%d/%m/%Y')}")  # Định dạng ngày
        self.selected_date_label.grid(row=1, column=1, sticky='w')

        icon_calendar_path = os.path.join(os.path.dirname(__file__), '..', 'image', 'calendar.png')
        image_icon_calendar = Image.open(icon_calendar_path)
        resized_image = image_icon_calendar.resize((25, 25), Image.Resampling.LANCZOS)
        self.icon_calendar = ImageTk.PhotoImage(resized_image)
        self.show_calendar_button = tk.Button(self, image=self.icon_calendar, command=self.show_calendar_dialog)
        self.show_calendar_button.grid(row=1, column=2, sticky='w', padx=(0, 5))

        # Ô nhập Status
        tk.Label(self, text="Status:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.status_entry = ttk.Combobox(self, values=["Dòng ý", "Từ chối", "None"])
        self.status_entry.grid(row=2, column=1, padx=5, pady=5)
        self.status_entry.set("None")

        # Ô nhập Reason
        tk.Label(self, text="Reason:").grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.reason_entry = tk.Entry(self)
        self.reason_entry.grid(row=3, column=1, padx=5, pady=5)

        # Ô nhập Type Off
        tk.Label(self, text="Type Off:").grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.typeOff_entry = ttk.Combobox(self, values=["OFF", "OT", "WFH"])
        self.typeOff_entry.grid(row=4, column=1, padx=5, pady=5)
        self.typeOff_entry.set("OFF")

        # Ô nhập Type Time
        tk.Label(self, text="Type Time:").grid(row=5, column=0, padx=5, pady=5, sticky='w')
        self.typeTime_entry = ttk.Combobox(self, values=["AM", "PM", "DAY"])
        self.typeTime_entry.grid(row=5, column=1, padx=5, pady=5)
        self.typeTime_entry.set("DAY")

        # Nút Thêm
        self.add_button = tk.Button(self, text="Thêm", command=self.add_working_time)
        self.add_button.grid(row=6, column=0, pady=5, sticky='w')

        # Nút Xóa
        self.delete_button = tk.Button(self, text="Xóa", command=self.delete_working_time)
        self.delete_button.grid(row=6, column=1, pady=5, sticky='w')

        # Nút Sửa
        self.edit_button = tk.Button(self, text="Sửa", command=self.update_working_time)
        self.edit_button.grid(row=6, column=2, pady=5, sticky='w')

        # Tạo Treeview để hiển thị dữ liệu
        self.tree = ttk.Treeview(self, columns=("ID", "Name", "Time", "Status", "Reason", "Type Off", "Type Time"), show="headings", height=10)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Time", text="Time")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Reason", text="Reason")
        self.tree.heading("Type Off", text="Type Off")
        self.tree.heading("Type Time", text="Type Time")
        self.tree.grid(row=9, column=0, columnspan=2)  
        self.tree.tag_configure("center", anchor="center")
        self.tree.bind("<Double-1>", self.on_tree_select)

        self.grid_rowconfigure(9, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def select_date(self, calendar, dialog):
        selected_date = calendar.get_date()
        self.selected_date = datetime.datetime.strptime(selected_date, "%m/%d/%y").strftime("%d/%m/%Y")
        self.selected_date_label.config(text=self.selected_date)
        dialog.destroy()

    def on_combobox_select(self, event):
        selected_name = self.emp_id_combobox.get()
        selected_index = self.employee_names.index(selected_name)
        self.selected_emp_id.set(self.employee_ids[selected_index])  

    def add_working_time(self):
        emp_id = self.selected_emp_id.get()
        time = self.selected_date_label.cget("text")
        status = self.status_entry.get()
        reason = self.reason_entry.get()
        typeOff = self.typeOff_entry.get()
        typeTime = self.typeTime_entry.get()

        try:
            # Kiểm tra định dạng ngày (dd/mm/yyyy)
            datetime.datetime.strptime(time, "%d/%m/%Y")  

            # Thực hiện lưu thông tin vào hệ thống
            print(f"emp_id: {emp_id},Time: {time}, Status: {status}, Reason: {reason}, Type Off: {typeOff}, Type Time: {typeTime}")
            
            # Giả sử bạn có hàm để xử lý thêm thời gian làm việc:
            self.working_time.add_working_time(emp_id, time, status, reason, typeOff, typeTime)
            self.update_treeview()
            messagebox.showinfo("Thành công", "Thời gian làm việc đã được thêm.")
            self.clear_entries()  # Xóa các ô nhập liệu sau khi thêm

        except ValueError as e:
            messagebox.showerror("Lỗi", f"Định dạng ngày không hợp lệ: {str(e)}")

    def update_working_time(self):
        selected_item = self.tree.selection()
        if selected_item:
            index = self.tree.index(selected_item)
            emp_id = self.selected_emp_id.get()
            time = self.selected_date_label.cget("text")
            status = self.status_entry.get()
            reason = self.reason_entry.get()
            typeOff = self.typeOff_entry.get()
            typeTime = self.typeTime_entry.get()

            self.working_time.update_working_time(index, emp_id, time, status, reason, typeOff,typeTime)
            self.update_treeview()
            self.clear_entries()
        else:
            messagebox.showwarning("Cảnh Báo", "Vui lòng chọn nhân viên để sửa!")


    def delete_working_time(self):
        selected_item = self.tree.selection()
        if selected_item:
            index = self.tree.index(selected_item)
            self.working_time.delete_working_time(index)
            self.update_treeview()
            self.clear_entries()
        else:
            messagebox.showwarning("Cảnh Báo", "Vui lòng chọn nhân viên để xóa!")

    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            index = self.tree.index(selected_item)
            working_time = self.working_time.list_working_times()[index]
            indexEmp = self.employee_ids.index(int(working_time.emp_id))
            self.selected_emp_id.set(working_time.emp_id)
            self.emp_id_combobox.set(self.employee_names[indexEmp])
            self.selected_date_label.config(text=working_time.time)
            self.status_entry.delete(0, tk.END)
            self.status_entry.insert(0, working_time.status)
            self.reason_entry.delete(0, tk.END)
            self.reason_entry.insert(0, working_time.reason)
            self.typeOff_entry.delete(0, tk.END)
            self.typeOff_entry.insert(0, working_time.typeOff)
            self.typeTime_entry.delete(0, tk.END)
            self.typeTime_entry.insert(0, working_time.typeTime)

    def update_treeview(self):
        # Làm sạch Treeview trước khi cập nhật
        for item in self.tree.get_children():
            self.tree.delete(item)
        employees = self.employee_list.get_employees()
        for working_time in self.working_time.working_time_list:
            employee_name = None 
            for employee in employees:
                if employee.emp_id == int(working_time.emp_id):
                    employee_name = employee.name
                    break
            self.tree.insert("", "end", values=(working_time.working_time_id,
            employee_name , working_time.time, working_time.status, working_time.reason, working_time.typeOff, working_time.typeTime))

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

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from service.employee_list import EmployeeList  # Đảm bảo đường dẫn này chính xác
from service.Payroll_list import PayrollList
from enity.employee import Employee
class PositionApp(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)


        # Các trường nhập liệu (2 cột)
        tk.Label(self.frame, text="Tên Chức vụ:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(self.frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.frame, text="Hệ Số Lương:").grid(row=0, column=2, padx=5, pady=5)
        self.age_entry = tk.Entry(self.frame)
        self.age_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Khung chứa các nút (Thêm, Sửa, Xóa)
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        # Nút thêm
        self.add_button = tk.Button(button_frame, text="Thêm Chức Vụ", command=self.add_position)
        self.add_button.grid(row=0, column=0, padx=10)

        # Nút sửa
        self.update_button = tk.Button(button_frame, text="Sửa Chức Vự", command=self.update_employee)
        self.update_button.grid(row=0, column=1, padx=10)

        # Nút xóa
        self.delete_button = tk.Button(button_frame, text="Xóa Chức Vụ", command=self.delete_employee)
        self.delete_button.grid(row=0, column=2, padx=10)
         # Cây để hiển thị nhân viên
        self.tree = ttk.Treeview(self, columns=("ID", "Tên Chức Vụ", "Hệ Số Lương"), show="headings")
        self.tree.pack(pady=10)

        # Treeview để hiển thị danh sách chức vụ
        # Đặt tiêu đề cho các cột
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor='center')

        self.tree.grid(row=4, column=0, columnspan=2)
    def add_position(self):
        id = self.entry_id.get()
        name = self.entry_name.get()
        salary_coefficient = self.entry_salary_coefficient.get()
        
        if id and name and salary_coefficient:
            try:
                salary_coefficient = float(salary_coefficient)
                self.position_module.add_position(id, name, salary_coefficient)
                self.refresh_treeview()
                self.clear_entries()
            except ValueError:
                messagebox.showerror("Lỗi", "Hệ số lương phải là số.")
        else:
            messagebox.showerror("Lỗi", "Vui lòng điền đủ thông tin.")

    def refresh_treeview(self):
        # Xóa dữ liệu cũ
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Thêm dữ liệu mới
        for position in self.position_module.get_all_positions():
            self.tree.insert("", "end", values=(position.id, position.name, position.salary_coefficient))

    def clear_entries(self):
        self.entry_id.delete(0, tk.END)
        self.entry_name.delete(0, tk.END)
        self.entry_salary_coefficient.delete(0, tk.END)

    def save_to_csv(self):
        filename = "positions.csv"
        self.position_module.save_to_csv(filename)
        messagebox.showinfo("Thông báo", f"Dữ liệu đã được lưu vào {filename}.")

    def load_from_csv(self):
        filename = "positions.csv"
        self.position_module.load_from_csv(filename)
        self.refresh_treeview()
        messagebox.showinfo("Thông báo", f"Dữ liệu đã được tải từ {filename}.")
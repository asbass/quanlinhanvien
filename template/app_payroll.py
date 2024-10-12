import tkinter as tk
from tkinter import messagebox, ttk
from enity.employee import Employee
from enity.Payroll import Payroll
from service.Payroll_list import PayrollList

class PayrollApp(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.Payroll_list = PayrollList()
        # Khung nhập liệu
        self.frame = tk.Frame(self)
        self.frame.pack(pady=10)
        # Các trường nhập liệu (2 cột)
        tk.Label(self.frame, text="ID:").grid(row=0, column=0, padx=5, pady=5)
        self.ID_entry = tk.Entry(self.frame)
        self.ID_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(self.frame, text="Tên:").grid(row=0, column=2, padx=5, pady=5)
        self.name_entry = tk.Entry(self.frame)
        self.name_entry.grid(row=0, column=3, padx=5, pady=5)
        tk.Label(self.frame, text="Vị Trí:").grid(row=1, column=0, padx=5, pady=5)
        self.pos_entry = tk.Entry(self.frame)
        self.pos_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(self.frame, text="Thưởng:").grid(row=1, column=2, padx=5, pady=5)
        self.reward_entry = tk.Entry(self.frame)
        self.reward_entry.grid(row=1, column=3, padx=5, pady=5)
        tk.Label(self.frame, text="Phạt:").grid(row=2, column=0, padx=5, pady=5)
        self.punish_entry = tk.Entry(self.frame)
        self.punish_entry.grid(row=2, column=1, padx=5, pady=5)
        tk.Label(self.frame, text="Số Ngày Nghỉ:").grid(row=2, column=2, padx=5, pady=5)
        self.dayoff_entry = tk.Entry(self.frame)
        self.dayoff_entry.grid(row=2, column=3, padx=5, pady=5)
        # Khung chứa các nút (Thêm, Sửa, Xóa)
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        # Nút thêm
        self.add_button = tk.Button(button_frame, text="Cập nhật lương",)
        self.add_button.grid(row=4, column=1, padx=10)

        # Nút sửa
        self.update_button = tk.Button(button_frame, text="Xoá trường đã nhập", command=self.clear_entries)
        self.update_button.grid(row=4, column=3, padx=10)

        self.tree = ttk.Treeview(self, columns=("ID", "Tên", "Vị Trí","Số Ngày Nghỉ", "Thưởng", "Phạt","Tổng Lương"), show="headings")
        self.tree.pack(pady=10)
        self.sort_reverse = {col: False for col in ("ID", "Tên", "Vị Trí","Số Ngày Nghỉ", "Thưởng", "Phạt","Tổng Lương")}
        for col in ("ID", "Tên", "Vị Trí","Số Ngày Nghỉ", "Thưởng", "Phạt", "Tổng Lương"):
            # Thêm sự kiện sắp xếp khi nhấp vào tiêu đề cột
            self.tree.heading(col, text=col, command=lambda _col=col: self.sort_column(_col, self.sort_reverse[_col]))
            self.tree.column(col, anchor="center")  # Căn giữa nội dung cột
        self.display_payroll()
        self.tree.bind("<ButtonRelease-1>", self.on_tree_select)

    def display_payroll(self):
    # Xóa dữ liệu cũ trong Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)
    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            index = self.tree.index(selected_item)
            payroll = self.Payroll_list.get_Payroll()[index]

            self.ID_entry.delete(0, tk.END)
            self.ID_entry.insert(0, payroll.emp_id)
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, payroll.name)
            self.pos_entry.delete(0, tk.END)
            self.pos_entry.insert(0, payroll.position)
            self.reward_entry.delete(0, tk.END)
            self.reward_entry.insert(0, payroll.reward)
            self.reward_entry.delete(0, tk.END)
            self.punish_entry.insert(0, payroll.punish)
            self.punish_entry.delete(0, tk.END)
            self.dayoff_entry.insert(0, payroll.dayoff)
            self.dayoff_entry.delete(0, tk.END)
    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.ID_entry.delete(0, tk.END)
        self.pos_entry.delete(0, tk.END)
        self.reward_entry.delete(0, tk.END)
        self.punish_entry.delete(0, tk.END)
        self.dayoff_entry.delete(0, tk.END)
    # Thêm nhân viên vào Treeview
        for pay in self.Payroll_list.get_Payroll():
            self.tree.insert("", "end", values=(pay.emp_id, pay.name, pay.position, pay.dayoff, pay.reward, pay.punish, pay.total))
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from service.posittion_list import PositionList  # Đảm bảo đường dẫn này chính xác

class PositonsApp(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.position_list = PositionList()  # Khởi tạo PositionList

        # Các trường nhập liệu (2 cột)
        tk.Label(self, text="Tên Chức Vụ:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_name = tk.Entry(self)
        self.entry_name.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self, text="Hệ Số Lương:").grid(row=1, column=2, padx=5, pady=5)
        self.entry_salary_coefficient = tk.Entry(self)
        self.entry_salary_coefficient.grid(row=1, column=3, padx=5, pady=5)

        # Khung chứa các nút (Thêm, Sửa, Xóa)
        button_frame = tk.Frame(self)
        button_frame.grid(row=2, columnspan=4, pady=10)

        # Nút thêm
        self.add_button = tk.Button(button_frame, text="Thêm Chức Vụ", command=self.add_position)
        self.add_button.grid(row=0, column=0, padx=10)

        # Nút sửa
        self.update_button = tk.Button(button_frame, text="Sửa Chức Vụ", command=self.update_position)
        self.update_button.grid(row=0, column=1, padx=10)

        # Nút xóa
        self.delete_button = tk.Button(button_frame, text="Xóa Chức Vụ", command=self.delete_position)
        self.delete_button.grid(row=0, column=2, padx=10)

        # Cây để hiển thị chức vụ
        self.tree = ttk.Treeview(self, columns=("ID", "Tên Chức Vụ", "Hệ Số Lương"), show="headings")
        self.tree.grid(row=3, column=0, columnspan=4, pady=10)

        # Đặt tiêu đề cho các cột
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor='center')

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)  # Liên kết sự kiện chọn

        self.refresh_treeview()  # Tải dữ liệu chức vụ khi khởi động

    def on_tree_select(self, event):
        """Xử lý sự kiện chọn một chức vụ trong cây."""
        selected_item = self.tree.selection()
        if selected_item:
            position_id = self.tree.item(selected_item)['values'][0]
            position = self.position_list.get_position_by_id(position_id)  # Lấy thông tin chức vụ

            if position:
                self.entry_name.delete(0, tk.END)
                self.entry_name.insert(0, position.name)  # Hiển thị tên chức vụ
                self.entry_salary_coefficient.delete(0, tk.END)
                self.entry_salary_coefficient.insert(0, position.salary_multiplier)  # Hiển thị hệ số lương

    def add_position(self):
        name = self.entry_name.get()
        salary_coefficient = self.entry_salary_coefficient.get()
        
        if name and salary_coefficient:
            try:
                salary_coefficient = float(salary_coefficient)
                self.position_list.add_position(name, salary_coefficient)
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
        for position in self.position_list.get_all_positions():
            self.tree.insert("", "end", values=(position.position_id, position.name, position.salary_multiplier))

    def clear_entries(self):
        self.entry_name.delete(0, tk.END)
        self.entry_salary_coefficient.delete(0, tk.END)

    def update_position(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Lỗi", "Vui lòng chọn chức vụ để sửa.")
            return

        position_id = self.tree.item(selected_item)['values'][0]
        name = self.entry_name.get()
        salary_coefficient = self.entry_salary_coefficient.get().strip()  # Loại bỏ khoảng trắng

        if name and salary_coefficient:
            try:
                # Kiểm tra và thay thế dấu phẩy bằng dấu chấm nếu cần
                salary_coefficient = salary_coefficient.replace(',', '.')
                salary_coefficient = float(salary_coefficient)  # Chuyển đổi sang float
                index = next((i for i, pos in enumerate(self.position_list.positions) if pos.position_id == position_id), None)
                if index is not None:
                    self.position_list.update_position(index, name, salary_coefficient)  # Cập nhật vị trí
                    self.refresh_treeview()  # Làm mới giao diện
                    self.clear_entries()  # Làm sạch các trường nhập liệu
                else:
                    messagebox.showerror("Lỗi", "Chức vụ không tìm thấy.")
            except ValueError:
                messagebox.showerror("Lỗi", f"Hệ số lương '{salary_coefficient}' không phải là số hợp lệ. Vui lòng nhập lại.")
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))
        else:
            messagebox.showerror("Lỗi", "Vui lòng điền đủ thông tin.")



    def delete_position(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Lỗi", "Vui lòng chọn chức vụ để xóa.")
            return

        position_id = self.tree.item(selected_item)['values'][0]
        self.position_list.delete_position(position_id)
        self.refresh_treeview()

    def close_connection(self):
        self.position_list.close_connection()

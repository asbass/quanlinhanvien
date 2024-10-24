import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from service.posittion_list import PositionList  # Đảm bảo đường dẫn này chính xác

class PositonsApp(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.position_list = PositionList()  # Khởi tạo PositionList
        
       # Khung nhập liệu
        self.frame = tk.Frame(self)
        self.frame.pack(pady=10, padx=10, fill=tk.X)  # Thay đổi sang pack

        # Các trường nhập liệu (sử dụng pack)
        input_frame = tk.Frame(self.frame)  # Tạo frame mới cho các trường nhập liệu
        input_frame.pack(fill=tk.X, padx=5, pady=5)  # Sử dụng pack

        tk.Label(input_frame, text="Tên Chức Vụ:").pack(side=tk.LEFT, padx=5)
        self.entry_name = tk.Entry(input_frame)
        self.entry_name.pack(side=tk.LEFT,fill=tk.X, expand=True, padx=5)

        tk.Label(input_frame, text="Hệ Số Lương:").pack(side=tk.LEFT, padx=5)
        self.entry_salary_coefficient = tk.Entry(input_frame)
        self.entry_salary_coefficient.pack(side=tk.LEFT,fill=tk.X, expand=True, padx=5)

        # Khung chứa các nút (Thêm, Sửa, Xóa) - sử dụng pack
        button_frame = tk.Frame(self.frame)
        button_frame.pack(pady=10)  # Sử dụng pack để quản lý nút

        # Nút thêm
        self.add_button = tk.Button(button_frame, text="Thêm Chức Vụ", command=self.add_position)
        self.add_button.pack(side=tk.LEFT, padx=10)

        # Nút sửa
        self.update_button = tk.Button(button_frame, text="Sửa Chức Vụ", command=self.update_position)
        self.update_button.pack(side=tk.LEFT, padx=10)

        # Nút xóa
        self.delete_button = tk.Button(button_frame, text="Xóa Chức Vụ", command=self.delete_position)
        self.delete_button.pack(side=tk.LEFT, padx=10)

        # Cây để hiển thị chức vụ (Cũng sử dụng pack)
        tree_frame = tk.Frame(self)  # Tạo frame để chứa Treeview
        tree_frame.pack(pady=10, fill=tk.BOTH, expand=True)  # Sử dụng pack

        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Tên Chức Vụ", "Hệ Số Lương"), show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True)  # Sử dụng pack

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
            position = self.position_list.get_position(position_id)  # Lấy thông tin chức vụ

            if position:
                self.entry_name.delete(0, tk.END)
                self.entry_name.insert(0, position["name"])  # Hiển thị tên chức vụ
                self.entry_salary_coefficient.delete(0, tk.END)
                self.entry_salary_coefficient.insert(0, position["salary_multiplier"])  # Hiển thị hệ số lương

    def add_position(self):
        name = self.entry_name.get()
        salary_coefficient = self.entry_salary_coefficient.get()
        
        if name and salary_coefficient:
            try:
                salary_coefficient = float(salary_coefficient)

                # Kiểm tra nếu hệ số lương âm
                if salary_coefficient < 0:
                    messagebox.showerror("Lỗi", "Hệ số lương không được là số âm.")
                    return  # Dừng thêm nếu hệ số lương âm
                
                self.position_list.add_position(name, salary_coefficient)
                self.refresh_treeview()
                self.clear_entries()

                if hasattr(self.master.master, 'update_Postion_list_in_position_app'):
                    self.master.master.update_Postion_list_in_position_app()
                    print("Chức vụ đã được thêm thành công và danh sách đã được cập nhật.")
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
                    if hasattr(self.master.master, 'update_Postion_list_in_position_app'):
                        self.master.master.update_Postion_list_in_position_app()
                        print("Chuc vu đã được sửa thành công và danh sách đã được cập nhật.")
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
        if hasattr(self.master.master, 'update_Postion_list_in_position_app'):
                    self.master.master.update_Postion_list_in_position_app()
                    print("Chuc vu đã được xóa thành công và danh sách đã được cập nhật.")

    def close_connection(self):
        self.position_list.close_connection()
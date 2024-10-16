import tkinter as tk
from tkinter import messagebox, ttk
from enity.department import Department
from service.department_list import departmentList
from service.employee_list import EmployeeList 

class DepartmentApp(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.department_list = departmentList()
        self.employee_list = EmployeeList() 
        # Khung nhập liệu
        self.frame = tk.Frame(self)
        self.frame.pack(pady=10)

        # Các trường nhập liệu (2 cột)
        tk.Label(self.frame, text="Tên Phòng Ban:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(self.frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(self.frame, text="Trưởng Phòng:").grid(row=1, column=0, padx=5, pady=5)
        self.manager_combobox = ttk.Combobox(self.frame, state="readonly")  # Tạo ComboBox
        self.manager_combobox.grid(row=1, column=1, padx=5, pady=5)
        self.load_employee_names()  # Gọi phương thức để tải tên nhân viên vào ComboBox
        # Khung chứa các nút (Thêm, Sửa, Xóa)
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        # Nút thêm
        self.add_button = tk.Button(button_frame, text="Thêm Phòng Ban", command=self.add_department)
        self.add_button.grid(row=0, column=0, padx=10)

        # Nút sửa
        self.update_button = tk.Button(button_frame, text="Sửa Phòng Ban", command=self.update_department)
        self.update_button.grid(row=0, column=1, padx=10)

        # Nút xóa
        self.delete_button = tk.Button(button_frame, text="Xóa Phòng Ban", command=self.delete_department)
        self.delete_button.grid(row=0, column=2, padx=10)

        # Cây để hiển thị phòng ban
        self.tree = ttk.Treeview(self, columns=("Mã PB", "Tên PB", "Trưởng Phòng"), show="headings")
        self.tree.pack(pady=10)
        self.tree.heading("Mã PB", text="Mã PB")
        self.tree.heading("Tên PB", text="Tên PB")
        self.tree.heading("Trưởng Phòng", text="Trưởng Phòng")
        self.display_department()
        self.tree.bind("<ButtonRelease-1>", self.on_tree_select)

    def add_department(self):
        name = self.name_entry.get()
        positions = self.manager_combobox.get()
        if name:
            
            self.department_list.add_department(name,positions)
            self.department_list.save_to_csv()
            self.update_treeview()
            self.clear_entries()
            if hasattr(self.master.master, 'update_department_list_in_employee_app'):
                self.master.master.update_department_list_in_employee_app()
        else:
            messagebox.showwarning("Cảnh Báo", "Vui lòng nhập tên phòng ban!")
    def update_department(self):
        selected_item = self.tree.selection()
        if selected_item:
            index = self.tree.index(selected_item)
            name = self.name_entry.get()
            positions = self.manager_combobox.get()
            if name:
                self.department_list.update_department(index, name,positions)
                self.department_list.save_to_csv()
                self.update_treeview()
                self.clear_entries()
                if hasattr(self.master.master, 'update_department_list_in_employee_app'):
                    self.master.master.update_department_list_in_employee_app()
            else:
                messagebox.showwarning("Cảnh Báo", "Vui lòng nhập tên phòng ban!")
        else:
            messagebox.showwarning("Cảnh Báo", "Vui lòng chọn phòng ban để sửa!")

    def delete_department(self):
        selected_item = self.tree.selection()
        if selected_item:
            index = self.tree.index(selected_item)
            self.department_list.del_department(index)
            self.department_list.save_to_csv()
            self.update_treeview()
            self.clear_entries()
            if hasattr(self.master.master, 'update_department_list_in_employee_app'):
                self.master.master.update_department_list_in_employee_app()
        else:
            messagebox.showwarning("Cảnh Báo", "Vui lòng chọn phòng ban để xóa!")
    
    def load_employee_names(self):
        employee_names = self.employee_list.get_employee_names() 
        self.manager_combobox['values'] = employee_names
    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            index = self.tree.index(selected_item)
            department = self.department_list.get_department()[index]
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, department.name)
            self.manager_combobox.set(department.positions)
    def update_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for dept in self.department_list.get_department():
            self.tree.insert("", "end", values=(dept.dept_id, dept.name, dept.positions))

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.manager_combobox.set('') 
    def display_department(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for dept in self.department_list.get_department():
            self.tree.insert("", "end", values=(dept.dept_id, dept.name, dept.positions))
    def update_employee_list(self, employee_list):
        self.manager_combobox['values'] = [emp.name for emp in employee_list]
        print("Danh sách nhân viên đã được cập nhật.")
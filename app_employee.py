import tkinter as tk
from tkinter import messagebox, ttk
from employee import Employee
from employee_list import EmployeeList

class EmployeeApp(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.employee_list = EmployeeList()

        # Khung nhập liệu
        self.frame = tk.Frame(self)
        self.frame.pack(pady=10)

        # Các trường nhập liệu (2 cột)
        tk.Label(self.frame, text="Tên:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(self.frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.frame, text="Tuổi:").grid(row=0, column=2, padx=5, pady=5)
        self.age_entry = tk.Entry(self.frame)
        self.age_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(self.frame, text="Phòng Ban:").grid(row=1, column=0, padx=5, pady=5)
        self.department_entry = tk.Entry(self.frame)
        self.department_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.frame, text="Vị Trí:").grid(row=1, column=2, padx=5, pady=5)
        self.position_entry = tk.Entry(self.frame)
        self.position_entry.grid(row=1, column=3, padx=5, pady=5)

        tk.Label(self.frame, text="Lương:").grid(row=2, column=0, padx=5, pady=5)
        self.salary_entry = tk.Entry(self.frame)
        self.salary_entry.grid(row=2, column=1, padx=5, pady=5)

        # Khung chứa các nút (Thêm, Sửa, Xóa)
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        # Nút thêm
        self.add_button = tk.Button(button_frame, text="Thêm Nhân Viên", command=self.add_employee)
        self.add_button.grid(row=0, column=0, padx=10)

        # Nút sửa
        self.update_button = tk.Button(button_frame, text="Sửa Nhân Viên", command=self.update_employee)
        self.update_button.grid(row=0, column=1, padx=10)

        # Nút xóa
        self.delete_button = tk.Button(button_frame, text="Xóa Nhân Viên", command=self.delete_employee)
        self.delete_button.grid(row=0, column=2, padx=10)

        # Cây để hiển thị nhân viên
        self.tree = ttk.Treeview(self, columns=("ID", "Tên", "Tuổi", "Phòng Ban", "Vị Trí", "Lương"), show="headings")
        self.tree.pack(pady=10)
        for col in ("ID", "Tên", "Tuổi", "Phòng Ban", "Vị Trí", "Lương"):
            self.tree.heading(col, text=col)

        self.tree.bind("<ButtonRelease-1>", self.on_tree_select)

    def add_employee(self):
        name = self.name_entry.get()
        age = self.age_entry.get()
        department = self.department_entry.get()
        position = self.position_entry.get()
        salary = self.salary_entry.get()

        if name and age and department and position and salary:
            self.employee_list.add_employee(name, age, department, position, salary)
            self.update_treeview()
            self.clear_entries()
        else:
            messagebox.showwarning("Cảnh Báo", "Vui lòng nhập đầy đủ thông tin!")

    def update_employee(self):
        selected_item = self.tree.selection()
        if selected_item:
            index = self.tree.index(selected_item)
            name = self.name_entry.get()
            age = self.age_entry.get()
            department = self.department_entry.get()
            position = self.position_entry.get()
            salary = self.salary_entry.get()

            if name and age and department and position and salary:
                self.employee_list.update_employee(index, name, age, department, position, salary)
                self.update_treeview()
                self.clear_entries()
            else:
                messagebox.showwarning("Cảnh Báo", "Vui lòng nhập đầy đủ thông tin!")
        else:
            messagebox.showwarning("Cảnh Báo", "Vui lòng chọn nhân viên để sửa!")

    def delete_employee(self):
        selected_item = self.tree.selection()
        if selected_item:
            index = self.tree.index(selected_item)
            self.employee_list.delete_employee(index)
            self.update_treeview()
            self.clear_entries()
        else:
            messagebox.showwarning("Cảnh Báo", "Vui lòng chọn nhân viên để xóa!")

    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            index = self.tree.index(selected_item)
            employee = self.employee_list.get_employees()[index]

            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, employee.name)
            self.age_entry.delete(0, tk.END)
            self.age_entry.insert(0, employee.age)
            self.department_entry.delete(0, tk.END)
            self.department_entry.insert(0, employee.department)
            self.position_entry.delete(0, tk.END)
            self.position_entry.insert(0, employee.position)
            self.salary_entry.delete(0, tk.END)
            self.salary_entry.insert(0, employee.salary)

    def update_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for emp in self.employee_list.get_employees():
            self.tree.insert("", "end", values=(emp.emp_id, emp.name, emp.age, emp.department, emp.position, emp.salary))

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.department_entry.delete(0, tk.END)
        self.position_entry.delete(0, tk.END)
        self.salary_entry.delete(0, tk.END)

import tkinter as tk
from tkinter import messagebox, ttk
from enity.employee import Employee
from service.employee_list import EmployeeList
from service.department_list import departmentList
class EmployeeApp(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.employee_list = EmployeeList()
        self.department_list = departmentList()
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
        self.department_combobox = ttk.Combobox(self.frame, state="readonly")
        self.department_combobox.grid(row=1, column=1, padx=5, pady=5)
        self.department_combobox.set("Chọn Phòng Ban") 
        self.load_Department_names()
        tk.Label(self.frame, text="Chức vụ:").grid(row=1, column=2, padx=5, pady=5)
        self.position_combobox = ttk.Combobox(self.frame, state="readonly")  # Tạo Combobox
        self.position_combobox.grid(row=1, column=3, padx=5, pady=5)
        self.set_position_options()
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
        search_frame = tk.Frame(self)
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="Tìm kiếm:").pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, padx=5)

        self.search_button = tk.Button(search_frame, text="Tìm", command=self.search_employee)
        self.search_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = tk.Button(search_frame, text="Làm Mới", command=self.update_treeview)
        self.reset_button.pack(side=tk.LEFT, padx=5)
        # Cây để hiển thị nhân viên
        self.tree = ttk.Treeview(self, columns=("ID", "Tên", "Tuổi", "Phòng Ban", "Chức vụ"), show="headings")
        self.tree.pack(pady=10)

        # Biến để lưu trạng thái sắp xếp
        self.sort_reverse = {col: False for col in ("ID", "Tên", "Tuổi", "Phòng Ban", "Chức vụ")}

        for col in ("ID", "Tên", "Tuổi", "Phòng Ban", "Chức vụ"):
            # Thêm sự kiện sắp xếp khi nhấp vào tiêu đề cột
            self.tree.heading(col, text=col, command=lambda _col=col: self.sort_column(_col, self.sort_reverse[_col]))
            self.tree.column(col, anchor="center")  # Căn giữa nội dung cột
        self.display_employees()
        self.tree.bind("<ButtonRelease-1>", self.on_tree_select)

    def add_employee(self):
        name = self.name_entry.get()
        age = self.age_entry.get()
        department = self.department_combobox.get()
        position = self.position_combobox.get()

        # Kiểm tra điều kiện nhập liệu
        if not name or not age or department == "Chọn Phòng Ban" or not position :
            messagebox.showwarning("Cảnh Báo", "Vui lòng nhập đầy đủ thông tin!")
        elif int(age) < 18 or int(age) > 60:
            messagebox.showwarning("Cảnh Báo", "Tuổi phải lớn hơn 18 và nhỏ hơn 60!")
        elif not age.isdigit()  or int(age) <= 0:
            messagebox.showwarning("Cảnh Báo", "Tuổi và lương phải là số dương!")
        else:
            self.employee_list.add_employee(name, age, department, position)
            self.employee_list.save_to_csv()  # Lưu vào tệp CSV sau khi cập nhật
            self.update_treeview()
            self.clear_entries()
            if hasattr(self.master.master, 'update_employee_list_in_employee_app'):
                self.master.master.update_employee_list_in_employee_app()
        

    def update_employee(self):
        selected_item = self.tree.selection()
        if selected_item:
            index = self.tree.index(selected_item)
            name = self.name_entry.get()
            age = self.age_entry.get()
            department = self.department_combobox.get()
            position = self.position_combobox.get()

            # Kiểm tra điều kiện nhập liệu
            if not name or not age or not department or not position:
                messagebox.showwarning("Cảnh Báo", "Vui lòng nhập đầy đủ thông tin!")
            elif int(age) < 18 or int(age) > 60:
                messagebox.showwarning("Cảnh Báo", "Tuổi phải lớn hơn 18 và nhỏ hơn 60!")
            elif not age.isdigit() or  int(age) <= 0:
                messagebox.showwarning("Cảnh Báo", "Tuổi phải là số dương!")
            else:
                self.employee_list.update_employee(index, name, age, department, position)
                self.employee_list.save_to_csv()  # Lưu vào tệp CSV sau khi cập nhật
                self.update_treeview()
                self.clear_entries()
                if hasattr(self.master.master, 'update_employee_list_in_employee_app'):
                    self.master.master.update_employee_list_in_employee_app()
        else:
            messagebox.showwarning("Cảnh Báo", "Vui lòng chọn nhân viên để sửa!")

    def load_Department_names(self):
        
       Department_names = self.department_list.get_department_names()  # Giả sử có phương thức này
       self.department_combobox['values'] = Department_names
    def delete_employee(self):
        selected_item = self.tree.selection()
        if selected_item:
            index = self.tree.index(selected_item)
            self.employee_list.delete_employee(index)
            self.employee_list.save_to_csv()  # Lưu vào tệp CSV sau khi xóa
            self.update_treeview()
            self.clear_entries()
            if hasattr(self.master.master, 'update_employee_list_in_employee_app'):
                self.master.master.update_employee_list_in_employee_app()
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
            self.department_combobox.set(employee.department)  # Sửa ở đây
            self.position_combobox.delete(0, tk.END)
            self.position_combobox.insert(0, employee.position)

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.department_combobox.set("Chọn Phòng Ban")
        self.position_combobox.delete(0, tk.END)
    def search_employee(self):
        keyword = self.search_entry.get().lower()
        filtered_employees = []

        # Tìm kiếm theo tên trước
        for emp in self.employee_list.get_employees():
            if keyword in emp.name.lower():
                filtered_employees.append(emp)

        # Nếu không tìm thấy nhân viên nào theo tên, tìm kiếm theo phòng ban
        if not filtered_employees:
            for emp in self.employee_list.get_employees():
                if keyword in emp.department.lower():
                    filtered_employees.append(emp)

        # Cập nhật Treeview với danh sách lọc
        self.update_treeview(filtered_employees)

    def sort_column(self, col, reverse):
        # Lấy danh sách nhân viên hiện tại
        employees = self.employee_list.get_employees()

        # Sắp xếp theo cột đã chọn
        if col == "ID":
            employees.sort(key=lambda emp: emp.emp_id, reverse=reverse)
        elif col == "Tên":
            employees.sort(key=lambda emp: emp.name.lower(), reverse=reverse)
        elif col == "Tuổi":
            employees.sort(key=lambda emp: emp.age, reverse=reverse)
        elif col == "Phòng Ban":
            employees.sort(key=lambda emp: emp.department.lower(), reverse=reverse)
        elif col == "Chức vụ":
            employees.sort(key=lambda emp: emp.position.lower(), reverse=reverse)
        # Cập nhật trạng thái sắp xếp
        self.sort_reverse[col] = not reverse

        # Cập nhật Treeview với danh sách đã sắp xếp
        self.update_treeview(employees)
    def update_treeview(self, employees=None):
        # Xóa dữ liệu cũ trong Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Nếu không có danh sách nào được truyền vào, hiển thị toàn bộ nhân viên
        if employees is None:
            employees = self.employee_list.get_employees()

        # Thêm các nhân viên vào Treeview
        for emp in employees:
            self.tree.insert("", "end", values=(emp.emp_id, emp.name, emp.age, emp.department, emp.position))
  
    def display_employees(self):
        # Xóa dữ liệu cũ trong Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Thêm nhân viên vào Treeview
        for emp in self.employee_list.get_employees():
            self.tree.insert("", "end", values=(emp.emp_id, emp.name, emp.age, emp.department, emp.position))
    def update_department_list(self, department_list):
        self.department_combobox['values'] = [dept.name for dept in department_list]
        print("Danh sách phòng ban đã được cập nhật.")
    def load_Department_names(self):
        
        Department_names = self.department_list.get_department_names()  # Giả sử có phương thức này
        self.department_combobox['values'] = Department_names
    def set_position_options(self):
        # Cập nhật danh sách các chức vụ ở đây
        positions = [
            "Quản lý",
            "Trưởng phòng",
            "Nhân viên kế toán",
            "Kỹ sư",
            "Nhân viên",
            "Nhân viên hành chính",
            "Trợ lý",
            "Chuyên viên"
        ]  # Danh sách chức vụ
        self.position_combobox['values'] = positions
        self.position_combobox.set(positions[0])
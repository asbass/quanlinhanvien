import tkinter as tk
from tkinter import messagebox, ttk
from enity.employee import Employee
from service.employee_list import EmployeeList
from service.department_list import departmentList
from service.posittion_list import PositionList
from .app_payroll import PayrollApp
class EmployeeApp(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.employee_list = EmployeeList()
        self.department_list = departmentList()
        self.postion_list = PositionList()
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
        self.position_combobox.set("Chọn Chức Vụ")
        self.load_Postions_names()
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
        if not name or not age or department == "Chọn Phòng Ban" or not position:
            messagebox.showwarning("Cảnh Báo", "Vui lòng nhập đầy đủ thông tin!")
        elif not age.isdigit():
            messagebox.showwarning("Cảnh Báo", "Tuổi phải là số")
        elif int(age) < 18 or int(age) > 60:
            messagebox.showwarning("Cảnh Báo", "Tuổi phải lớn hơn 18 và nhỏ hơn 60!")
        else:
            try:
                # Thêm nhân viên vào danh sách
                self.employee_list.add_employee(name, age, department, position)
                self.update_treeview()  # Cập nhật cây hiển thị danh sách nhân viên
                self.clear_entries()  # Xóa các trường nhập liệu
                # Cập nhật danh sách nhân viên từ cơ sở dữ liệu
                if hasattr(self.master.master, 'update_employee_list_in_employee_app'):
                    self.master.master.update_employee_list_in_employee_app()
                    print("Nhân viên đã được thêm thành công và danh sách đã được cập nhật.")
            except Exception as e:
                print(f"Lỗi khi thêm nhân viên: {e}")
    def update_employee(self):
        selected_item = self.tree.selection()  # This returns a tuple of selected item IDs
        if not selected_item:
            messagebox.showwarning("Cảnh Báo", "Vui lòng chọn nhân viên để sửa!")
            return

        # Get the first selected item ID
        selected_item_id = selected_item[0]
        
        # Now use this ID to fetch the employee's data
        # Get the values of the selected item directly from the tree
        emp_values = self.tree.item(selected_item_id)["values"]  
        emp_id = emp_values[0]  # Get the emp_id from the values

        # Fetch values from input fields
        name = self.name_entry.get().strip()
        age = self.age_entry.get().strip()
        department = self.department_combobox.get()
        position = self.position_combobox.get()

        # Check input conditions
        if not name or not age or not department or not position:
            messagebox.showwarning("Cảnh Báo", "Vui lòng nhập đầy đủ thông tin!")
        elif not age.isdigit() or not (18 <= int(age) <= 60):
            messagebox.showwarning("Cảnh Báo", "Tuổi phải lớn hơn 18 và nhỏ hơn 60!")
        else:
            try:
                # Call the update_employee method with the appropriate parameters
                self.employee_list.update_employee(emp_id, name, age, department, position)  
                self.update_treeview()  # Refresh the interface
                self.clear_entries()  # Clear input fields
                if hasattr(self.master.master, 'update_employee_list_in_employee_app'):
                    self.master.master.update_employee_list_in_employee_app()
                    print("Nhân viên đã được thêm thành công và danh sách đã được cập nhật.")
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))
                print(str(e))


    def load_Postions_names(self):
       Postions_names = self.postion_list.get_position_names()  # Giả sử có phương thức này
       self.position_combobox['values'] = Postions_names
    def delete_employee(self):
        selected_item = self.tree.selection()
        if selected_item:
            confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa nhân viên này?")
            if confirm:
                emp_id = self.tree.item(selected_item[0], 'values')[0]  # Lấy ID nhân viên từ Treeview
                self.employee_list.delete_employee(emp_id)  # Gọi phương thức xóa
                self.update_treeview()  # Cập nhật giao diện sau khi xóa
                if hasattr(self.master.master, 'update_employee_list_in_employee_app'):
                    self.master.master.update_employee_list_in_employee_app()
                    print("Nhân viên đã được thêm thành công và danh sách đã được cập nhật.")
        else:
            messagebox.showwarning("Cảnh Báo", "Vui lòng chọn nhân viên để xóa!")

    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        
        if selected_item:
            # Lấy dữ liệu từ dòng đã chọn
            selected_employee = self.tree.item(selected_item)["values"]
            # Gán các giá trị từ dòng đã chọn vào các trường nhập liệu
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, selected_employee[1])  # Giá trị Tên ở cột thứ 2

            self.age_entry.delete(0, tk.END)
            self.age_entry.insert(0, selected_employee[2])  # Giá trị Tuổi ở cột thứ 3

            self.department_combobox.set(selected_employee[3])  # Giá trị Phòng Ban ở cột thứ 4

            self.position_combobox.set(selected_employee[4])  # Giá trị Chức vụ ở cột thứ 5

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.department_combobox.set("Chọn Phòng Ban")
        self.position_combobox.set("Chọn Chức Vụ")
        self.search_entry.delete(0, tk.END)

    def search_employee(self):
        keyword = self.search_entry.get().lower()
        filtered_employees = []

        # Tìm kiếm theo tên trước
        for emp in self.employee_list.get_employees():
            if keyword in emp.name.lower():  # Tìm kiếm theo tên (chuyển tên về chữ thường)
                filtered_employees.append(emp)

        # Nếu không tìm thấy nhân viên nào theo tên, tìm kiếm theo phòng ban
        if not filtered_employees:
            for emp in self.employee_list.get_employees():
                if keyword in emp.department.lower():  # Tìm kiếm theo phòng ban
                    filtered_employees.append(emp)

        # Nếu vẫn chưa tìm thấy, tìm kiếm từ cơ sở dữ liệu
        if not filtered_employees:
            query = "SELECT * FROM Employee WHERE LOWER(name) LIKE %s OR LOWER(department) LIKE %s"
            search_pattern = f"%{keyword}%"  # Tạo mẫu tìm kiếm
            results = self.employee_list.db.fetch_all(query, (search_pattern, search_pattern))

            # Chuyển đổi kết quả từ truy vấn thành đối tượng Employee
            for row in results:
                emp = Employee(row['name'], row['age'], row['department_id'], row['position_id'])
                filtered_employees.append(emp)

        # Hiển thị danh sách nhân viên đã lọc, nếu không có kết quả thì thông báo
        if filtered_employees:
            self.update_treeview(filtered_employees)
        else:
            messagebox.showinfo("Thông báo", "Không tìm thấy nhân viên!")
            self.update_treeview()  # Hiển thị lại toàn bộ danh sách nhân viên nếu không tìm thấy

        print([emp.name for emp in filtered_employees])  # Kiểm tra xem nhân viên nào được tìm thấy
        

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
        self.clear_entries()
        # Thêm các nhân viên vào Treeview
        for emp in employees:
            department_name = self.employee_list.get_department_name_by_id(emp["department_id"])
            positons_name = self.employee_list.get_position_name_by_id(emp["position_id"])
            # Thêm thông tin nhân viên vào Treeview
            self.tree.insert("", "end", values=(
                emp['emp_id'], 
                emp["name"], 
                emp["age"], 
                department_name,  # Hiển thị tên phòng ban
                positons_name
            ))
  
    def display_employees(self):
    # Xóa dữ liệu cũ trong Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Thêm nhân viên vào Treeview
        for emp in self.employee_list.get_employees():
            # Lấy tên phòng ban từ department_id
            department_name = self.employee_list.get_department_name_by_id(emp["department_id"])
            positons_name = self.employee_list.get_position_name_by_id(emp["position_id"])
            # Thêm thông tin nhân viên vào Treeview
            self.tree.insert("", "end", values=(
                emp['emp_id'], 
                emp["name"], 
                emp["age"], 
                department_name,  # Hiển thị tên phòng ban
                positons_name
            ))
    def update_positon_list(self, Position_names):
        self.position_combobox['values'] = Position_names
        print("Danh sách phòng ban đã được cập nhật.")
    def update_department_list(self, department_list):
        self.department_combobox['values'] = department_list
        print("Danh sách phòng ban đã được cập nhật.")

    def load_Department_names(self):
        Department_names = self.department_list.get_department_names()  # Giả sử có phương thức này
        self.department_combobox['values'] = Department_names

    def close_connection(self):
        self.employee_list.close_connection()  # Đóng kết nối từ departmentList
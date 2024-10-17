import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from service.employee_list import EmployeeList  # Đảm bảo đường dẫn này chính xác
from service.Payroll_list import PayrollList
from enity.employee import Employee
class PayrollApp(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Lưu danh sách nhân viên
        self.employee_list = EmployeeList()  # Khởi tạo danh sách nhân viên
        self.payroll_list = PayrollList()
        # Thiết lập hệ số lương cho từng chức vụ
        self.position_salary_factors = {
            "Quản lý": 1.5,
            "Trưởng phòng": 1.4,
            "Nhân viên kế toán": 1.2,
            "Kỹ sư": 1.3,
            "Nhân viên": 1.0,
            "Nhân viên hành chính": 1.0,
            "Trợ lý": 0.9,
            "Chuyên viên": 1.1,
        }
        self.is_employee_list_loaded = False

        # Khung nhập liệu
        self.frame = tk.Frame(self)
        self.frame.pack(pady=10)

        # Nhập ID Nhân Viên
        tk.Label(self.frame, text="ID Nhân Viên:").grid(row=0, column=0, padx=5, pady=5)
        self.id_entry = tk.Entry(self.frame,state='readonly') 
        self.id_entry.grid(row=0, column=1, padx=5, pady=5)

        # Nhập tháng
        tk.Label(self.frame, text="Tháng:").grid(row=1, column=0, padx=5, pady=5)
        self.month_entry = ttk.Combobox(self.frame, values=[i for i in range(1, 13)], state="readonly")
        self.month_entry.grid(row=1, column=1, padx=5, pady=5)

        # Tự động chọn tháng 1
        self.month_entry.current(0)  # Chọn tháng 1 (chỉ số 0 trong danh sách)

        # Nhập năm
        tk.Label(self.frame, text="Năm:").grid(row=2, column=0, padx=5, pady=5)
        self.year_entry = tk.Entry(self.frame)
        self.year_entry.insert(0, str(datetime.now().year))  # Đặt năm hiện tại
        self.year_entry.grid(row=2, column=1, padx=5, pady=5)

        # Nhập tên nhân viên
        tk.Label(self.frame, text="Tên Nhân Viên:").grid(row=3, column=0, padx=5, pady=5)
        employee_names = self.employee_list.get_employee_names()
        self.employee_name_entry = ttk.Combobox(self.frame, values=employee_names, state="readonly")
        self.employee_name_entry.grid(row=3, column=1, padx=5, pady=5)
        self.employee_name_entry.bind("<<ComboboxSelected>>", self.on_employee_selected)
        # Nhập chức vụ
        tk.Label(self.frame, text="Chức vụ:").grid(row=4, column=0, padx=5, pady=5)
        self.position_entry = tk.Entry(self.frame, state='readonly')  # Trường chức vụ chỉ đọc
        self.position_entry.grid(row=4, column=1, padx=5, pady=5)

        # Nhập lương cơ bản
        tk.Label(self.frame, text="Lương Cơ Bản (VNĐ):").grid(row=5, column=0, padx=5, pady=5)
        self.basic_salary_entry = tk.Entry(self.frame, state='readonly')  # Trường chỉ đọc
        self.basic_salary_entry.grid(row=5, column=1, padx=5, pady=5)

        # Nhập lương thưởng
        tk.Label(self.frame, text="Lương Thưởng (VNĐ):").grid(row=6, column=0, padx=5, pady=5)
        self.bonus_salary_entry = tk.Entry(self.frame)  # Trường nhập lương thưởng
        self.bonus_salary_entry.grid(row=6, column=1, padx=5, pady=5)
        self.bonus_salary_entry.bind("<KeyRelease>", self.on_key_release)  # Tính lương khi gõ

        # Nhập số ngày nghỉ
        tk.Label(self.frame, text="Số Ngày Nghỉ:").grid(row=7, column=0, padx=5, pady=5)
        self.days_off_entry = tk.Entry(self.frame)
        self.days_off_entry.grid(row=7, column=1, padx=5, pady=5)
        self.days_off_entry.bind("<KeyRelease>", self.on_key_release)  # Tính lương khi gõ

        # Nhập lương thực nhận
        tk.Label(self.frame, text="Lương Thực Nhận (VNĐ):").grid(row=8, column=0, padx=5, pady=5)
        self.net_salary_entry = tk.Entry(self.frame, state='readonly')  # Trường chỉ đọc cho lương thực nhận
        self.net_salary_entry.grid(row=8, column=1, padx=5, pady=5)

        # Nút thêm bảng lương
        self.add_button = tk.Button(self.frame, text="Thêm Bảng Lương", command=self.add_payroll)
        self.add_button.grid(row=9, column=0, padx=10)

        # Cây để hiển thị bảng lương
        self.tree = ttk.Treeview(self, columns=('ID', 'Tên', 'Vị trí', 'Tháng', 'Năm', 'Lương cơ bản', 'Thưởng', 'Ngày Nghỉ', 'Lương thực nhận'), show='headings')
        self.tree.pack(pady=20)

        # Đặt tiêu đề cho các cột
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor='center')

        # Tải và hiển thị dữ liệu bảng lương
        self.load_and_display_payroll()
    def load_and_display_payroll(self):
        """Tải bảng lương và hiển thị trong Treeview."""
        for payroll in self.payroll_list.get_Payroll():
            self.tree.insert('', 'end', values=(
                payroll.emp_id,
                payroll.name,
                payroll.position,
                payroll.month,
                payroll.year,
                payroll.basic_salary,
                payroll.reward,
                payroll.day_off,
                payroll.net_salary
            ))
    def calculate_salary(self, event=None):
        """Tính lương thực nhận."""
        try:
            # Lấy lương cơ bản và lương thưởng từ các trường nhập liệu
            basic_salary_str = self.basic_salary_entry.get().replace(',', '').replace(' VND', '')
            bonus_salary_str = self.bonus_salary_entry.get().replace(',', '').replace(' VND', '')
            days_off = self.days_off_entry.get()

            # Chuyển đổi sang số
            basic_salary = float(basic_salary_str) if basic_salary_str else 0
            bonus_salary = float(bonus_salary_str) if bonus_salary_str else 0
            days_off = int(days_off) if days_off.isdigit() else 0

            # Tính lương thực nhận
            net_salary = (basic_salary + bonus_salary) - (days_off * (basic_salary / 30))
            net_salary = round(net_salary)
            self.net_salary_entry.config(state='normal')  # Cho phép chỉnh sửa lương thực nhận
            self.net_salary_entry.delete(0, tk.END)
            self.net_salary_entry.insert(0, f"{max(net_salary, 0):,} VND")  # Đảm bảo lương không âm và định dạng
            self.net_salary_entry.config(state='readonly')  # Đặt lại thành chỉ đọc
        except ValueError:
            # Xử lý trường hợp nhập liệu không hợp lệ
            self.net_salary_entry.delete(0, tk.END)

    def add_payroll(self):
        """Thêm bảng lương vào danh sách."""
        employee_id = self.id_entry.get().strip()
        month = self.month_entry.get().strip()
        year = self.year_entry.get().strip()
        employee_name = self.employee_name_entry.get().strip()
        position = self.position_entry.get().strip()
        basic_salary = self.basic_salary_entry.get().strip()
        bonus_salary = self.bonus_salary_entry.get().strip()
        days_off = self.days_off_entry.get().strip()
        net_salary = self.net_salary_entry.get().strip()

        # Kiểm tra xem nhân viên đã có bảng lương cho tháng và năm này chưa
        for item in self.tree.get_children():
            values = self.tree.item(item, "values")
            if values[0] == employee_id and values[1] == str(month) and values[2] == str(year):
                messagebox.showerror("Lỗi", "Nhân viên đã có bảng lương cho tháng này trong năm rồi.")
                return  # Ngừng thêm bảng lương nếu đã tồn tại

        # Thêm bảng lương vào Treeview
        self.tree.insert("", "end", values=(employee_id, employee_name, position, month, year, basic_salary, bonus_salary, days_off, net_salary))

        # Chuyển đổi các giá trị cần thiết cho việc thêm vào payroll_list
        try:
            reward = int(bonus_salary.replace(',', '').replace(' VND', ''))  # Lương thưởng
            day_off = int(days_off)  # Số ngày nghỉ
        except ValueError:
            messagebox.showerror("Lỗi", "Giá trị lương thưởng hoặc số ngày nghỉ không hợp lệ.")
            return

        # Tìm kiếm nhân viên trong danh sách nhân viên
        employee_data = self.employee_list.get_employee_info(employee_name)  # Giả sử có phương thức này
        if employee_data is None:  # Kiểm tra nhân viên có tồn tại không
            messagebox.showerror("Lỗi", "Không tìm thấy nhân viên với tên này.")
            return

        # Kiểm tra xem employee_data là từ điển và tạo đối tượng Employee
        if isinstance(employee_data, dict):
            # Lấy các thông tin cần thiết từ từ điển
            emp_id = employee_data.get('emp_id')  # Lấy ID
            name = employee_data.get('name')  # Lấy tên
            age = employee_data.get('age')  # Lấy tuổi
            department = employee_data.get('department')  # Lấy phòng ban
            position = employee_data.get('position')  # Lấy vị trí

            # Tạo đối tượng Employee với các tham số đúng
            employee = Employee(name, age, department, position)
        else:
            messagebox.showerror("Lỗi", "Thông tin nhân viên không hợp lệ.")
            return

        # Gọi phương thức để thêm bảng lương
        self.payroll_list.add_payroll(employee, month, year, day_off, basic_salary, reward, net_salary)
        self.employee_list.save_to_csv()  # Lưu vào tệp CSV sau khi cập nhật
        
        # Xóa các trường nhập liệu
        self.clear_entries()
    def update_employee_position(self):
        self.is_employee_list_loaded = False
        self.load_employee_list()
    def update_employee_list(self, employee_list):
        self.employee_name_entry['values'] = [emp.name for emp in employee_list]
        print("Danh sách nhân viên đã được cập nhật.")
    def on_key_release(self, event):
        if self.days_off_entry.get().isdigit() or self.bonus_salary_entry.get().isdigit():
            self.calculate_salary()
    def clear_entries(self):
        """Xóa các trường nhập liệu."""
        self.id_entry.delete(0, tk.END)
        self.employee_name_entry.delete(0, tk.END)
        self.position_entry.delete(0, tk.END)
        self.basic_salary_entry.delete(0, tk.END)
        # Xóa các trường nhập liệu
        self.bonus_salary_entry.delete(0, tk.END)  # Xóa trường lương thưởng
        self.days_off_entry.delete(0, tk.END)  # Xóa trường số ngày nghỉ

        # Đặt giá trị mới cho các trường nhập liệu
        self.bonus_salary_entry.insert(0, "1,000,000 VND")  # Đặt lương thưởng là 1 triệu
        self.days_off_entry.insert(0, "0")  # Đặt số ngày nghỉ là 0
        self.net_salary_entry.delete(0, tk.END)
        self.month_entry.set('1')  # Đặt lại tháng về mặc định
        self.year_entry.delete(0, tk.END)
        self.year_entry.insert(0, str(datetime.now().year))  # Đặt lại năm hiện tại

    def on_employee_selected(self, event):
         # Lấy thông tin nhân viên đã chọn từ combobox hoặc listbox
        selected_employee_name = self.employee_name_entry.get()  # Hoặc sử dụng listbox tùy thuộc vào cách bạn thiết lập giao diện
        # Tìm nhân viên tương ứng trong danh sách nhân viên
        selected_employee = self.employee_list.get_employee_by_name(selected_employee_name)
        if selected_employee:
            emp_id = selected_employee.emp_id
            position = selected_employee.position

            # Tính lương cơ bản dựa trên chức vụ
            salary_factor = self.position_salary_factors.get(position, 1)
            basic_salary = 5000000 * salary_factor  # Lương cơ bản

            # Cập nhật giao diện với các thông tin nhân viên
            self.id_entry.config(state='normal')
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, emp_id)
            self.id_entry.config(state='readonly')

            self.position_entry.config(state='normal')
            self.position_entry.delete(0, tk.END)
            self.position_entry.insert(0, position)
            self.position_entry.config(state='readonly')

            # Cập nhật lương cơ bản
            self.basic_salary_entry.config(state='normal')
            self.basic_salary_entry.delete(0, tk.END)
            self.basic_salary_entry.insert(0, f"{basic_salary:,} VND")
            self.basic_salary_entry.config(state='readonly')

            # Cập nhật lương thưởng
            bonus_salary = 1000000  # Giả sử thưởng cố định 1 triệu
            self.bonus_salary_entry.config(state='normal')
            self.bonus_salary_entry.delete(0, tk.END)
            self.bonus_salary_entry.insert(0, f"{bonus_salary:,} VND")
            self.bonus_salary_entry.config(state='normal')
            self.update_employee_list(self.employee_list.get_employees())  
            # Tính lương thực nhận
            self.calculate_salary()  # Gọi lại để cập nhật lương thực nhận

    def load_employee_list(self):
        """Tải danh sách nhân viên chỉ một lần."""
        if not self.is_employee_list_loaded:
            self.employee_list.clear_employee_list()
            self.employee_list.load_Employee()
            self.is_employee_list_loaded = True
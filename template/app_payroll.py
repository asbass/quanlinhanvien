import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from service.employee_list import EmployeeList  # Đảm bảo đường dẫn này chính xác
from service.Payroll_list import PayrollList
from enity.employee import Employee
from service.posittion_list import PositionList
from service.woking_time_service import WorkingTimeService
import uuid
import re

class PayrollApp(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Lưu danh sách nhân viên
        self.employee_list = EmployeeList()  # Khởi tạo danh sách nhân viên
        self.payroll_list = PayrollList()
        self.posittion_list = PositionList()
        self.workingtime_list = WorkingTimeService()
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
        self.month_entry.bind("<<ComboboxSelected>>", self.on_employee_selected)
        self.month_entry.current(0)  # Chọn tháng 1 (chỉ số 0 trong danh sách)
        # Nhập năm
        tk.Label(self.frame, text="Năm:").grid(row=2, column=0, padx=5, pady=5)
        self.year_entry = tk.Entry(self.frame)
        self.year_entry.insert(0, str(datetime.now().year))  # Đặt năm hiện tại
        self.year_entry.grid(row=2, column=1, padx=5, pady=5)
        # Nhập tên nhân viên
        tk.Label(self.frame, text="Tên Nhân Viên:").grid(row=3, column=0, padx=5, pady=5)
        self.employee_name_entry = ttk.Combobox(self.frame, state="readonly")
        self.employee_name_entry.grid(row=3, column=1, padx=5, pady=5)
        self.employee_name_entry.set("Chọn Tên Nhân Viên") 
        self.employee_name_entry.bind("<<ComboboxSelected>>", self.on_employee_selected)
        self.loads_employee_list()
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
        self.load_payroll_data()
        # Tải và hiển thị dữ liệu bảng lương
  
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
            # Đảm bảo so sánh đúng các giá trị
            if (values[0] == employee_id and  # employee_id
                values[3] == str(month) and   # month
                values[4] == str(year)):      # year
                messagebox.showerror("Lỗi", "Nhân viên đã có bảng lương cho tháng này trong năm rồi.")
                return  # Ngừng thêm bảng lương nếu đã tồn tại
        # Chuyển đổi các giá trị cần thiết cho việc thêm vào payroll_list
        try:
            # Kiểm tra nếu chuỗi lương và thưởng là số hợp lệ (bỏ đi dấu phẩy và ký tự "VND")            
            # Kiểm tra định dạng số hợp lệ cho lương cơ bản và thưởng
            basic_salary = re.sub(r'[^\d]', '', basic_salary)  # Bỏ đi ký tự không phải số
            bonus_salary = re.sub(r'[^\d]', '', bonus_salary)
            net_salary = re.sub(r'[^\d]', '', net_salary)
            
            # Chuyển đổi thành số nguyên
            reward = float(bonus_salary)  # Lương thưởng
            day_off = int(days_off)  # Số ngày nghỉ
            basic_salary = float(basic_salary)  # Lương cơ bản
            net_salary = float(net_salary)  # Lương thực nhận
        except ValueError:
            messagebox.showerror("Lỗi", "Giá trị lương, thưởng hoặc số ngày nghỉ không hợp lệ.")
            return
        basic_salary_formatted = f"{basic_salary:,.0f} VNĐ"
        bonus_salary_formatted = f"{reward:,.0f} VNĐ"
        net_salary_formatted = f"{net_salary:,.0f} VNĐ"
        # Tạo payroll_id bằng UUID

        # Thêm bảng lương vào Treeview
        self.tree.insert("", "end", values=(employee_id, employee_name, position, month, year, basic_salary_formatted, bonus_salary_formatted, days_off, net_salary_formatted))

        # Gọi phương thức để thêm bảng lương vào cơ sở dữ liệu
        try:

            self.payroll_list.add_payroll( employee_id, month, year, day_off, basic_salary, reward, net_salary)
            print("Payroll record added successfully.")
            if hasattr(self.master.master, 'update_Payroll_list_in_Payroll_app'):
                    self.master.master.update_Payroll_list_in_Payroll_app()
                    print("Nhân viên đã được thêm thành công và danh sách đã được cập nhật.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi thêm bảng lương: {e}")
        self.clear_entries()
    # def update_employee_position(self, position_list):
    #     self.employee_name_entry['values'] = position_list
    #     print("Danh sách phòng ban đã được cập nhật.")
            
    def loads_employee_list(self):
        employee_names = self.employee_list.get_employee_names()  # Get the latest employee names
        self.employee_name_entry['values'] = employee_names  # Update the UI component
        self.employee_name_entry.update()
        self.employee_name_entry.delete(0, tk.END)
        print("Employee list updated with the latest data from the database.")
    def update_employee_list(self, employee_list):
        self.employee_name_entry['values'] = employee_list  # Cập nhật ComboBox hoặc các thành phần khác
        print("Danh sách nhân viên đã được cập nhật trong PayrollApp.")
        if employee_list:
            self.employee_name_entry.current(0)  # Tùy chọn chọn nhân viên đầu tiên
        
        print("Danh sách nhân viên đã được cập nhật trong PayrollApp.")
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
        selected_employee_name = self.employee_name_entry.get()
            # Cập nhật employee_name_entry
        self.employee_name_entry.config(state='normal')
        self.employee_name_entry.delete(0, tk.END)
        self.employee_name_entry.insert(0, selected_employee_name)  # Cập nhật tên nhân viên
        self.employee_name_entry.config(state='readonly')
        # Tìm nhân viên tương ứng trong danh sách nhân viên
        selected_employee = self.employee_list.get_employee_id_by_name(selected_employee_name)
        print(selected_employee)

        if selected_employee:
            emp_id = selected_employee['emp_id']  # Lấy emp_id từ kết quả
            position_id = selected_employee['position_id']  # Lấy position_id từ kết quả
            
            # Lấy thông tin chức vụ từ position_id
            position = self.posittion_list.get_position_by_emp_id(position_id)
            
            if position:  # Đảm bảo position là một đối tượng Position
                print("Chức vụ:", position.name)
                salary_multiplier = position.salary_multiplier  # Lấy salary_multiplier từ đối tượng Position
            else:
                print("Không tìm thấy chức vụ cho nhân viên với emp_id:", emp_id)
                salary_multiplier = 1  # Thiết lập giá trị mặc định nếu không tìm thấy chức vụ

            # Tính lương cơ bản dựa trên salary_multiplier
            basic_salary = 5000000 * salary_multiplier  # Lương cơ bản
            # Lấy tháng và năm từ giao diện
            month = int(self.month_entry.get())  # Lấy tháng từ combobox
            year = int(self.year_entry.get())    # Lấy năm từ entry

            days_off = self.workingtime_list.get_days_off(emp_id,month,year)
            
            self.days_off_entry.config(state='normal')
            self.days_off_entry.delete(0, tk.END)
            self.days_off_entry.insert(0, days_off)  # Cập nhật số ngày nghỉ
            self.days_off_entry.config(state='readonly')
            # Cập nhật giao diện với các thông tin nhân viên
            self.id_entry.config(state='normal')
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, emp_id)
            self.id_entry.config(state='readonly')

            self.position_entry.config(state='normal')
            self.position_entry.delete(0, tk.END)
            self.position_entry.insert(0, position.name)  # Cập nhật tên chức vụ
            self.position_entry.config(state='readonly')

            # Cập nhật lương cơ bản
            self.basic_salary_entry.config(state='normal')
            self.basic_salary_entry.delete(0, tk.END)
            self.basic_salary_entry.insert(0, f"{int(basic_salary):,} VND")
            self.basic_salary_entry.config(state='readonly')

            # Cập nhật lương thưởng
            bonus_salary = 1000000  # Giả sử thưởng cố định 1 triệu
            self.bonus_salary_entry.config(state='normal')
            self.bonus_salary_entry.delete(0, tk.END)
            self.bonus_salary_entry.insert(0, f"{bonus_salary:,} VND")
            self.bonus_salary_entry.config(state='normal')

            # Cập nhật danh sách nhân viên
            # self.update_employee_list(self.employee_list.get_employees())  

            # Tính lương thực nhận
            self.calculate_salary()  # Gọi lại để cập nhật lương thực nhận

        else:
            print("Không tìm thấy nhân viên với tên:", selected_employee_name)

    def close_connection(self):
        self.payroll_list.close_connection()  # Đóng kết nối từ departmentList
    def load_payroll_data(self):
        for payroll in self.payroll_list.load_payrolls():
            # Sử dụng payroll.emp_id thay vì payroll["emp_id"]
            employee_name = self.employee_list.get_employee_name_by_id(payroll.emp_id)
            postions_id= self.employee_list.get_position_id_from_employee(payroll.emp_id)
            positons_name = self.employee_list.get_position_name_by_id(postions_id)
            basic_salary_formatted = f"{payroll.basic_salary:,.0f} VNĐ"
            reward_formatted = f"{payroll.reward:,.0f} VNĐ"
            net_salary_formatted = f"{payroll.net_salary:,.0f} VNĐ"
            self.tree.insert("", "end", values=(
                payroll.emp_id,
                employee_name,
                positons_name,
                payroll.month,
                payroll.year,
                basic_salary_formatted,
                reward_formatted,
                payroll.day_off,
                net_salary_formatted
            ))
        
           
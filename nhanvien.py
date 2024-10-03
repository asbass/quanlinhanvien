import streamlit as st
from employee_data import Employee  # Nhập lớp Employee từ tệp employee_data.py
import pandas as pd
import altair as alt

# Tiêu đề ứng dụng
st.title("Quản Lý Nhân Viên")

# Khởi tạo dữ liệu giả định
if 'employees' not in st.session_state:
    employee1 = Employee(emp_id="001", name="Nguyễn Văn A", position="Nhân viên", age=30, salary=5000000.0)
    employee2 = Employee(emp_id="002", name="Trần Thị B", position="Quản lý", age=35, salary=7000000.0)
    employee3 = Employee(emp_id="003", name="Lê Văn C", position="Kỹ sư", age=28, salary=6000000.0)
    employee4 = Employee(emp_id="004", name="Phạm Thị D", position="Nhân viên", age=25, salary=4000000.0)
    employee5 = Employee(emp_id="005", name="Đặng Văn E", position="Giám đốc", age=40, salary=12000000.0)

    st.session_state.employees = [employee1, employee2, employee3, employee4, employee5]

# Tạo các tab cho các chức năng
tabs = st.tabs(["Thêm Nhân Viên", "Sửa Nhân Viên", "Danh Sách Nhân Viên", "Thống Kê"])

# Hàm kiểm tra xem chuỗi có phải là chữ hay không
def is_alpha(string):
    return string.isalpha() or all(char.isspace() for char in string)

# Tab Thêm Nhân Viên
with tabs[0]:
    st.subheader("Thêm Nhân Viên")
    with st.form("form_employee"):
        emp_id = st.text_input("ID")
        name = st.text_input("Họ Tên")
        position = st.text_input("Chức Vụ")
        age = st.number_input("Tuổi", min_value=18, max_value=100)
        salary = st.number_input("Lương", min_value=1000000.0, format="%.2f")

        submitted = st.form_submit_button("Thêm Nhân Viên")
        if submitted:
            # Kiểm tra xem ID đã tồn tại hay chưa
            if emp_id in [emp.emp_id for emp in st.session_state.employees]:
                st.error("ID này đã tồn tại! Vui lòng nhập ID khác.")
            elif not emp_id or not name or not position or age <= 0 or salary <= 100000:
                st.error("Tất cả các trường không được để trống và lương phải lớn hơn 100.000.")
            elif not is_alpha(name):
                st.error("Họ Tên phải là chữ và không chứa số.")
            elif not is_alpha(position):
                st.error("Chức Vụ phải là chữ và không chứa số.")
            else:
                new_employee = Employee(emp_id, name, position, age, salary)
                st.session_state.employees.append(new_employee)
                st.success("Nhân viên đã được thêm thành công!")

# Tab Sửa Nhân Viên
with tabs[1]:
    st.subheader("Sửa Nhân Viên")
    
    if st.session_state.employees:
        id_to_edit = st.selectbox("Chọn ID nhân viên để sửa", [emp.emp_id for emp in st.session_state.employees])
        emp_to_edit = next(emp for emp in st.session_state.employees if emp.emp_id == id_to_edit)

        with st.form("form_edit_employee"):
            new_name = st.text_input("Họ Tên", value=emp_to_edit.name)
            new_position = st.text_input("Chức Vụ", value=emp_to_edit.position)
            new_age = st.number_input("Tuổi", min_value=18, max_value=100, value=emp_to_edit.age)
            new_salary = st.number_input("Lương", min_value=0.0, step=100000.0, value=emp_to_edit.salary, format="%.2f")

            submitted = st.form_submit_button("Sửa Nhân Viên")
            if submitted:
                emp_to_edit.name = new_name
                emp_to_edit.position = new_position
                emp_to_edit.age = new_age
                emp_to_edit.salary = new_salary
                st.success("Thông tin nhân viên đã được cập nhật.")

# Tab Danh Sách Nhân Viên
# Tab Danh Sách Nhân Viên
with tabs[2]:
    st.subheader("Danh Sách Nhân Viên")
    
    # Tìm kiếm theo tên
    search_name = st.text_input("Tìm kiếm theo tên")

    # Lựa chọn sắp xếp
    sort_by = st.selectbox("Sắp xếp theo", ["Tên", "Lương"])

    # Nút để thực hiện sắp xếp
    sort_button = st.button("Sắp xếp")

    # Lọc danh sách nhân viên
    filtered_employees = [emp for emp in st.session_state.employees if search_name.lower() in emp.name.lower()]

    # Nếu nút sắp xếp được nhấn
    if sort_button:
        if sort_by == "Tên":
            filtered_employees.sort(key=lambda emp: emp.name)
        else:
            filtered_employees.sort(key=lambda emp: emp.salary, reverse=True)

    # Hiển thị danh sách nhân viên
    if filtered_employees:
        for emp in filtered_employees:
            col1, col2 = st.columns([8, 2])
            with col1:
                st.write(f"**ID:** {emp.emp_id}  |  **Họ Tên:** {emp.name}  |  **Chức Vụ:** {emp.position}  |  **Tuổi:** {emp.age}  |  **Lương:** {emp.salary:.2f}")
            with col2:
                # Nút Xóa
                if st.button("Xóa", key=f"xoa_{emp.emp_id}"):  # Duy nhất key cho mỗi nút Xóa
                    st.session_state.employees.remove(emp)
    else:
        st.write("Không tìm thấy nhân viên nào.")

# Tab Thống Kê
with tabs[3]:
    st.subheader("Thống Kê Nhân Viên")

    # Tạo DataFrame từ danh sách nhân viên
    employee_df = pd.DataFrame([vars(emp) for emp in st.session_state.employees])

    # Tính toán thống kê
    total_employees = len(st.session_state.employees)
    average_salary = employee_df["salary"].mean()
    highest_salary = employee_df["salary"].max()
    lowest_salary = employee_df["salary"].min()

    # Định dạng các giá trị tiền tệ với phân cách hàng nghìn và đơn vị VND
    formatted_average_salary = f"{average_salary:,.0f} VND"
    formatted_highest_salary = f"{highest_salary:,.0f} VND"
    formatted_lowest_salary = f"{lowest_salary:,.0f} VND"

    # Hiển thị các thông tin thống kê bằng cách sử dụng các cột để phân chia thông tin
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Tổng số nhân viên", total_employees)

    with col2:
        st.metric("Lương trung bình", formatted_average_salary)

    with col3:
        st.metric("Lương cao nhất", formatted_highest_salary)

    with col4:
        st.metric("Lương thấp nhất", formatted_lowest_salary)

    # 1. Biểu đồ cột - Lương trung bình theo chức vụ
    st.write("### Lương trung bình theo chức vụ:")
    average_salary_by_position = employee_df.groupby("position")["salary"].mean().reset_index()
    bar_chart = alt.Chart(average_salary_by_position).mark_bar().encode(
        x=alt.X('position:N', title="Chức Vụ"),
        y=alt.Y('salary:Q', title="Lương Trung Bình"),
        tooltip=['position', 'salary']
    ).properties(width=800, height=400)  # Đặt chiều rộng là 800 pixel
    st.altair_chart(bar_chart)

    # 2. Biểu đồ tròn - Số lượng nhân viên theo chức vụ
    st.write("### Tỉ lệ nhân viên theo chức vụ:")
    employee_count_by_position = employee_df.groupby("position").size().reset_index(name='count')
    pie_chart = alt.Chart(employee_count_by_position).mark_arc().encode(
        theta='count:Q',
        color='position:N',
        tooltip=['position', 'count']
    ).properties(width=800, height=400)  # Đặt chiều rộng là 800 pixel
    st.altair_chart(pie_chart)

    # 3. Biểu đồ tán xạ - Mối quan hệ giữa tuổi và lương
    st.write("### Mối quan hệ giữa tuổi và lương:")
    scatter_chart = alt.Chart(employee_df).mark_circle(size=60).encode(
        x=alt.X('age:Q', title="Tuổi"),
        y=alt.Y('salary:Q', title="Lương"),
        color='position:N',
        tooltip=['name', 'age', 'salary', 'position']
    ).properties(width=800, height=400)  # Đặt chiều rộng là 800 pixel
    st.altair_chart(scatter_chart)
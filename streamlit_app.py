import streamlit as st
import pandas as pd

# Tiêu đề ứng dụng
st.title("Quản Lý Nhân Viên")

# Khởi tạo dữ liệu giả định
if 'employees' not in st.session_state:
    st.session_state.employees = pd.DataFrame(columns=["ID", "Họ Tên", "Chức Vụ", "Tuổi", "Lương"])

# Hàm để thêm nhân viên
def add_employee(id, name, position, age, salary):
    new_employee = pd.DataFrame([[id, name, position, age, salary]], columns=["ID", "Họ Tên", "Chức Vụ", "Tuổi", "Lương"])
    st.session_state.employees = pd.concat([st.session_state.employees, new_employee], ignore_index=True)

# Form để thêm nhân viên
with st.form("form_employee"):
    st.subheader("Thêm Nhân Viên")
    id = st.text_input("ID")
    name = st.text_input("Họ Tên")
    position = st.text_input("Chức Vụ")
    age = st.number_input("Tuổi", min_value=18, max_value=100)
    salary = st.number_input("Lương", min_value=0.0)

    submitted = st.form_submit_button("Thêm Nhân Viên")
    if submitted:
        add_employee(id, name, position, age, salary)
        st.success("Nhân viên đã được thêm!")

# Hiển thị danh sách nhân viên
st.subheader("Danh Sách Nhân Viên")
st.dataframe(st.session_state.employees)

# Tùy chọn để xóa nhân viên
if st.session_state.employees.shape[0] > 0:
    st.subheader("Xóa Nhân Viên")
    id_to_delete = st.selectbox("Chọn ID nhân viên để xóa", st.session_state.employees["ID"])
    
    if st.button("Xóa Nhân Viên"):
        st.session_state.employees = st.session_state.employees[st.session_state.employees["ID"] != id_to_delete]
        st.success("Nhân viên đã được xóa!")


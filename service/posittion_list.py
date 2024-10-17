from service.connect_sql import DatabaseConnection
from enity.postions import Position  # Giả định bạn có một lớp Position tương tự như Employee

class PositionList:
    def __init__(self):
        self.db = DatabaseConnection()
        self.db.connect()  # Kết nối đến cơ sở dữ liệu

        self.positions = []  # Danh sách vị trí
        self.load_positions_from_db()  # Tải các vị trí từ cơ sở dữ liệu
  
    def add_position(self, name, salary_coefficient):
        # Thêm vị trí mới vào danh sách
        new_position = Position(name, salary_coefficient)  # Thêm hệ số lương vào đây
        self.positions.append(new_position)

        # Thêm vào cơ sở dữ liệu
        query = """
            INSERT INTO Positions (position_id, name, salary_multiplier)  # Cập nhật truy vấn SQL
            VALUES (%s,%s, %s)
        """
        data = (str(new_position.position_id),name, salary_coefficient)  # Cập nhật dữ liệu
        self.db.execute_query(query, data)

    def update_position(self, index, name, salary_multiplier):
        """Cập nhật tên và hệ số lương của chức vụ tại vị trí chỉ định."""
        try:
            index = int(index)  # Chuyển đổi index sang kiểu int
        except ValueError:
            raise ValueError("Index phải là một số nguyên.")

        if 0 <= index < len(self.positions):
            pos = self.positions[index]  # Lấy vị trí từ danh sách theo chỉ số
            pos.name = name  # Cập nhật tên
            pos.salary_multiplier = salary_multiplier  # Cập nhật hệ số lương

            # Cập nhật thông tin trong cơ sở dữ liệu
            query = """
                UPDATE Positions
                SET name = %s, salary_multiplier = %s
                WHERE position_id = %s
            """
            data = (name, salary_multiplier, pos.position_id)  # Cập nhật dữ liệu
            try:
                self.db.execute_query(query, data)  # Thực thi truy vấn
            except Exception as e:
                raise Exception(f"Cập nhật vị trí không thành công: {e}")
        else:
            raise IndexError("Chỉ số không hợp lệ: Vui lòng chọn một chỉ số hợp lệ.")

    def delete_position(self, position_id):
        query = "DELETE FROM Positions WHERE position_id = %s"
        self.db.execute_query(query, (position_id,))
        self.positions = [pos for pos in self.positions if pos.position_id != position_id]

    def load_positions_from_db(self):
        """Tải danh sách vị trí từ cơ sở dữ liệu."""
        query = "SELECT * FROM Positions"
        rows = self.db.fetch_all(query)
        for row in rows:
            pos = Position(row['name'], row['salary_multiplier'])  # Sử dụng cả tên và hệ số lương
            pos.position_id = row['position_id']  # Gán position_id từ cơ sở dữ liệu
            self.positions.append(pos)
    def get_positions(self):
        # Lấy danh sách các phòng ban
        query = "SELECT * FROM Positions"
        return self.db.fetch_all(query)
    def get_all_positions(self):
        # Trả về danh sách tất cả các chức vụ
        return self.positions
    def get_position_names(self):
        """Trả về danh sách tên vị trí."""
        Positions =self.get_positions()
        return [position['name'] for position in Positions if 'name' in position]

    def get_position_by_id(self, position_id):
        for pos in self.positions:
            if pos.position_id == position_id:
                return pos
        return None

    def get_position_info(self, name):
        """Trả về thông tin vị trí theo tên."""
        for position in self.positions:
            if position.name == name:
                return {
                    'ID': position.position_id,
                    'Tên': position.name
                }
        return None  # Trả về None nếu không tìm thấy vị trí
    def close_connection(self):
        self.db.close_connection()  # Đóng kết nối khi không còn sử dụng
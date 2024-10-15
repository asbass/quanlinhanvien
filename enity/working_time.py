import uuid

class WokingTime:
    def __init__(self, emp_id: int, time: str, status: str, reason: str, typeOff: str, typeTime: str) -> None:
        self.working_time_id: uuid.UUID = uuid.uuid4()  # Tạo UUID mới mỗi khi khởi tạo
        self.emp_id: int = emp_id
        self.time: str = time
        self.status: str = status
        self.reason: str = reason
        self.typeOff: str = typeOff
        self.typeTime: str = typeTime

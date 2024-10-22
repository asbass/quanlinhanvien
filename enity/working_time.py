import uuid

class WorkingTime:
    def __init__(self, working_time_id: uuid.UUID, emp_id: int, time: str, status: str, reason: str, type_off: str, type_time: str) -> None:
        self.working_time_id: uuid.UUID = working_time_id  # Sử dụng UUID được truyền vào
        self.emp_id: int = emp_id
        self.time: str = time
        self.status: str = status
        self.reason: str = reason
        self.type_off: str = type_off
        self.type_time: str = type_time

    def __str__(self) -> str:
        return f"WorkingTime(id={self.working_time_id}, emp_id={self.emp_id}, time={self.time}, status={self.status}, reason={self.reason}, typeOff={self.type_off}, typeTime={self.type_time})"
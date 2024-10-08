class Department:
    _id_counter = 1

    def __init__(self, name,positions):
        self.dept_id = Department._id_counter
        self.name = name
        self.positions = positions
        Department._id_counter += 1

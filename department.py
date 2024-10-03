class Department:
    _id_counter = 1

    def __init__(self, name):
        self.dept_id = Department._id_counter
        self.name = name
        Department._id_counter += 1

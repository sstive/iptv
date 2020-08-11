class Task:

    def __init__(self, database):
        # TODO: Get tasks from database
        self.database = database

        self.__update_task__()

    # Set current date in database TODO
    def __update_task__(self):
        pass

    # Finish task TODO
    def __complete_task__(self, task_id):
        pass

    # Run task TODO
    def execute(self):
        pass

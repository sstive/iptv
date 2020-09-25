from datetime import datetime


class Task:

    def __init__(self, task_id, database):
        self.tid = task_id
        self.DB = database

        if self.DB.run('tasks.get_date', tid=self.tid) > datetime.now().date():
            self.finished = True
        else:
            self.finished = False

    def __del__(self):
        # Shifting task time
        self.DB.begin()
        self.DB.run('tasks.prolong', tid=self.tid)
        pass

    # Run task
    def execute(self):
        pass

from os import environ as env


class Task:
    # Task id (Override)
    tid = 0
    # Database
    DB = None
    # Max number of threads
    MAX_THREADS = 256

    def __init__(self):
        if 'MAX_THREADS' in env.keys():
            self.MAX_THREADS = int(env['MAX_THREADS'])

    def add_database(self, database):
        self.DB = database

    def _execute(self):
        pass

    # Run task
    def run(self):
        crash = None

        try:
            self._execute()
        except Exception as e:
            if 'DEBUG' in env and env['DEBUG']:
                raise e
            crash = e

        self.DB.run('tasks.executed', tid=self.tid, crashed=str(crash))

        if crash is not None:
            print(f"\nError in task {self.tid}: {crash}\n")

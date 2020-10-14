from DBHelper import Database
from Tasks import TASKS

# Custom functions for database
from Utils.db_functions import FUNCS


if __name__ == '__main__':
    # Init database
    DB = Database('Config/Database.json', functions=FUNCS)

    for task in TASKS:
        task.add_database(DB)
        task.run()

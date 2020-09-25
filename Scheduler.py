from DBHelper import Database
from Tasks import *

# Custom functions for database
from Utils.functions import FUNCS


if __name__ == '__main__':
    # Init database
    DB = Database('Config/Database/Database.json', functions=FUNCS)

    Updater(1, DB).execute()
    MailManager(2, DB).execute()

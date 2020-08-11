from DBHelper import Database
from Tasks import *


# TODO: Init database
DB = Database()

# TODO: Run tasks
task = Updater(DB)
task.execute()

task = MailManager(DB)
task.execute()

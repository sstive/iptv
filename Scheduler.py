from DBHelper import Database
from Tasks import *

# Custom functions for database
from Utils.functions import FUNCS


# Init database
DB = Database('Config/Database/Database.json', FUNCTIONS=FUNCS)


# Running tasks #
Tasks = [
    SourceUpdater(1, DB),

    UrlChecker(2, DB),

    PlaylistFormer(3, DB),

    MailManager(4, DB)
]

for task in Tasks:
    if not task.finished:
        task.execute()

from DBHelper.database import Database


if __name__ == "__main__":
    db = Database("Database.json", drop='*')

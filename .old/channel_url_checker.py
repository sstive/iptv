from classes.database import Database
# TODO: replace print with logging

# Connecting to database
db = Database()

# Getting channels
channels = db.get_channels()
del db

# Checking channels
print('Checking channels...')
i = 1
for ch in channels.keys():
    print(f"{i}/{len(channels)}", end=' ')
    channels[ch].check()
    i += 1
print('Done')

db = Database(True)

# Saving without bad urls
db.add_channels(channels)

del db

import sqlite3

##### Create the Database if it doesn't exist
with sqlite3.connect("User.db") as db:
    cursor = db.cursor()

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS user(
userID INTEGER PRIMARY KEY,
username   VARCHAR(20) NOT NULL,
password   VARCHAR(20) NOT NULL,
first_name VARCHAR(20) NOT NULL,
last_name  VARCHAR(20) NOT NULL,
tier_name VARCHAR(20) NOT NULL); 
"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS profiles(
userID INTEGER PRIMARY KEY,
username VARCHAR(20) NOT NULL,
title VARCHAR(20),
location VARCHAR(20) NOT NULL,
specialty VARCHAR(50) NOT NULL,
about VARCHAR(250),
FOREIGN KEY(userID) REFERENCES user(userID))
"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS art(
userID INTEGER PRIMARY KEY,
username VARCHAR(20) NOT NULL,
title VARCHAR(20),
year INTEGER,
medium VARCHAR(60),
price INTEGER,
description VARCHAR(250),
FOREIGN KEY(userID) REFERENCES user(userID))
"""
)


#status: 1. sentpending
#        2. acceptpending
#        3. friend
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS friends(
username VARCHAR(20) NOT NULL,
stranger VARCHAR(20) NOT NULL,
status VARCHAR(20));
"""
)

# messaging
# 1. sent (message was sent)
# 2. deleted (message was deleted)
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS messageFriend(
sender VARCHAR(20) NOT NULL, 
receiver VARCHAR(20) NOT NULL,
message VARCHAR(20) NOT NULL,
status VARCHAR(20));
"""
)

# username: buyer
# 1. applied
# 2. deleted (notify user who applied)
# 3. saved
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS buyInfo(
userID INTEGER PRIMARY KEY,
username VARCHAR(20) NOT NULL,
title VARCHAR(20) NOT NULL,
price INTEGER,
payment VARCHAR(20),
comment VARCHAR(250),
status VARCHAR(20),
FOREIGN KEY(userID) REFERENCES user(userID))
"""
)

cursor.close()
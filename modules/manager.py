from modules.aes import enc, dec
from modules.generate import gen
import sqlite3
import os


class Manager:

    def __init__(self, name, pwd):
        self.name = name
        self.pwd = pwd
        self.sql = False

        if os.path.isfile(name):
            dec(name, "."+name, pwd)
            self.sql = sqlite3.connect("."+name)

    def isvalid(self):
        try:
            self.sql.execute("SELECT * FROM Main;")
            return True
        except:
            return False
    
    def create(self, pwd):
      self.sql = sqlite3.connect("."+self.name)
      self.sql.execute("CREATE TABLE Main (WEBSITE varchar(255) NOT NULL, USER varchar(255) NOT NULL, PASSWORD varchar(255) NOT NULL);")
      return "Database created successfully..."

    def update(self, website, param, value):
        if param == "user":
            self.sql.execute("UPDATE Main SET USER = ? WHERE WEBSITE = ?;", (value, website))
        elif param == "pwd":
            self.sql.execute("UPDATE Main SET PASSWORD = ? WHERE WEBSITE = ?;", (value, website))
        else:
            return f"'{param}' is not a valid option"
        return "Data updated successfully..."

    def add(self, website, user, pwd):
        self.sql.execute("INSERT INTO Main (WEBSITE, USER, PASSWORD) VALUES (?, ?, ?);", (website, user, pwd))
        return "Data added successfully..."

    def addrandom(self, website, user, length):
        rand = gen(length)
        self.sql.execute("INSERT INTO Main (WEBSITE, USER, PASSWORD) VALUES (?, ?, ?);", (website, user, rand))
        return rand

    def read(self, website):
        if website == "*":
            data = list(self.sql.execute("SELECT * FROM Main;"))
        else:
            data = list(self.sql.execute("SELECT * FROM Main WHERE WEBSITE = ?;", (website,)))

        return data

    def readall(self):
        data = list(self.sql.execute("SELECT WEBSITE, USER FROM Main;"))
        return data

    def delete(self, website):
        self.sql.execute("DELETE FROM Main WHERE WEBSITE = ?;", (website,))
        return "Data deleted successfully..."
    
    def deletetable(self):
      os.remove(self.name)
      os.remove("."+self.name)
      return "Database deleted successfully..."
    
    def reset(self):
      self.conn.rollback()
      return "Database was resetted successfully..."

    def close(self):
        self.sql.commit()
        self.sql.close()
        enc("."+self.name, self.name, self.pwd)
        os.remove("."+self.name)

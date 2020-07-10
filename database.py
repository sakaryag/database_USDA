import sqlite3 as dbapi2

from earthquake import Earthquake


class Database:
    def __init__(self, dbfile):
        self.dbfile = dbfile
    def add_earthquake(self, earthquake):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO EQ (TITLE, YR) VALUES (?, ?)"
            cursor.execute(query, (earthquake.title, earthquake.year))
            connection.commit()
            earthquake_key = cursor.lastrowid
        return earthquake_key

    def update_earthquake(self, earthquake_key, earthquake):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "UPDATE EQ SET TITLE = ?, YR = ? WHERE (ID = ?)"
            cursor.execute(query, (earthquake.title, earthquake.year, earthquake_key))
            connection.commit()

    def delete_earthquake(self, earthquake_key):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM EQ WHERE (ID = ?)"
            cursor.execute(query, (earthquake_key,))
            connection.commit()

    def get_earthquake(self, earthquake_key):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT TITLE, YR FROM EQ WHERE (ID = ?)"
            cursor.execute(query, (earthquake_key,))
            title, year = cursor.fetchone()
        earthquake_ = Earthquake(title, year=year)
        return earthquake_

    def get_earthquakes(self):
        earthquakes = []
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT ID, TITLE, YR FROM EQ ORDER BY ID"
            cursor.execute(query)
            for earthquake_key, title, year in cursor:
                earthquakes.append((earthquake_key, Earthquake(title, year)))
        return earthquakes

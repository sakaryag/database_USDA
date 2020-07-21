import sqlite3 as dbapi2

from food import food_group
from food import food_detail


class Database:
    def __init__(self, dbfile):
        self.dbfile = dbfile


    def get_food(self):
        with dbapi2.connect("food.db") as connection:
            cursor = connection.cursor()
            query = "SELECT FOOD_NAME,DESCRIPTION,NITROGEN,PROTEIN,FAT,CALORIE FROM SPICES"
            cursor.execute(query)

            row = cursor.fetchone()
            for food in row:
                name=row[0]
                desc=row[1]
                nitro=row[2]
                pro=row[3]
                fat=row[4]
                cal=row[5]
        food_ = food_detail(name,desc,nitro,pro,fat,cal)
        return food_

    def get_food_group(self):
        foods = []
        with dbapi2.connect("food.db") as connection:
            cursor = connection.cursor()
            query = "SELECT ID, TITLE FROM USDA ORDER BY ID"
            cursor.execute(query)
            for food_key, title in cursor:
                foods.append((food_key, food_group(title)))
        return foods
    def add_food_group(self, food_group):
        with dbapi2.connect("food.db") as connection:
            cursor = connection.cursor()
            query = "INSERT INTO USDA (TITLE) VALUES (?)"
            cursor.execute(query,(food_group.title,))
            connection.commit()
            food_key = cursor.lastrowid
        return food_key

    def add_food(self, food_detail):
         with dbapi2.connect("food.db") as connection:
             cursor = connection.cursor()
             query = "INSERT INTO DAIRY (TITLE) VALUES (?)"
             cursor.execute(query,(food_group.title,))
             connection.commit()
             food_key = cursor.lastrowid
         return food_key

    def update_food(self, food_key, food_group):
         with dbapi2.connect("food.db") as connection:
             cursor = connection.cursor()
             query = "UPDATE USDA SET TITLE = ?WHERE (ID = ?)"
             cursor.execute(query, (food_group.title, food_key))
             connection.commit()


    def delete_food(self, food_key):
         with dbapi2.connect("food.db") as connection:
             cursor = connection.cursor()
             query = "DELETE FROM USDA WHERE (ID = ?)"
             cursor.execute(query, (food_key,))
             connection.commit()

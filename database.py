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

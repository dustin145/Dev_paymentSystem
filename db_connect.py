import sqlite3 

DATABASE_NAME = ("C:/Users/Ash/Documents/python/paymentInfo.db") 

def get_db():
    conn = sqlite3.connect(DATABASE_NAME)
    return conn



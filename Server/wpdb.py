import mysql.connector
import pymysql
import os
from datetime import date
from dotenv import load_dotenv
from flask import Flask

load_dotenv()

class WPDB:
    def __init__(self):
        self.expenses_db = pymysql.connect(
            host = os.getenv("DB_HOST"),
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PW"),
            database = 'wpdb'
        )
        
        #order of names matters
        self.safeKeys = [
            'productID',
            'productName',
            'productDescription',
            'productPrice',
            'productType',
            'productDate',
            'productStock'
            ]

    def getProductData(self, id):
        cursor = self.expenses_db.cursor()
        sql = "select * from expenses where user_id = %s;"
        params = (id,)
        print(f"{params} {sql}")
        cursor.execute(sql,params)
        ret = cursor.fetchall()
        cursor.close()
        # print(ret)
        return ret
    
    #order of variables matters
    def insert_expenses(self, data):
        fields = []
        if "productName" not in data:
            return False
        if "productPrice" not in data:
            return False
        
        for key in self.safeKeys:
            if key in data and data[key]:
                fields.append(data[key])
            else:
                fields.append(None)

        print("fields: ", fields)

        try:
            sql = """insert into expenses (productID, productName, productDescription, productPrice, productType, productDate, productStock(%s, %s, %s, %s, %s, %s, %s);"""
            params = (fields[0],fields[1],fields[2],fields[3],fields[4],fields[5],fields[6],fields[7])
            print('params: ', params)
            cursor = self.expenses_db.cursor()
            cursor.execute(sql, params)
            self.expenses_db.commit()
            cursor.close()
            return True

        except mysql.connector.Error as e :
            print("Mysql command err: ", e)
            return False

    def updateProductData(self, data):
        if "productID" not in data:
            return False
        productID = data['productID']

        sql = "update products set "
        keys = list(data.keys())
        vals = list(data.values())
        counts = 0
        for key in keys:
            if key !="productID" and key not in self.safeKeys:
                return False
            if key != keys[len(keys)-1]:
                sql += key+"=%s, "
            else:
                sql += key+"=%s "
            counts += 1

        sql += "where productID=%s"
        vals.append(productID)
        params = tuple(vals)
        print("sql command: %s, params: %s" % (sql, params))
        try:
            params = (params)
            cursor = self.expenses_db.cursor()
            cursor.execute(sql, params)
            self.expenses_db.commit()
            cursor.close()
            return True

        except mysql.connector.Error as e :
            print("Mysql command err: ", e)
            return False

    def delete_expenses(self, id):
        if not id:
            return False
        try:
            sql = """delete from expenses where id=%s;"""
            params = (id,)
            cursor = self.expenses_db.cursor()
            cursor.execute(sql, params)
            self.expenses_db.commit()
            cursor.close()
            return True
        
        except mysql.connector.Error as e :
            print("Mysql command err: ", e)
            return False
    
    def close_db(self):
        self.expenses_db.close()





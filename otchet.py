#!/usr/bin/python3
import pymysql
from setting import db_info
from sql import sql_template


connection = pymysql.connect(**db_info)

try:
    with connection.cursor() as cursor:
        cursor.execute(sql_template)
        result = cursor.fetchone()
 	        while result:
                    print(result)
                    result = cursor.fetchone()
        #print(result)

finally:
    connection.close()



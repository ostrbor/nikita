#!/usr/bin/python3
import pymysql, re
from settings import db_info
from sql import sql_template, sql_keys
from datetime import datetime, timedelta


def make_query(connection, sql):
	with connection.cursor() as cursor:
		cursor.execute(sql)
		result = cursor.fetchall()
		print(result)
		#while True:
		#	result = cursor.fetchone()
		#	if not result: break
		#	print(result)

def get_input():
	print('Making query to database %s' % db_info['db'])
	print('Warning! Date format must be YYYY-mm-dd.')
	date_re = r'\d{4}-\d{2}-\d{2}'
	msg = 'Please enter %s: '
	res = {k: input(msg % k) for k in sql_keys}
	for (k, v) in res.items():
		if re.search(date_re, v):
			res[k] = datetime.strptime(v, '%Y-%m-%d')
	return res

if __name__ == '__main__':
	user_data = get_input()
	sql = sql_template % user_data
        with pymysql.connect(**db_info) as connection:
		make_query(connection, sql)

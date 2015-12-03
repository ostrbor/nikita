#!/usr/bin/python3
import pymysql, re, xlwt
from settings import db_info
from sql import sql_template, sql_keys
from datetime import datetime, timedelta


def make_query(connection, sql):
	with connection.cursor() as cursor:
		cursor.execute(sql)
		rows = cursor.fetchall()
		print(rows)
		#while True:
		#	result = cursor.fetchone()
		#	if not result: break
		#	print(result)

def get_input():
	print('Making query to database %s' % db_info['db'])
	print('Warning! Date format must be YYYY-mm-dd.')
	date_re = r'\d{4}-\d{2}-\d{2}'
	msg = 'Please enter %s: '
	user_data = {k: input(msg % k) for k in sql_keys}
	for (k, v) in user_data.items():
		if re.search(date_re, v):
			user_data[k] = datetime.strptime(v, '%Y-%m-%d')
	return user_data

def save_xls(db_records):
	book = xlwt.Workbook()
	sheet = book.add_sheet("Sheet 1")
	for rec_per_day in db_records:
		rec = tuple(rec_per_day)
		for column_num, value in enumerate(zip(*rec)):
			for row_num in range(len(value)):
				sheet.write(row_num, column_num, value[row_num])
	book.save('book.xls')
	
def calc_days(date0, date1):
	return date1-date0 if date1>date0 else date0-date1

if __name__ == '__main__':
	user_data = get_input()
	sql = sql_template % user_data
        with pymysql.connect(**db_info) as connection:
		make_query(connection, sql)sheet1 = book.add_sheet("Sheet 1")

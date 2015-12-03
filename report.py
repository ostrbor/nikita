#!/usr/bin/python3
import pymysql, re, xlwt
from settings import db_info, select_date
from sql import sql_template, sql_keys
from datetime import datetime, timedelta


def make_query(connection, sql):
	with connection.cursor() as cursor:
		cursor.execute(sql)
		rows = cursor.fetchall()
		print(rows)
		return rows
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
	for col_num, rec in enumerate(db_records):
		if not rec: continue
		for key in rec:
			row_num = select_date.get(key, None)
			if row_num:
				sheet.write(row_num, col_num, rec[key])
	book.save('book.xls')

#def extract_dates(user_data):
#	dates = [v for (k, v) in user_data.items() if isinstance(v, datetime)]
#	return dates

if __name__ == '__main__':
	user_data = get_input(); start_date =  user_data['StartDate']
	delta = user_data['FinishDate'] - start_date
	converted_data = user_data.copy()
	sql_array = []
	db_response = []
	for i in range(delta.days):
		start = start_date + timedelta(days=i)
		finish = start_date + timedelta(days=i+1)
		converted_data['StartDate'] = start
		converted_data['FinishDate'] = finish
		sql = sql_template % converted_data
		sql_array.append(sql)
	con = pymysql.connect(**db_info)
	cur = con.cursor()
	for sql in sql_array:
		cur.execute(sql)
		res = cur.fetchone()
		db_response.append(res)
        #with pymysql.connect(**db_info) as connection:
        #	for sql in sql_array:
	#		response = make_query(connection, sql)
	#		db_response.append(response)
	print(db_response)
	for i in db_response:
		print(i)
	print(len(db_response))
	
	#save_xls(db_response)
	con.close()

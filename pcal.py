# coding: utf-8

'''Производственный календарь'''

import calendar, datetime

class pCal:

	#http://data.gov.ru/opendata/7708660670-proizvcalendar
	p_clndr =  {
	'2016':[
	[1,2,3,4,5,6,7,8,9,10,16,17,23,24,30,31],
	[6,7,13,14,21,22,23,27,28],
	[5,6,7,8,12,13,19,20,26,27],
	[2,3,9,10,16,17,23,24,30],
	[1,2,3,7,8,9,14,15,21,22,28,29],
	[4,5,11,12,13,18,19,25,26],
	[2,3,9,10,16,17,23,24,30,31],
	[6,7,13,14,20,21,27,28],
	[3,4,10,11,17,18,24,25],
	[1,2,8,9,15,16,22,23,29,30],
	[4,5,6,12,13,19,20,26,27],
	[3,4,10,11,17,18,24,25,31]
	],
	'2017':[
	[1,2,3,4,5,6,7,8,9,14,15,21,22,28,29],
	[4,5,11,12,18,19,23,25,26],
	[4,5,8,11,12,18,19,25,26],
	[1,2,8,9,15,16,22,23,29,30],
	[1,6,7,8,9,13,14,20,21,27,28],
	[3,4,10,11,12,17,18,24,25],
	[1,2,8,9,15,16,22,23,29,30],
	[5,6,12,13,19,20,26,27],
	[2,3,9,10,16,17,23,24,30],
	[1,7,8,14,15,21,22,28,29],
	[4,5,6,11,12,18,19,25,26],
	[2,3,9,10,16,17,23,24,30,31]
	],
	'2018':[
	[1,2,3,4,5,6,7,8,9,10,13,14,20,21,27,28],
	[3,4,10,11,17,18,23,24,25],
	[3,4,8,10,11,17,18,24,25,31],
	[1,7,8,14,15,21,22,28,29],
	[1,5,6,9,12,13,19,20,26,27],
	[2,3,9,10,12,16,17,23,24,30],
	[1,7,8,14,15,21,22,28,29],
	[4,5,11,12,18,19,25,26],
	[1,2,8,9,15,16,22,23,29,30],
	[6,7,13,14,20,21,27,28],
	[3,4,5,10,11,17,18,24,25],
	[1,2,8,9,15,16,22,23,29,30]
	],
	'2019':[
	[1,2,3,4,5,6,7,8,9,10,12,13,19,20,26,27],
	[2,3,9,10,16,17,23,24,25],
	[2,3,8,9,10,16,17,23,24,30,31],
	[6,7,13,14,20,21,27,28],
	[4,5,9,11,12,18,19,25,26],
	[1,2,8,9,12,15,16,22,23,29,30],
	[6,7,13,14,20,21,27,28],
	[3,4,10,11,17,18,24,25,31],
	[1,7,8,14,15,21,22,28,29],
	[5,6,12,13,19,20,26,27],
	[2,3,9,10,16,17,23,24,30],
	[1,7,8,14,15,21,22,28,29]
	]
	}

	now = datetime.datetime.now()
	cur_mnth = now.month
	
	if cur_mnth == 1:
		lst_mnth = 12
	else:
		lst_mnth = now.month-1

	def month_days(month_number='current'):
		if month_number == 'current':
			return calendar.monthrange(pCal.now.year, pCal.cur_mnth)[1]
		elif month_number == 'previous':
			return calendar.monthrange(pCal.now.year, pCal.lst_mnth)[1]
		elif isinstance(month_number, int) and (int(month_number) > 0) and (int(month_number) < 13):
			return calendar.monthrange(pCal.now.year, int(month_number))[1]
		else:
			return False

	def working_days(month_number='current'):
		if month_number == 'current':
			return str( pCal.month_days() - len(pCal.p_clndr[str(pCal.now.year)][pCal.cur_mnth-1]) )
		elif month_number == 'previous':
			return str( pCal.month_days(pCal.lst_mnth) - len(pCal.p_clndr[str(pCal.now.year)][pCal.lst_mnth-1]) )
		elif isinstance(month_number, int) and (int(month_number) > 0) and (int(month_number) < 13):
			return str( pCal.month_days(int(month_number)) - len(pCal.p_clndr[str(pCal.now.year)][int(month_number)]) )
		else:
			return False

	def working_days_passed(day='current'):
		total_holidays = 0

		if day == 'current':
			to_day = int(pCal.now.day)
		elif int(day) in range(1,31):
			to_day = int(day)
		else:
			return False

		# Считать сегодня или нет
		# if(pCal.now.hour < 14):
		# 	to_day = to_day - 1

		for d in pCal.p_clndr[str(pCal.now.year)][pCal.cur_mnth-1]:
			if int(d) < to_day:
				total_holidays = total_holidays + 1
			else:
				break
		return to_day - total_holidays


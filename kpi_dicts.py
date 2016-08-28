# -*- coding: utf-8 -*-

domain_url = 'aHR0cDovL290cC5kZW1pcy5ydQ=='
api_uri = "/smoke/oto/uto-kpi-api.php"
kpi_uri = "/smoke/oto/uto-kpi-tmp.php"
api_employees_get = "?action=users&da-rest=json"
api_result_get = "?action=result&da-rest=json"

result_rus_dict = {
'labor':				'Объем набранных баллов',
'labor_vip':			'Объем баллов за проверки VIP',
'issues_cnt':			'Количество выполненных задач',
'idle_penalty':			'Штрафные баллы за просрочку задач',
'overdue_cnt':			'Количество просроченных задач',
'result':				'Итоговое число баллов',
'intime':				'Количество задач выполненных в срок',
'intime_perc':			'Процент задач выполненных в срок',
'plan':					'План',
'plan_amnesty':			'Порог амнистии',
'absence':				'Отсутствия',
'plan_perc':			'Процент плана',
'money':				'Премия (итог)',
'money_result':			'Премия (факт)',
'vacation_labor':		'Отсутствия: компенсация',
'dept_labor':			'Подразделение: Объем набранных баллов',
'dept_labor_vip':		'Подразделение: Объем баллов за проверки VIP',
'dept_issues_cnt':		'Подразделение: Количество выполненных задач',
'dept_idle_penalty':	'Подразделение: Штрафные баллы за просрочку задач',
'dept_overdue_cnt':		'Подразделение: Количество просроченных задач',
'dept_result':			'Подразделение: Итоговое число баллов',
'dept_intime':			'Подразделение: Количество задач выполненных в срок',
'dept_intime_perc':		'Подразделение: Процент задач выполненных в срок',
'dept_plan':			'Подразделение: План',
'dept_plan_perc':		'Подразделение: Процент плана',
'dept_money_labor':		'Подразделение: Премия',
'dept_money_intime':	'Подразделение: Премия за сроки',
'forecast_ratio':		'Прогноз: Базовое отношение',
'labor_forecast':		'Прогноз: Объем набранных баллов',
'labor_vip_forecast':	'Прогноз: Объем баллов за проверки VIP',
'idle_penalty_forecast':'Прогноз: Штрафные баллы',
'result_forecast':		'Прогноз: Итоговое число баллов',
'plan_perc_forecast':	'Прогноз: Процент плана',
'money_forecast':		'Прогноз: Премия (итог)',
'money_result_forecast':'Прогноз: Премия (факт)',
'dept_labor_forecast':	'Прогноз подразделение: Баллы',
'dept_labor_vip_forecast':'Прогноз подразделение: Баллы за VIP',
'dept_result_forecast':	'Прогноз подразделение: Итоговое число баллов',
'dept_plan_perc_forecast':'Прогноз подразделение: Процент плана',
'dept_money_labor_forecast':'Прогноз подразделение: Премия',
# generatd keys
'1_labor':'баллы чистые',
'2_result':'баллы грязные',
# '':'',
}

plan_rate_dict = {
'Ведущий программист':450,
'Старший программист':400,
'Программист':350,
'Стажер-1М':87.5, # испытательный срок
'Стажер-1М':210,
'Стажер-3М':315,
'Исп-1М':100, # повышенный грейд
'Исп-1М':240,
'Исп-3М':360
}

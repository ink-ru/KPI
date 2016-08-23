
domain_url = "http://otp.demis.ru"
api_uri = "/smoke/oto/uto-kpi-api.php"
kpi_uri = "/smoke/oto/uto-kpi-tmp.php"
smoke_uri = "/smoke/"
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
'money':				'Премия',
'money_result':			'money_result',
'vacation_labor':		'Компенсация отпуска',
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

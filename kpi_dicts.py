#!/usr/bin/python3
# -*- coding: utf-8 -*-

domain_url = "http://otp.demis.ru"
api_uri = "/smoke/oto/uto-kpi-api.php"
kpi_uri = "/smoke/oto/uto-kpi-tmp.php"
smoke_uri = "/smoke/"
api_employees_get = "?action=users&da-rest=json"
api_result_get = "?action=result&da-rest=json"

result_rus_dict = {
'intime': 'задач в срок',
'overdue_cnt':'просроченно задач',
'dept_intime':'подразделение - в срок',
'result':'баллы грязные',
'dept_labor':'подразделение - баллы чистые',
'dept_result':'подразделение - баллы грязные',
'dept_issues_cnt':'подразделение - всего задач',
'idle_penalty':'штраф за провис',
'intime_perc':'процент в срок',
'dept_idle_penalty':'подразделение - штраф за провис',
'issues_cnt':'всего задач',
'labor':'баллы чистые',
'dept_labor_vip':'подразделение - VIP',
'dept_overdue_cnt':'подразделение - просроченно задач',
'dept_intime_perc':'подразделение - процент в срок',
'labor_vip':'VIP',
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

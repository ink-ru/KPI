#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys, re, urllib, json, collections
import urllib.parse
import urllib.request
import operator # http://stackoverflow.com/questions/19411101/pyside-qtableview-example
import subprocess

from PyQt4.QtCore import QSettings
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from pcal import *
from kpi_dicts import *

# import signal # TODO add time limit

import socket
socket.setdefaulttimeout(10)

class AppSettings():
	def __init__(self, parent=None):
		super(AppSettings, self).__init__()
		self.settings = QSettings()
		self.authstring = self.settings.value('authstring')

	def getParametr(self, name):
		if hasattr(self, name):
			attr = getattr(self, name)
			if attr != None:
				return attr
		attr = self.settings.value(name)
		if attr != None:
			return attr
		else:
			return False

	def setParametr(self, name, value):
		setattr(self, name, value)
		self.settings.setValue(name, value)
		return True

class GetKPI():
	def __init__(self, parent=None):
		super(GetKPI, self).__init__(parent)
		# add init code here

	def get_auth_url(url, username, password):		
		data = urllib.parse.urlencode({'ldap-mail': username, 'ldap-pass': password, 'go': ' Войти '})
		data = data.encode('ascii') # data should be bytes
		request = urllib.request.Request(url, data)
		resorce = urllib.request.urlopen(request)
		html = resorce.read().decode("utf-8").strip()
		return html

	def auth_probe(username, password):
		# content = GetKPI.get_auth_url(domain_url+smoke_uri, username, password)
		content = GetKPI.get_auth_url(domain_url + api_uri + api_result_get, username, password)

		if content.find("Авторизация LDAP") > 0:
			return False
		return True

class MyWindow(QWidget):
	def __init__(self, data_list, header, *args):
		QWidget.__init__(self, *args)
		# setGeometry(x_pos, y_pos, width, height)
		self.setGeometry(300, 200, 570, 450)
		self.setWindowTitle("Demis KPI")
		self.setWindowIcon(QIcon('app.png'))
		table_model = MyTableModel(self, data_list, header)
		self.table_view = QTableView()
		self.table_view.setModel(table_model)

		# Установка шрифта
		# self.setStyleSheet('font: 10pt "Courier New"')
		font = QFont("Arial", 12)
		self.table_view.setFont(font)

		# set column width to fit contents (set font first!)
		self.table_view.resizeColumnsToContents()

		# set selection mode
		# self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
		
		# пользователь не может изменять размер столбцов
		# self.table_view.horizontalHeader().setResizeMode(QtGui.QHeaderView.Fixed)

		# включаем растягивание последнего столбца
		self.table_view.horizontalHeader().setStretchLastSection(False)

		# отключаем показ границ виджета
		self.table_view.setStyleSheet('''border: none;''')

		# Сетка
		# self.table_view.setShowGrid(False)

		# Включаем чередующуюся подсветку строк
		self.table_view.setAlternatingRowColors(True)

		# скрываем заголовки строк
		# self.table_view.verticalHeader().hide()

		# enable sorting
		self.table_view.setSortingEnabled(True)
		self.table_view.sortByColumn(0, Qt.AscendingOrder)
		layout = QVBoxLayout(self)

		self.table_view.hideColumn(0)
		
		self.statusbar = QStatusBar()
		self.statusbar.setObjectName("statusbar")

		self.myQMenuBar = QMenuBar(self)
		fileMenu = self.myQMenuBar.addMenu('File')

		# exitAction = QAction('Exit', self)
		exitAction = QAction(QIcon('exit.png'), 'Exit', self)
		exitAction.setShortcut('esc')      
		exitAction.triggered.connect(qApp.quit)
		fileMenu.addAction(exitAction)

		# fileMenu.addSeparator() # -----

		restartAction = QAction(QIcon('./img/reload.png'), 'Reload', self)
		restartAction.setShortcut('f5')       
		restartAction.triggered.connect(self.action_reload)
		fileMenu.addAction(restartAction)

		toggleVIPAction = QAction(QIcon('./img/vip.png'), 'VIP', self)
		toggleVIPAction.setShortcut('alt+v')
		toggleVIPAction.triggered.connect(self.toggle_vip)

		toggleGroupAction = QAction(QIcon('./img/group.png'), 'Group', self)
		toggleGroupAction.setShortcut('alt+g')
		toggleGroupAction.triggered.connect(self.toggle_group)

		self.toolbar = QToolBar(self)
		self.toolbar.addAction(exitAction)
		self.toolbar.addAction(restartAction)
		self.toolbar.addAction(toggleVIPAction)
		self.toolbar.addAction(toggleGroupAction)

		self.setLayout(layout)
		layout.addWidget(self.myQMenuBar)
		layout.addWidget(self.toolbar)
		layout.addWidget(self.table_view)
		layout.addWidget(self.statusbar)

	def scrollTo(self, index, hint):
		if index.column() > 1:
			QtGui.QTableView.scrollTo(self, index, hint)
	
	def toggle_vip(self):
		if self.table_view.isColumnHidden(3):
			self.table_view.showColumn(3)
			self.table_view.showColumn(11)
			# self.table_view.selectColumn(3)
		else:
			self.table_view.hideColumn(3)
			self.table_view.hideColumn(11)
		self.statusbar.showMessage('изменение видимости VIP')

	def toggle_group(self):
		clist = [9,10,11,12,13,14,15,16]
		if self.table_view.isColumnHidden(clist[0]):
			for i in clist:
				self.table_view.showColumn(i)
				# print('hide' + str(i))
		else:
			for i in clist:
				self.table_view.hideColumn(i)
				# print('show' + str(i))
		self.statusbar.showMessage('изменение видимости показателей групп')

	def action_reload(self):
		subprocess.Popen([__file__])
		sys.exit(0)

class MyTableModel(QAbstractTableModel):
	def __init__(self, parent, mylist, header, *args):
		QAbstractTableModel.__init__(self, parent, *args)
		self.mylist = mylist
		self.header = header

	def rowCount(self, parent):
		return len(self.mylist)

	def columnCount(self, parent):
		return len(self.mylist[0])

	def data(self, index, role):
		if not index.isValid():
			return None
		elif role != Qt.DisplayRole:
			return None
		return self.mylist[index.row()][index.column()]

	def headerData(self, section, orientation, role):
		if orientation == Qt.Horizontal and role == Qt.DisplayRole:
			return self.header[section]
		elif orientation == Qt.Vertical:
		# 	return ['Row %d' % int(row+1) for row in range(len(self.mylist))]
			index = self.index(section, 0) # assuming ID is the first column
			return self.data(index, role)
		
		return QAbstractTableModel.headerData(self, section, orientation, role)
		# return None

	def sort(self, col, order):
		"""sort table by given column number col"""
		self.emit(SIGNAL("layoutAboutToBeChanged()"))
		self.mylist = sorted(self.mylist,
			key=operator.itemgetter(col))
		if order == Qt.DescendingOrder:
			self.mylist.reverse()
		self.emit(SIGNAL("layoutChanged()"))

class Login(QDialog):
	def __init__(self, parent=None):
		super(Login, self).__init__(parent)
		self.textName = QLineEdit(self)
		self.textPass = QLineEdit(self)
		self.buttonLogin = QPushButton('Login', self)
		self.buttonLogin.clicked.connect(self.handleLogin)
		layout = QVBoxLayout(self)
		layout.addWidget(self.textName)
		layout.addWidget(self.textPass)
		layout.addWidget(self.buttonLogin)

	def handleLogin(self):
		sett = AppSettings()
		sett.setParametr("username", self.textName.text())
		sett.setParametr("password", self.textPass.text())

		if GetKPI.auth_probe(self.textName.text(), self.textPass.text()) != False:
			self.accept()
		else:
			QMessageBox.warning(
				self, 'Error', 'Неверный логин или пароль!')

if __name__=="__main__":

	app = QApplication([]) # app = QApplication(sys.argv)
	sett = AppSettings()
	auth = False

	username = sett.getParametr("username")
	password = sett.getParametr("password")


	if GetKPI.auth_probe(username, password) == False:
		print("Требуется авторизация")
		login = Login()
		if login.exec_() == QDialog.Accepted:
			auth = True
	else:
		auth = True

	if auth == True:
		header = ['Сотрудник', 
		"баллы грязные",
		"просроченно задач",
		"VIP",
		"баллы чистые",
		"всего задач",
		"процент в срок",
		"задач в срок",
		"штраф за провис",
		"подразделение - баллы грязные",
		"подразделение - просроченно задач",
		"подразделение - VIP",
		"подразделение - баллы чистые",
		"подразделение - всего задач",
		"подразделение - процент в срок",
		"подразделение - в срок",
		"подразделение - штраф за провис"
		]

		full_url = domain_url + api_uri + api_result_get
		rjson = GetKPI.get_auth_url(full_url, username, password)
		cdict = json.loads(rjson)

		full_url = domain_url + api_uri + api_employees_get
		rjson = GetKPI.get_auth_url(full_url, username, password)
		udict = json.loads(rjson)

		data_list = []

		for record in cdict:
			user_data = ()

			emp_name = str(udict[record]['name'])
			grade = str(udict[record]['grade_name'])

			user_data += (emp_name + " (" + grade + ")",)

			od = collections.OrderedDict(sorted(cdict[record].items(), reverse=True))
			for r_feild in od:
				indicator_name = str(result_rus_dict[r_feild])
				indicator = float(cdict[record][r_feild])
				# user_data += (str(indicator) + " (" + indicator_name + ")",)
				user_data += (indicator,)
			data_list = data_list + [user_data,]
		
		win = MyWindow(data_list, header)
		win.setMinimumSize(800, 600)
		win.resize(1024, 768)
		win.show()
		win.statusbar.showMessage('Ready')
		app.exec_()
	else:
		app.quit
		

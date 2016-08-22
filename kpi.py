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
		self.kpi = ''
		self.setWindowIcon(QIcon('app.png'))
		table_model = MyTableModel(self, data_list, header)
		self.table_view = QTableView()
		self.table_view.setModel(table_model)
		self.sett = AppSettings()

		# http://doc.qt.io/qt-5/stylesheet-examples.html
		# http://doc.qt.io/qt-5/stylesheet-reference.html
		style = '''border: none;'''
		# отключаем показ границ виджета
		self.table_view.setStyleSheet(style)

		# Установка шрифта
		self.setStyleSheet('''/* font: 12pt "Arial"; */

		QHeaderView::up-arrow, QHeaderView::down-arrow, QHeaderView::indicator, QTableView::indicator {color:#fff;
		margin: 0;
		padding: 0;
		spacing: 0;
		margin-right: -10px;
		width: 2px;
		max-width: 2px;
		/* subcontrol-origin: content;
		subcontrol-origin: margin;
		subcontrol-origin: border; */
		subcontrol-position: right center;
		position: absolute;
		right: -10px;
		icon-size: 2px;
		show-decoration-selected: 0;
		opacity: 0;
		viasbility: hidden;
		font-size: 1px;
		outline-offset:0;
		border: none;
		background: none;
		}

		QTableView::item:hover {
			background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
										stop: 0 #cfcfdd, stop: 1 #f0f0f0);
			border: 1px solid #000;
		}
			''')
		font = QFont("Arial", 12)
		self.table_view.setFont(font)

		# set column width to fit contents (set font first!)
		self.table_view.resizeColumnsToContents()

		# set selection mode
		# self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
		
		# пользователь не может изменять размер столбцов
		# self.table_view.horizontalHeader().setResizeMode(QHeaderView.Fixed)

		self.table_view.horizontalHeader().setCascadingSectionResizes(False)
		# self.table_view.horizontalHeader().setDefaultSectionSize(100)

		# включаем растягивание последнего столбца
		self.table_view.horizontalHeader().setStretchLastSection(False)

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

		exitAction = QAction(QIcon('exit.png'), 'Exit', self)
		exitAction.setShortcut('esc')      
		exitAction.triggered.connect(qApp.quit)
		fileMenu.addAction(exitAction)

		# fileMenu.addSeparator()

		restartAction = QAction(QIcon('./img/reload.png'), 'Reload', self)
		restartAction.setShortcut('f5')       
		restartAction.triggered.connect(self.action_reload)
		fileMenu.addAction(restartAction)

		fileMenu = self.myQMenuBar.addMenu('Preferences')

		set_id_Action = QAction('Изменить учетные данные', self)
		set_id_Action.setShortcut('alt+i')       
		set_id_Action.triggered.connect(self.action_set_auth)
		fileMenu.addAction(set_id_Action)

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

		if self.sett.getParametr("vip") == '0':
			self.toggle_vip()

		print('initial Group state - ' + str(self.sett.getParametr("group")))
		if self.sett.getParametr("group") == '0':
			self.toggle_group()

	def event(self, event):
		if (event.type() == QEvent.WindowStateChange and self.isMinimized()):
			# self.setWindowFlags(self.windowFlags() & ~Qt.Tool)
			self.hide()
			return True
		else:
			return super(MyWindow, self).event(event)

	def scrollTo(self, index, hint):
		if index.column() > 1:
			QTableView.scrollTo(self, index, hint)
	
	def toggle_vip(self):
		if self.table_view.isColumnHidden(9):
			self.table_view.showColumn(9)
			self.table_view.showColumn(21)
			self.sett.setParametr("vip", 1)
		else:
			self.table_view.hideColumn(9)
			self.table_view.hideColumn(21)
			self.sett.setParametr("vip", 0)
		self.statusbar.showMessage('изменение видимости VIP')

	def toggle_group(self):
		if self.table_view.isColumnHidden(15):
			for i in range(15,27):
				self.table_view.showColumn(i)
			self.sett.setParametr("group", 1)
		else:
			for i in range(15,27):
				self.table_view.hideColumn(i)
			self.sett.setParametr("group", 0)
		self.statusbar.showMessage('изменение видимости показателей групп')

	def action_reload(self):
		subprocess.Popen([__file__])
		sys.exit(0)

	# action_set_auth
	def action_set_auth(self):
		saver = Login()
		if saver.exec_() == QDialog.Accepted:
			self.statusbar.showMessage('Данные сохранены')
			return True
		else:
			self.statusbar.showMessage('Ошибка сохранения данных!')
		return

	def action_set_id(self):
		saver = SetID()
		if saver.exec_() == QDialog.Accepted:
			self.statusbar.showMessage('ID сохранен')
			return True
		else:
			self.statusbar.showMessage('Ошибка сохранения ID')
		return

	# Не используется
	# Реализовано в классе SystemTrayIcon
	def trayActivated(self, reason):
		if reason == QSystemTrayIcon.DoubleClick:
			self.setWindowState(Qt.WindowNoState)
			self.show()
		elif reason == QSystemTrayIcon.Trigger:
			CommonTools.show_popup('всего баллов', str(self.kpi))

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

class SystemTrayIcon(QSystemTrayIcon):
	def __init__(self, icon, parent, kpi):
		QSystemTrayIcon.__init__(self, icon, parent)
		self.win = parent
		self.kpi = kpi
		menu = QMenu(parent)

		showAction = QAction('Показать окно программы', self)
		# showAction.setShortcut('ctrl+h')      
		showAction.triggered.connect(self.show_action)
		menu.addAction(showAction)

		exitAction = QAction('Exit', self)
		exitAction.setShortcut('esc')      
		exitAction.triggered.connect(qApp.quit)
		menu.addAction(exitAction)

		self.setContextMenu(menu)

		# on activation listener
		self.activated.connect(self.trayActivated)

	def show_action(self):
		self.win.setWindowState(Qt.WindowNoState)
		self.win.show()
		return True

	def trayActivated(self, reason):
		if reason == QSystemTrayIcon.DoubleClick:
			self.win.setWindowState(Qt.WindowNoState)
			self.win.show()
		elif reason == QSystemTrayIcon.Trigger:
			CommonTools.show_popup('всего баллов', str(self.kpi))    

	def create_icon(self, text):
		font = QFont("Arial", 24)
		font.setPointSizeF(font.pointSizeF() * 2)
		font.setWeight(600)
		metrics = QFontMetricsF(font)

		rect = metrics.boundingRect(text)
		position = -rect.topLeft()
		
		if not text:
				return
		
		pixmap = QPixmap(rect.width(), rect.height())
		pixmap.fill(Qt.white)
		
		painter = QPainter()
		painter.begin(pixmap)
		painter.setFont(font)
		painter.setPen(QColor(0, 0, 0))
		# painter.drawText(1, 1, 64, 64, Qt.AlignLeft, text)
		painter.drawText(position, text)
		painter.end()
	
		return(pixmap)


class CommonTools():
	def show_popup(header, data):
		cmd = "notify-send '" + str(header) + "' '" + str(data) + "' '-t' 5000"
		process = subprocess.Popen(cmd, shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
		# process = subprocess.call(['notify-send', data])

		# stdout, stderr = process.communicate() # only with Popen
		# print(stdout)
		# print(stderr)
		return True

if __name__=="__main__":

	def split_header(text):
		text = text.split(' ', 2)
		s = "\n";
		text =  s.join( text )
		return text

	app = QApplication([]) # app = QApplication(sys.argv)
	sett = AppSettings()
	auth = False
	header = ['Сотрудник']

	username = sett.getParametr("username")
	password = sett.getParametr("password")
	# username = sett.setParametr("username", "")
	# password = sett.setParametr("password", "")

	if GetKPI.auth_probe(username, password) == False:
		print("Требуется авторизация")
		login = Login()
		if login.exec_() == QDialog.Accepted:
			auth = True
			subprocess.Popen([__file__])
			sys.exit(0)

	else:
		auth = True

	if auth == True:

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
				try:
					indicator_name = split_header(str(result_rus_dict[r_feild]))
				except KeyError as e:
					indicator_name = str(r_feild)
					# raise ValueError('Undefined unit: {}'.format(e.args[0]))

				if len(header) <= len(od):
					header = header + [indicator_name,]

				if (udict[record]['login'] == username) and (r_feild == 'result'):
					icon_data = str(cdict[record][r_feild])
					notify_name = emp_name

				indicator = round(float(cdict[record][r_feild]),2)
				# user_data += (str(indicator) + " (" + indicator_name + ")",)
				user_data += (indicator,)
			data_list = data_list + [user_data,]
		
		win = MyWindow(data_list, header)
		

		trayIcon = SystemTrayIcon(QIcon("app.png"), win, icon_data)
		trayIcon.setIcon(QIcon(trayIcon.create_icon(icon_data)))

		# Реализовано в классе SystemTrayIcon
		# win.kpi = icon_data
		# trayIcon.activated.connect(win.trayActivated)

		trayIcon.setToolTip(icon_data)
		trayIcon.show()

		win.setMinimumSize(800, 600)
		win.resize(1024, 768)
		win.show()
		win.statusbar.showMessage('Ready')
		
		CommonTools.show_popup(notify_name +' - всего баллов', icon_data)
		
		app.exec_()

	else:
		app.quit
		

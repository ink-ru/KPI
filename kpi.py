#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys, re, urllib, json, collections, base64
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

# img_path = '/usr/share/pixmaps/kpi/'
img_path = './img/'
# d = base64.b64encode(bytes(domain_url, "utf-8"))
domain_url = base64.b64decode(domain_url).decode("utf-8", "ignore")

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
		# TODO: implement QNetworkRequest and QAbstractNetworkCache
		data = urllib.parse.urlencode({'ldap-mail': username, 'ldap-pass': password, 'go': ' Войти '})
		data = data.encode('ascii') # data should be bytes
		request = urllib.request.Request(url, data)
		resorce = urllib.request.urlopen(request)
		html = resorce.read().decode("utf-8").strip()
		return html

	def auth_probe(username, password):
		content = GetKPI.get_auth_url(domain_url + api_uri + api_employees_get, username, password)
		if content.find("Авторизация LDAP") > 0:
			return False
		return True

class MyWindow(QWidget):
	def __init__(self, data_list, header, userpos, *args):
		QWidget.__init__(self, *args)
		# setGeometry(x_pos, y_pos, width, height)
		self.setGeometry(300, 200, 570, 450)
		self.setWindowTitle("Demis KPI")
		self.kpi = ''
		self.setWindowIcon(QIcon(img_path+'app.png'))
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
			/* background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #cfcfdd, stop: 1 #f0f0f0); */
			background: grey;
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
		self.table_view.selectRow(userpos)
		self.table_view.sortByColumn(0, Qt.AscendingOrder)
		layout = QVBoxLayout(self)

		self.table_view.hideColumn(0)
		
		self.statusbar = QStatusBar()
		self.statusbar.setObjectName("statusbar")

		self.myQMenuBar = QMenuBar(self)
		fileMenu = self.myQMenuBar.addMenu('File')

		exitAction = QAction(QIcon(img_path+'exit.png'), 'Exit', self)
		exitAction.setShortcut('esc')      
		exitAction.triggered.connect(qApp.quit)
		fileMenu.addAction(exitAction)

		# fileMenu.addSeparator()

		restartAction = QAction(QIcon(img_path+'reload.png'), 'Reload', self)
		restartAction.setShortcut('f5')       
		restartAction.triggered.connect(self.action_reload)
		fileMenu.addAction(restartAction)

		fileMenu = self.myQMenuBar.addMenu('Preferences')

		set_id_Action = QAction('Настройки', self)
		set_id_Action.setShortcut('alt+i')       
		set_id_Action.triggered.connect(self.action_set_settings)
		fileMenu.addAction(set_id_Action)

		toggleVIPAction = QAction(QIcon(img_path+'vip.png'), 'VIP', self)
		toggleVIPAction.setShortcut('alt+v')
		toggleVIPAction.setCheckable(True)
		toggleVIPAction.setChecked(True)
		toggleVIPAction.triggered.connect(self.toggle_vip)

		toggleGroupAction = QAction(QIcon(img_path+'group.png'), 'Group', self)
		toggleGroupAction.setShortcut('alt+g')
		toggleGroupAction.setCheckable(True)
		toggleGroupAction.setChecked(True)
		toggleGroupAction.triggered.connect(self.toggle_group)

		# copyAction = QAction(self)
		# copyAction.setShortcut('ctrl+ins')
		# copyAction.setShortcut('ctrl+c')
		# copyAction.setShortcut(QKeySequence(Qt.Key_C))
		# copyAction.triggered.connect(self.copy_cells_to_clipboard)
		# self.addAction(copyAction)

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
			toggleVIPAction.setChecked(False)

		if self.sett.getParametr("group") == '0':
			self.toggle_group()
			toggleGroupAction.setChecked(False)

	def keyPressEvent(self, e):
		if (e.modifiers() & Qt.ControlModifier):
			if e.key() in (Qt.Key_C, 16777222): # QKeySequence.Copy
				self.copy_cells_to_clipboard()

	def copy_cells_to_clipboard(self):
		if len(self.table_view.selectionModel().selectedIndexes()) > 0:
			# sort select indexes into rows and columns
			previous = self.table_view.selectionModel().selectedIndexes()[0]
			columns = []
			rows = []
			for index in self.table_view.selectionModel().selectedIndexes():
				if previous.column() != index.column():
					columns.append(rows)
					rows = []
				rows.append(index.data())
				previous = index
			columns.append(rows)

			# add rows and columns to clipboard            
			clipboard = ""
			nrows = len(columns[0])
			ncols = len(columns)
			for r in range(nrows):
				for c in range(ncols):
					clipboard += str(columns[c][r]).replace('.', ',')
					if c != (ncols-1):
						clipboard += '\t'
				clipboard += '\n'

			# copy to the system clipboard
			sys_clip = QApplication.clipboard()
			sys_clip.setText(clipboard)

	# def closeEvent(self,event):
	# 	reply = QMessageBox.question(self,'Message',"Are you sure to quit?", QMessageBox.Yes, QMessageBox.No)
	# 	if reply == QMessageBox.Yes:
	# 		event.accept()
	# 	else:
	# 		event.ignore()

	def event(self, event):
		if event.type() == QEvent.WindowStateChange:
			if self.isMinimized():
				# self.setWindowFlags(self.windowFlags() & ~Qt.Tool)
				self.hide()
				self.sett.setParametr("window_state", 'minimized');
		else:
			return super(MyWindow, self).event(event)
		return True

	def scrollTo(self, index, hint):
		if index.column() > 1:
			QTableView.scrollTo(self, index, hint)
	
	def toggle_vip(self):
		# TODO store ranges in app settings
		vip_range = (13,14,21,32,33)
		if self.table_view.isColumnHidden(vip_range[0]):
			for i in vip_range:
				self.table_view.showColumn(i)
			self.sett.setParametr("vip", 1)
		else:
			for i in vip_range:
				self.table_view.hideColumn(i)
			self.sett.setParametr("vip", 0)
		self.statusbar.showMessage('изменение видимости VIP')

	def toggle_group(self):
		# TODO store ranges in app settings
		group_range = (24,26,27,28,30,31,33,35,36,37,38,39,40)
		if self.table_view.isColumnHidden(group_range[0]):
			for i in group_range:
				self.table_view.showColumn(i)
			self.sett.setParametr("group", 1)
		else:
			for i in group_range:
				self.table_view.hideColumn(i)
			self.sett.setParametr("group", 0)
		self.statusbar.showMessage('изменение видимости показателей подразделений')

	def action_reload(self):
		# TODO: reload model only - http://www.qtcentre.org/threads/31770-How-to-inform-a-Model-TableView-that-some-data-changed
		subprocess.Popen([__file__])
		sys.exit(0)

	def action_set_settings(self):
		saver = ChangeSettings()
		if saver.exec_() == QDialog.Accepted:
			self.statusbar.showMessage('Данные сохранены')
			return True
		else:
			self.statusbar.showMessage('Ошибка сохранения данных!')
		return

	def action_set_settings_old(self):
		saver = Login()
		if saver.exec_() == QDialog.Accepted:
			self.statusbar.showMessage('Данные сохранены')
			return True
		else:
			self.statusbar.showMessage('Ошибка сохранения данных!')
		return

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

class ChangeSettings(QDialog):
	def __init__(self, parent=None):
		super(ChangeSettings, self).__init__(parent)
		self.sett = AppSettings()

		self.loginLabel = QLabel("Login: ")
		self.textName = QLineEdit(self)
		self.textName.setText(self.sett.getParametr("username"))

		self.passwordLabel = QLabel("Password: ")
		self.textPass = QLineEdit(self)
		self.textPass.setText(self.sett.getParametr("password"))

		self.periodLabel = QLabel("Период обновления: ")
		self.listWidget = QListWidget()
		for i in ('не обновлять','15','30','60'):
			item = QListWidgetItem(i)
			self.listWidget.addItem(item)
		refresh_period = self.sett.getParametr("refresh_period")
		if refresh_period:
			for i in self.listWidget.findItems(refresh_period, Qt.MatchFixedString):
				if i.text() == refresh_period:
					self.listWidget.setCurrentItem(i)
					break

		self.buttonSave = QPushButton('Сохранить', self)
		self.buttonSave.clicked.connect(self.handleSubmit)

		layout = QVBoxLayout(self)
		layout.addWidget(self.loginLabel)
		layout.addWidget(self.textName)
		layout.addWidget(self.passwordLabel)
		layout.addWidget(self.textPass)
		layout.addWidget(self.periodLabel)
		layout.addWidget(self.listWidget)
		layout.addWidget(self.buttonSave)

	def handleSubmit(self):
		self.sett.setParametr("username", self.textName.text())
		self.sett.setParametr("password", self.textPass.text())
		if int(self.listWidget.selectedItems()[0].text()) > 0:
			refresh_period = self.sett.setParametr("refresh_period", self.listWidget.selectedItems()[0].text())	
		else:
			refresh_period = self.sett.setParametr("refresh_period", '0')
		self.accept()

class Login(QDialog):
	def __init__(self, parent=None):
		super(Login, self).__init__(parent)
		self.textName = QLineEdit(self)
		self.textName.setText("login")
		self.textPass = QLineEdit(self)
		self.textPass.setText("password")
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
		# self.win.setWindowState(Qt.WindowActive)
		AppSettings.setParametr(self.win.sett, "window_state", 'shown');
		return True

	def trayActivated(self, reason):
		if reason == QSystemTrayIcon.DoubleClick:
			self.show_action()
		elif reason == QSystemTrayIcon.Trigger:
			CommonTools.show_popup('всего баллов', str(self.kpi))    

	def create_large_icon(self, text):
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

	def create_icon(self, text):
		if not text: return
		font = QFont("Arial", 26)
		font.setWeight(600)
		pixmap = QPixmap(64, 64)
		pixmap.fill(Qt.white)
		
		painter = QPainter()
		painter.begin(pixmap)
		painter.setFont(font)
		painter.setPen(QColor(0, 0, 0))
		painter.drawText(1, 14, 64, 64, Qt.AlignLeft, text)
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

	def closeEvent(window):
		sett.setParametr("geometry", window.saveGeometry());
		# sett.setParametr("windowState", app.saveState());
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
	icon_data = ''
	userpos = 0
	users = []

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

		try:
			cdict = json.loads(rjson)
		except:
			raise ValueError('Сервер вернул пустой ответ')

		full_url = domain_url + api_uri + api_employees_get
		rjson = GetKPI.get_auth_url(full_url, username, password)
		
		try:
			udict = json.loads(rjson)
		except:
			raise ValueError('Сервер вернул пустой ответ')

		data_list = []

		for record in cdict:
			user_data = ()

			emp_name = str(udict[record]['name'])
			grade = str(udict[record]['grade_name'])

			users += [emp_name,]

			user_data += (emp_name + " (" + grade + ")",)

			if (udict[record]['login'] == username) and (icon_data == ''):
				icon_data = str(cdict[record]['result'])
				notify_name = emp_name

			od = collections.OrderedDict(sorted(cdict[record].items(), reverse=True))
			for r_feild in od:
				try:
					indicator_name = split_header(str(result_rus_dict[r_feild]))
				except KeyError as e:
					indicator_name = str(r_feild)
					# raise ValueError('Undefined unit: {}'.format(e.args[0]))

				if len(header) <= len(od):
					header = header + [indicator_name,]

				indicator = round(float(cdict[record][r_feild]),2)
				# user_data += (str(indicator) + " (" + indicator_name + ")",)
				user_data += (indicator,)
			data_list = data_list + [user_data,]
		
		userpos = sorted(users).index(notify_name)

		win = MyWindow(data_list, header, userpos)
		app.aboutToQuit.connect(lambda: CommonTools.closeEvent(win))

		trayIcon = SystemTrayIcon(QIcon(img_path+"app.png"), win, icon_data)
		trayIcon.setIcon(QIcon(trayIcon.create_icon(icon_data)))

		trayIcon.setToolTip(icon_data)
		trayIcon.show()

		win.setMinimumSize(800, 600)
		win.resize(1024, 768)

		last_geom = sett.getParametr("geometry")
		window_state = sett.getParametr("window_state")
		refresh_period = int(sett.getParametr("refresh_period"))*60000
		if not refresh_period:
			refresh_period = 1800000 # 30 min

		if last_geom:
			if type(last_geom) is not bytearray:
				last_geom = bytearray()
				last_geom.extend(sett.getParametr("geometry"))
			win.restoreGeometry(last_geom)
		if window_state == 'minimized':
			win.setWindowState(Qt.WindowMinimized)
		else:
			win.show()
		win.statusbar.showMessage('Ready')
		CommonTools.show_popup(notify_name +' - всего баллов', icon_data)

		timer = QTimer()
		timer.timeout.connect(lambda: win.action_reload())
		timer.start(refresh_period) # 60000 trigger every minute.
		
		app.exec_()

	else:
		app.quit
		

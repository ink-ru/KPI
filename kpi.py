#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re, urllib, operator, json, collections
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import pcal
import kpi_dicts

# import signal # TODO add time limit

import socket
socket.setdefaulttimeout(10)

class AppSettings():
	def __init__(self, parent=None):
		super(GetKPI, self).__init__(parent)
		self.authstring = settings.value('authstring')

	def getParametr(self, name):
		if self.name != None:
			return self.name
		value = settings.value(name)
		return value

	def setParametr(self, name, value):
		self.name = value
		settings.setValue(name, value)
		return True

class GetKPI():
	def __init__(self, parent=None):
		super(GetKPI, self).__init__(parent)
		# add init code here

	def get_auth_url(self, url, username, password):		
		data = urllib.parse.urlencode({'ldap-mail': username, 'ldap-pass': password, 'go': ' Войти '})
		data = data.encode('ascii') # data should be bytes
		request = urllib.request.Request(url, data)
		resorce = urllib.request.urlopen(request)
		html = resorce.read().decode("utf-8").strip()
		return html

class MyWindow(QWidget):
	def __init__(self, data_list, header, *args):
		QWidget.__init__(self, *args)
		# setGeometry(x_pos, y_pos, width, height)
		self.setGeometry(300, 200, 570, 450)
		self.setWindowTitle("Click on column title to sort")
		table_model = MyTableModel(self, data_list, header)
		table_view = QTableView()
		table_view.setModel(table_model)
		# set font
		font = QFont("Courier New", 14)
		table_view.setFont(font)
		# set column width to fit contents (set font first!)
		table_view.resizeColumnsToContents()
		# enable sorting
		table_view.setSortingEnabled(True)
		layout = QVBoxLayout(self)
		layout.addWidget(table_view)
		self.setLayout(layout)

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
	def headerData(self, col, orientation, role):
		if orientation == Qt.Horizontal and role == Qt.DisplayRole:
			return self.header[col]
		return None
	def sort(self, col, order):
		"""sort table by given column number col"""
		self.emit(SIGNAL("layoutAboutToBeChanged()"))
		self.mylist = sorted(self.mylist,
			key=operator.itemgetter(col))
		if order == Qt.DescendingOrder:
			self.mylist.reverse()
		self.emit(SIGNAL("layoutChanged()"))

header = ['Solvent Name', ' BP (deg C)', ' MP (deg C)', ' Density (g/ml)']

data_list = [
	('ACETIC ACID', 117.9, 16.7, 1.049),
	('ACETIC ANHYDRIDE', 140.1, -73.1, 1.087),
	('ACETONE', 56.3, -94.7, 0.791),
	('ACETONITRILE', 81.6, -43.8, 0.786),
	('XYLENES', 139.1, -47.8, 0.86)
	]

app = QApplication([])
win = MyWindow(data_list, header)
win.resize(1024, 768)
win.show()
app.exec_()

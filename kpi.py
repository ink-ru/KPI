#!/usr/bin/python
# -*- coding: utf-8 -*-

import re, urllib, random, json, collections
from PyQt4.QtCore import QSettings
from PyQt4 import QtGui

# import signal # TODO add time limit

import pcal
import kpi_dicts

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

class KPITable(QtGui.QDialog):

	def __init__(self, parent=None):
		super(KPITable, self).__init__(parent)
		self.layout = QtGui.QGridLayout()

		# self.led = QtGui.QLineEdit("Sample")
		# layout.addWidget(self.led, 0, 0)

		self.table = QtGui.QTableWidget()
		self.table.setRowCount(5)
		self.table.setColumnCount(5)	
		self.layout.addWidget(self.table, 1, 0)

	def retriveData(self):
		self.table.setItem(1, 0, QtGui.QTableWidgetItem('text0'))

		# insert row
		rowPosition = self.table.rowCount()
		self.table.insertRow(rowPosition)

		self.table.setItem(rowPosition , 0, QtGui.QTableWidgetItem("text1"))
		self.table.setItem(rowPosition , 1, QtGui.QTableWidgetItem("text2"))
		self.table.setItem(rowPosition , 2, QtGui.QTableWidgetItem("text3"))

	def render(self):
		self.setLayout(self.layout)

if __name__ == '__main__':
	import sys
	app = QtGui.QApplication(sys.argv)
	t = KPITable()
	t.resize(1024, 768)
	t.retriveData()
	t.render()
	t.show()
	sys.exit(app.exec_())

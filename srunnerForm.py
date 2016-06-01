# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'scriptrunner.ui'
#
# Created: Tue Sep 22 08:56:14 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_ScriptRunner(object):
    def setupUi(self, ScriptRunner):
        ScriptRunner.setObjectName(_fromUtf8("ScriptRunner"))
        ScriptRunner.resize(935, 700)
        self.centralWidget = QtGui.QWidget(ScriptRunner)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralWidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.tabWidget = QtGui.QTabWidget(self.centralWidget)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.tab)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.logo = QtGui.QLabel(self.tab)
        self.logo.setText(_fromUtf8(""))
        self.logo.setPixmap(QtGui.QPixmap(_fromUtf8("../Документы/RusCyborg/Logox.png")))
        self.logo.setObjectName(_fromUtf8("logo"))
        self.horizontalLayout_2.addWidget(self.logo)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.tab_2)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 0, 2, 1, 1)
        self.runScripts = QtGui.QPushButton(self.tab_2)
        self.runScripts.setObjectName(_fromUtf8("runScripts"))
        self.gridLayout_2.addWidget(self.runScripts, 1, 1, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem3, 0, 0, 1, 1)
        self.tableScripts = QtGui.QTableWidget(self.tab_2)
        self.tableScripts.setObjectName(_fromUtf8("tableScripts"))
        self.tableScripts.setColumnCount(2)
        self.tableScripts.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableScripts.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableScripts.setHorizontalHeaderItem(1, item)
        self.gridLayout_2.addWidget(self.tableScripts, 0, 1, 1, 1)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.horizontalLayout.addWidget(self.tabWidget)
        ScriptRunner.setCentralWidget(self.centralWidget)

        self.retranslateUi(ScriptRunner)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ScriptRunner)

    def retranslateUi(self, ScriptRunner):
        ScriptRunner.setWindowTitle(_translate("ScriptRunner", "ScriptRunner", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("ScriptRunner", "Main", None))
        self.runScripts.setText(_translate("ScriptRunner", "Run Script", None))
        item = self.tableScripts.horizontalHeaderItem(0)
        item.setText(_translate("ScriptRunner", "Script", None))
        item = self.tableScripts.horizontalHeaderItem(1)
        item.setText(_translate("ScriptRunner", "Hot Key", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("ScriptRunner", "Scripts", None))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/OpenDialog.ui'
#
# Created: Fri Nov  5 10:51:10 2010
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_OpenDialog(object):
    def setupUi(self, OpenDialog):
        OpenDialog.setObjectName("OpenDialog")
        OpenDialog.resize(194, 310)
        OpenDialog.setModal(False)
        self.verticalLayout = QtGui.QVBoxLayout(OpenDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(OpenDialog)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setMargin(2)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.connectionList = QtGui.QListWidget(OpenDialog)
        self.connectionList.setObjectName("connectionList")
        self.verticalLayout.addWidget(self.connectionList)
        self.buttonBox = QtGui.QDialogButtonBox(OpenDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(OpenDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), OpenDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), OpenDialog.reject)
        QtCore.QObject.connect(self.connectionList, QtCore.SIGNAL("itemActivated(QListWidgetItem*)"), OpenDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(OpenDialog)

    def retranslateUi(self, OpenDialog):
        OpenDialog.setWindowTitle(QtGui.QApplication.translate("OpenDialog", "Syleqt Open", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("OpenDialog", "Open Connection", None, QtGui.QApplication.UnicodeUTF8))


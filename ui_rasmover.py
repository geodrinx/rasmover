# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_rasmover.ui'
#
# Created: Mon Mar 24 11:52:16 2014
#      by: PyQt4 UI code generator 4.10.3
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

class Ui_rasmover(object):
    def setupUi(self, rasmover):
        rasmover.setObjectName(_fromUtf8("rasmover"))
        rasmover.resize(400, 300)
        self.buttonBox = QtGui.QDialogButtonBox(rasmover)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))

        self.retranslateUi(rasmover)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), rasmover.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), rasmover.reject)
        QtCore.QMetaObject.connectSlotsByName(rasmover)

    def retranslateUi(self, rasmover):
        rasmover.setWindowTitle(_translate("rasmover", "rasmover", None))


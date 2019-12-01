# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src\main\python\cguis\design\info_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_InfoDialog(object):
    def setupUi(self, InfoDialog):
        InfoDialog.setObjectName("InfoDialog")
        InfoDialog.resize(640, 480)
        InfoDialog.setWindowTitle("Dialog")
        self.gridLayout = QtWidgets.QGridLayout(InfoDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.colors = QtWidgets.QWidget(InfoDialog)
        self.colors.setMinimumSize(QtCore.QSize(240, 160))
        self.colors.setMaximumSize(QtCore.QSize(240, 160))
        self.colors.setObjectName("colors")
        self.gridLayout.addWidget(self.colors, 0, 0, 3, 1)
        self.info_label = QtWidgets.QLabel(InfoDialog)
        self.info_label.setMinimumSize(QtCore.QSize(250, 60))
        self.info_label.setMaximumSize(QtCore.QSize(250, 60))
        self.info_label.setObjectName("info_label")
        self.gridLayout.addWidget(self.info_label, 0, 1, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(408, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 3, 1, 1)
        self.name_label = QtWidgets.QLabel(InfoDialog)
        self.name_label.setMinimumSize(QtCore.QSize(60, 30))
        self.name_label.setMaximumSize(QtCore.QSize(60, 30))
        self.name_label.setObjectName("name_label")
        self.gridLayout.addWidget(self.name_label, 1, 1, 1, 1)
        self.name_ledit = QtWidgets.QLineEdit(InfoDialog)
        self.name_ledit.setMinimumSize(QtCore.QSize(200, 30))
        self.name_ledit.setMaximumSize(QtCore.QSize(200, 30))
        self.name_ledit.setObjectName("name_ledit")
        self.gridLayout.addWidget(self.name_ledit, 1, 2, 1, 1)
        self.rule_label = QtWidgets.QLabel(InfoDialog)
        self.rule_label.setMinimumSize(QtCore.QSize(60, 30))
        self.rule_label.setMaximumSize(QtCore.QSize(60, 30))
        self.rule_label.setObjectName("rule_label")
        self.gridLayout.addWidget(self.rule_label, 2, 1, 1, 1)
        self.hm_rule_label = QtWidgets.QLabel(InfoDialog)
        self.hm_rule_label.setMinimumSize(QtCore.QSize(150, 30))
        self.hm_rule_label.setMaximumSize(QtCore.QSize(150, 30))
        self.hm_rule_label.setObjectName("hm_rule_label")
        self.gridLayout.addWidget(self.hm_rule_label, 2, 2, 1, 1)
        self.desc_label = QtWidgets.QLabel(InfoDialog)
        self.desc_label.setMinimumSize(QtCore.QSize(0, 50))
        self.desc_label.setMaximumSize(QtCore.QSize(16777215, 50))
        self.desc_label.setObjectName("desc_label")
        self.gridLayout.addWidget(self.desc_label, 3, 0, 1, 1)
        self.desc_tedit = QtWidgets.QTextEdit(InfoDialog)
        self.desc_tedit.setObjectName("desc_tedit")
        self.gridLayout.addWidget(self.desc_tedit, 4, 0, 1, 4)
        self.buttonBox = QtWidgets.QDialogButtonBox(InfoDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 4)

        self.retranslateUi(InfoDialog)
        self.buttonBox.accepted.connect(InfoDialog.accept)
        self.buttonBox.rejected.connect(InfoDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(InfoDialog)

    def retranslateUi(self, InfoDialog):
        _translate = QtCore.QCoreApplication.translate
        self.info_label.setText(_translate("InfoDialog", "Color Set Information"))
        self.name_label.setText(_translate("InfoDialog", "Name:"))
        self.rule_label.setText(_translate("InfoDialog", "Rule:"))
        self.hm_rule_label.setText(_translate("InfoDialog", "hm_rule"))
        self.desc_label.setText(_translate("InfoDialog", "Description"))

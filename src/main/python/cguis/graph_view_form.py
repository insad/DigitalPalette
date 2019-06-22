# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'graph_view_form.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_graph_view(object):
    def setupUi(self, graph_view):
        graph_view.setObjectName("graph_view")
        graph_view.resize(600, 399)
        self.cobox_chl = QtWidgets.QComboBox(graph_view)
        self.cobox_chl.setGeometry(QtCore.QRect(105, 10, 35, 20))
        self.cobox_chl.setMinimumSize(QtCore.QSize(35, 20))
        self.cobox_chl.setMaximumSize(QtCore.QSize(35, 20))
        self.cobox_chl.setObjectName("cobox_chl")
        self.cobox_chl.addItem("")
        self.cobox_chl.addItem("")
        self.cobox_chl.addItem("")
        self.cobox_chl.addItem("")
        self.gview = QtWidgets.QGraphicsView(graph_view)
        self.gview.setGeometry(QtCore.QRect(0, 0, 256, 192))
        self.gview.setObjectName("gview")
        self.cobox_gph = QtWidgets.QComboBox(graph_view)
        self.cobox_gph.setGeometry(QtCore.QRect(10, 10, 35, 20))
        self.cobox_gph.setMinimumSize(QtCore.QSize(35, 20))
        self.cobox_gph.setMaximumSize(QtCore.QSize(35, 20))
        self.cobox_gph.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContentsOnFirstShow)
        self.cobox_gph.setObjectName("cobox_gph")
        self.cobox_gph.addItem("")
        self.cobox_gph.addItem("")
        self.cobox_gph.addItem("")
        self.cobox_gph.addItem("")
        self.gview.raise_()
        self.cobox_chl.raise_()
        self.cobox_gph.raise_()

        self.retranslateUi(graph_view)
        QtCore.QMetaObject.connectSlotsByName(graph_view)

    def retranslateUi(self, graph_view):
        _translate = QtCore.QCoreApplication.translate
        graph_view.setWindowTitle(_translate("graph_view", "Form"))
        self.cobox_chl.setItemText(0, _translate("graph_view", "A"))
        self.cobox_chl.setItemText(1, _translate("graph_view", "1"))
        self.cobox_chl.setItemText(2, _translate("graph_view", "2"))
        self.cobox_chl.setItemText(3, _translate("graph_view", "3"))
        self.cobox_gph.setItemText(0, _translate("graph_view", "N"))
        self.cobox_gph.setItemText(1, _translate("graph_view", "V"))
        self.cobox_gph.setItemText(2, _translate("graph_view", "H"))
        self.cobox_gph.setItemText(3, _translate("graph_view", "F"))



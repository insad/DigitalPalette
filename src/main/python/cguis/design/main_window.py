# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src\main\python\cguis\design\main_window.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(400, 300))
        MainWindow.setWindowTitle("MainWindow")
        self.central_widget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.central_widget.sizePolicy().hasHeightForWidth())
        self.central_widget.setSizePolicy(sizePolicy)
        self.central_widget.setObjectName("central_widget")
        MainWindow.setCentralWidget(self.central_widget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.result_dock_widget = QtWidgets.QDockWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.result_dock_widget.sizePolicy().hasHeightForWidth())
        self.result_dock_widget.setSizePolicy(sizePolicy)
        self.result_dock_widget.setMinimumSize(QtCore.QSize(400, 125))
        self.result_dock_widget.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea|QtCore.Qt.TopDockWidgetArea)
        self.result_dock_widget.setObjectName("result_dock_widget")
        self.result_dock_contents = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.result_dock_contents.sizePolicy().hasHeightForWidth())
        self.result_dock_contents.setSizePolicy(sizePolicy)
        self.result_dock_contents.setObjectName("result_dock_contents")
        self.result_dock_widget.setWidget(self.result_dock_contents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.result_dock_widget)
        self.rule_dock_widget = QtWidgets.QDockWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rule_dock_widget.sizePolicy().hasHeightForWidth())
        self.rule_dock_widget.setSizePolicy(sizePolicy)
        self.rule_dock_widget.setMinimumSize(QtCore.QSize(165, 90))
        self.rule_dock_widget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.rule_dock_widget.setObjectName("rule_dock_widget")
        self.rule_dock_contents = QtWidgets.QWidget()
        self.rule_dock_contents.setObjectName("rule_dock_contents")
        self.rule_dock_widget.setWidget(self.rule_dock_contents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.rule_dock_widget)
        self.operation_dock_widget = QtWidgets.QDockWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.operation_dock_widget.sizePolicy().hasHeightForWidth())
        self.operation_dock_widget.setSizePolicy(sizePolicy)
        self.operation_dock_widget.setMinimumSize(QtCore.QSize(165, 90))
        self.operation_dock_widget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.operation_dock_widget.setObjectName("operation_dock_widget")
        self.operation_dock_contents = QtWidgets.QWidget()
        self.operation_dock_contents.setObjectName("operation_dock_contents")
        self.operation_dock_widget.setWidget(self.operation_dock_contents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.operation_dock_widget)
        self.mode_dock_widget = QtWidgets.QDockWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mode_dock_widget.sizePolicy().hasHeightForWidth())
        self.mode_dock_widget.setSizePolicy(sizePolicy)
        self.mode_dock_widget.setMinimumSize(QtCore.QSize(165, 90))
        self.mode_dock_widget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.mode_dock_widget.setObjectName("mode_dock_widget")
        self.mode_dock_contents = QtWidgets.QWidget()
        self.mode_dock_contents.setObjectName("mode_dock_contents")
        self.mode_dock_widget.setWidget(self.mode_dock_contents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.mode_dock_widget)
        self.channel_dock_widget = QtWidgets.QDockWidget(MainWindow)
        self.channel_dock_widget.setMinimumSize(QtCore.QSize(165, 90))
        self.channel_dock_widget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.channel_dock_widget.setObjectName("channel_dock_widget")
        self.channel_dock_contents = QtWidgets.QWidget()
        self.channel_dock_contents.setObjectName("channel_dock_contents")
        self.channel_dock_widget.setWidget(self.channel_dock_contents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.channel_dock_widget)
        self.transformation_dock_widget = QtWidgets.QDockWidget(MainWindow)
        self.transformation_dock_widget.setMinimumSize(QtCore.QSize(165, 42))
        self.transformation_dock_widget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.transformation_dock_widget.setObjectName("transformation_dock_widget")
        self.transformation_dock_contents = QtWidgets.QWidget()
        self.transformation_dock_contents.setObjectName("transformation_dock_contents")
        self.transformation_dock_widget.setWidget(self.transformation_dock_contents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.transformation_dock_widget)
        self.actionImport = QtWidgets.QAction(MainWindow)
        self.actionImport.setObjectName("actionImport")
        self.actionExport = QtWidgets.QAction(MainWindow)
        self.actionExport.setObjectName("actionExport")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionCreate = QtWidgets.QAction(MainWindow)
        self.actionCreate.setObjectName("actionCreate")
        self.actionLocate = QtWidgets.QAction(MainWindow)
        self.actionLocate.setObjectName("actionLocate")
        self.actionSettings = QtWidgets.QAction(MainWindow)
        self.actionSettings.setObjectName("actionSettings")
        self.actionHomepage = QtWidgets.QAction(MainWindow)
        self.actionHomepage.setObjectName("actionHomepage")
        self.actionUpdate = QtWidgets.QAction(MainWindow)
        self.actionUpdate.setObjectName("actionUpdate")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionRule = QtWidgets.QAction(MainWindow)
        self.actionRule.setObjectName("actionRule")
        self.actionChannel = QtWidgets.QAction(MainWindow)
        self.actionChannel.setObjectName("actionChannel")
        self.actionOperation = QtWidgets.QAction(MainWindow)
        self.actionOperation.setObjectName("actionOperation")
        self.actionMode = QtWidgets.QAction(MainWindow)
        self.actionMode.setObjectName("actionMode")
        self.actionTransformation = QtWidgets.QAction(MainWindow)
        self.actionTransformation.setObjectName("actionTransformation")
        self.actionResult = QtWidgets.QAction(MainWindow)
        self.actionResult.setObjectName("actionResult")
        self.actionAttach = QtWidgets.QAction(MainWindow)
        self.actionAttach.setObjectName("actionAttach")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionImport)
        self.menuFile.addAction(self.actionExport)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuEdit.addAction(self.actionCreate)
        self.menuEdit.addAction(self.actionLocate)
        self.menuEdit.addAction(self.actionAttach)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionSettings)
        self.menuView.addAction(self.actionRule)
        self.menuView.addAction(self.actionChannel)
        self.menuView.addAction(self.actionOperation)
        self.menuView.addAction(self.actionMode)
        self.menuView.addAction(self.actionTransformation)
        self.menuView.addAction(self.actionResult)
        self.menuHelp.addAction(self.actionHomepage)
        self.menuHelp.addAction(self.actionUpdate)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.result_dock_widget.setToolTip(_translate("MainWindow", "Display and modify color set result."))
        self.result_dock_widget.setWindowTitle(_translate("MainWindow", "Result"))
        self.rule_dock_widget.setToolTip(_translate("MainWindow", "Set harmony rule for color set."))
        self.rule_dock_widget.setWindowTitle(_translate("MainWindow", "Rule"))
        self.operation_dock_widget.setToolTip(_translate("MainWindow", "Manipulate files and work area."))
        self.operation_dock_widget.setWindowTitle(_translate("MainWindow", "Operation"))
        self.mode_dock_widget.setToolTip(_translate("MainWindow", "Set display mode for color set result."))
        self.mode_dock_widget.setWindowTitle(_translate("MainWindow", "Mode"))
        self.channel_dock_widget.setToolTip(_translate("MainWindow", "Set category and channel for opened graph."))
        self.channel_dock_widget.setWindowTitle(_translate("MainWindow", "Channel"))
        self.transformation_dock_widget.setToolTip(_translate("MainWindow", "Move and zoom graph and depot content."))
        self.transformation_dock_widget.setWindowTitle(_translate("MainWindow", "Transformation"))
        self.actionImport.setText(_translate("MainWindow", "Import"))
        self.actionExport.setText(_translate("MainWindow", "Export"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionCreate.setText(_translate("MainWindow", "Create"))
        self.actionLocate.setText(_translate("MainWindow", "Locate"))
        self.actionSettings.setText(_translate("MainWindow", "Settings"))
        self.actionHomepage.setText(_translate("MainWindow", "Homepage"))
        self.actionUpdate.setText(_translate("MainWindow", "Update"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionRule.setText(_translate("MainWindow", "Rule"))
        self.actionChannel.setText(_translate("MainWindow", "Channel"))
        self.actionOperation.setText(_translate("MainWindow", "Operation"))
        self.actionMode.setText(_translate("MainWindow", "Mode"))
        self.actionTransformation.setText(_translate("MainWindow", "Transformation"))
        self.actionResult.setText(_translate("MainWindow", "Result"))
        self.actionAttach.setText(_translate("MainWindow", "Attach"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionSave.setText(_translate("MainWindow", "Save"))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src\main\python\cguis\design\settings_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        SettingsDialog.setObjectName("SettingsDialog")
        SettingsDialog.resize(535, 644)
        SettingsDialog.setWindowTitle("")
        self.gridLayout = QtWidgets.QGridLayout(SettingsDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.setti_items = QtWidgets.QTabWidget(SettingsDialog)
        self.setti_items.setTabPosition(QtWidgets.QTabWidget.North)
        self.setti_items.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.setti_items.setDocumentMode(False)
        self.setti_items.setObjectName("setti_items")
        self.setti_interface = QtWidgets.QWidget()
        self.setti_interface.setObjectName("setti_interface")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.setti_interface)
        self.verticalLayout.setContentsMargins(4, 8, 4, 4)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName("verticalLayout")
        self.interface_color_square_gbox = QtWidgets.QGroupBox(self.setti_interface)
        self.interface_color_square_gbox.setObjectName("interface_color_square_gbox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.interface_color_square_gbox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.cubic_ratio_label = QtWidgets.QLabel(self.interface_color_square_gbox)
        self.cubic_ratio_label.setMinimumSize(QtCore.QSize(250, 20))
        self.cubic_ratio_label.setMaximumSize(QtCore.QSize(250, 20))
        self.cubic_ratio_label.setObjectName("cubic_ratio_label")
        self.gridLayout_2.addWidget(self.cubic_ratio_label, 0, 0, 1, 1)
        self.cubic_ratio_dp = QtWidgets.QDoubleSpinBox(self.interface_color_square_gbox)
        self.cubic_ratio_dp.setMinimumSize(QtCore.QSize(60, 0))
        self.cubic_ratio_dp.setMaximumSize(QtCore.QSize(60, 16777215))
        self.cubic_ratio_dp.setMinimum(0.0)
        self.cubic_ratio_dp.setMaximum(1.0)
        self.cubic_ratio_dp.setSingleStep(0.1)
        self.cubic_ratio_dp.setProperty("value", 0.0)
        self.cubic_ratio_dp.setObjectName("cubic_ratio_dp")
        self.gridLayout_2.addWidget(self.cubic_ratio_dp, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(447, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(248, 16, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 1, 0, 1, 2)
        self.verticalLayout.addWidget(self.interface_color_square_gbox)
        self.interface_color_wheel_gbox = QtWidgets.QGroupBox(self.setti_interface)
        self.interface_color_wheel_gbox.setObjectName("interface_color_wheel_gbox")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.interface_color_wheel_gbox)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.wheel_ratio_label = QtWidgets.QLabel(self.interface_color_wheel_gbox)
        self.wheel_ratio_label.setMinimumSize(QtCore.QSize(250, 20))
        self.wheel_ratio_label.setMaximumSize(QtCore.QSize(250, 20))
        self.wheel_ratio_label.setObjectName("wheel_ratio_label")
        self.gridLayout_4.addWidget(self.wheel_ratio_label, 0, 0, 1, 1)
        self.wheel_ratio_dp = QtWidgets.QDoubleSpinBox(self.interface_color_wheel_gbox)
        self.wheel_ratio_dp.setMinimumSize(QtCore.QSize(60, 0))
        self.wheel_ratio_dp.setMaximumSize(QtCore.QSize(60, 16777215))
        self.wheel_ratio_dp.setMinimum(0.0)
        self.wheel_ratio_dp.setMaximum(1.0)
        self.wheel_ratio_dp.setSingleStep(0.1)
        self.wheel_ratio_dp.setProperty("value", 0.0)
        self.wheel_ratio_dp.setObjectName("wheel_ratio_dp")
        self.gridLayout_4.addWidget(self.wheel_ratio_dp, 0, 1, 1, 1)
        self.volum_ratio_label = QtWidgets.QLabel(self.interface_color_wheel_gbox)
        self.volum_ratio_label.setMinimumSize(QtCore.QSize(250, 20))
        self.volum_ratio_label.setMaximumSize(QtCore.QSize(250, 20))
        self.volum_ratio_label.setObjectName("volum_ratio_label")
        self.gridLayout_4.addWidget(self.volum_ratio_label, 1, 0, 1, 1)
        self.volum_ratio_dp = QtWidgets.QDoubleSpinBox(self.interface_color_wheel_gbox)
        self.volum_ratio_dp.setMinimumSize(QtCore.QSize(60, 0))
        self.volum_ratio_dp.setMaximumSize(QtCore.QSize(60, 16777215))
        self.volum_ratio_dp.setMinimum(0.0)
        self.volum_ratio_dp.setMaximum(1.0)
        self.volum_ratio_dp.setSingleStep(0.1)
        self.volum_ratio_dp.setProperty("value", 0.0)
        self.volum_ratio_dp.setObjectName("volum_ratio_dp")
        self.gridLayout_4.addWidget(self.volum_ratio_dp, 1, 1, 1, 1)
        self.s_tag_radius_label = QtWidgets.QLabel(self.interface_color_wheel_gbox)
        self.s_tag_radius_label.setMinimumSize(QtCore.QSize(250, 20))
        self.s_tag_radius_label.setMaximumSize(QtCore.QSize(250, 20))
        self.s_tag_radius_label.setObjectName("s_tag_radius_label")
        self.gridLayout_4.addWidget(self.s_tag_radius_label, 2, 0, 1, 1)
        self.s_tag_radius_dp = QtWidgets.QDoubleSpinBox(self.interface_color_wheel_gbox)
        self.s_tag_radius_dp.setMinimumSize(QtCore.QSize(60, 0))
        self.s_tag_radius_dp.setMaximumSize(QtCore.QSize(60, 16777215))
        self.s_tag_radius_dp.setMinimum(0.0)
        self.s_tag_radius_dp.setMaximum(0.2)
        self.s_tag_radius_dp.setSingleStep(0.02)
        self.s_tag_radius_dp.setProperty("value", 0.0)
        self.s_tag_radius_dp.setObjectName("s_tag_radius_dp")
        self.gridLayout_4.addWidget(self.s_tag_radius_dp, 2, 1, 1, 1)
        self.v_tag_radius_label = QtWidgets.QLabel(self.interface_color_wheel_gbox)
        self.v_tag_radius_label.setMinimumSize(QtCore.QSize(250, 20))
        self.v_tag_radius_label.setMaximumSize(QtCore.QSize(250, 20))
        self.v_tag_radius_label.setObjectName("v_tag_radius_label")
        self.gridLayout_4.addWidget(self.v_tag_radius_label, 3, 0, 1, 1)
        self.v_tag_radius_dp = QtWidgets.QDoubleSpinBox(self.interface_color_wheel_gbox)
        self.v_tag_radius_dp.setMinimumSize(QtCore.QSize(60, 0))
        self.v_tag_radius_dp.setMaximumSize(QtCore.QSize(60, 16777215))
        self.v_tag_radius_dp.setMinimum(0.0)
        self.v_tag_radius_dp.setMaximum(0.2)
        self.v_tag_radius_dp.setSingleStep(0.02)
        self.v_tag_radius_dp.setProperty("value", 0.0)
        self.v_tag_radius_dp.setObjectName("v_tag_radius_dp")
        self.gridLayout_4.addWidget(self.v_tag_radius_dp, 3, 1, 1, 1)
        self.wheel_ed_wid_label = QtWidgets.QLabel(self.interface_color_wheel_gbox)
        self.wheel_ed_wid_label.setMinimumSize(QtCore.QSize(250, 20))
        self.wheel_ed_wid_label.setMaximumSize(QtCore.QSize(250, 20))
        self.wheel_ed_wid_label.setObjectName("wheel_ed_wid_label")
        self.gridLayout_4.addWidget(self.wheel_ed_wid_label, 4, 0, 1, 1)
        self.wheel_ed_wid_sp = QtWidgets.QSpinBox(self.interface_color_wheel_gbox)
        self.wheel_ed_wid_sp.setMinimum(0)
        self.wheel_ed_wid_sp.setMaximum(20)
        self.wheel_ed_wid_sp.setProperty("value", 0)
        self.wheel_ed_wid_sp.setObjectName("wheel_ed_wid_sp")
        self.gridLayout_4.addWidget(self.wheel_ed_wid_sp, 4, 1, 1, 1)
        self.positive_wid_label = QtWidgets.QLabel(self.interface_color_wheel_gbox)
        self.positive_wid_label.setMinimumSize(QtCore.QSize(250, 20))
        self.positive_wid_label.setMaximumSize(QtCore.QSize(250, 20))
        self.positive_wid_label.setObjectName("positive_wid_label")
        self.gridLayout_4.addWidget(self.positive_wid_label, 5, 0, 1, 1)
        self.positive_wid_sp = QtWidgets.QSpinBox(self.interface_color_wheel_gbox)
        self.positive_wid_sp.setMaximum(20)
        self.positive_wid_sp.setObjectName("positive_wid_sp")
        self.gridLayout_4.addWidget(self.positive_wid_sp, 5, 1, 1, 1)
        self.negative_wid_label = QtWidgets.QLabel(self.interface_color_wheel_gbox)
        self.negative_wid_label.setMinimumSize(QtCore.QSize(250, 20))
        self.negative_wid_label.setMaximumSize(QtCore.QSize(250, 20))
        self.negative_wid_label.setObjectName("negative_wid_label")
        self.gridLayout_4.addWidget(self.negative_wid_label, 6, 0, 1, 1)
        self.negative_wid_sp = QtWidgets.QSpinBox(self.interface_color_wheel_gbox)
        self.negative_wid_sp.setMaximum(20)
        self.negative_wid_sp.setObjectName("negative_wid_sp")
        self.gridLayout_4.addWidget(self.negative_wid_sp, 6, 1, 1, 1)
        self.wheel_ed_color_label = QtWidgets.QLabel(self.interface_color_wheel_gbox)
        self.wheel_ed_color_label.setMinimumSize(QtCore.QSize(250, 20))
        self.wheel_ed_color_label.setMaximumSize(QtCore.QSize(250, 20))
        self.wheel_ed_color_label.setObjectName("wheel_ed_color_label")
        self.gridLayout_4.addWidget(self.wheel_ed_color_label, 7, 0, 1, 1)
        self.wheel_ed_color_0_dp = QtWidgets.QSpinBox(self.interface_color_wheel_gbox)
        self.wheel_ed_color_0_dp.setMinimumSize(QtCore.QSize(60, 0))
        self.wheel_ed_color_0_dp.setMaximumSize(QtCore.QSize(60, 16777215))
        self.wheel_ed_color_0_dp.setMaximum(255)
        self.wheel_ed_color_0_dp.setObjectName("wheel_ed_color_0_dp")
        self.gridLayout_4.addWidget(self.wheel_ed_color_0_dp, 7, 1, 1, 1)
        self.wheel_ed_color_1_dp = QtWidgets.QSpinBox(self.interface_color_wheel_gbox)
        self.wheel_ed_color_1_dp.setMinimumSize(QtCore.QSize(60, 0))
        self.wheel_ed_color_1_dp.setMaximumSize(QtCore.QSize(60, 16777215))
        self.wheel_ed_color_1_dp.setMaximum(255)
        self.wheel_ed_color_1_dp.setObjectName("wheel_ed_color_1_dp")
        self.gridLayout_4.addWidget(self.wheel_ed_color_1_dp, 7, 2, 1, 1)
        self.wheel_ed_color_2_dp = QtWidgets.QSpinBox(self.interface_color_wheel_gbox)
        self.wheel_ed_color_2_dp.setMinimumSize(QtCore.QSize(60, 0))
        self.wheel_ed_color_2_dp.setMaximumSize(QtCore.QSize(60, 16777215))
        self.wheel_ed_color_2_dp.setMaximum(255)
        self.wheel_ed_color_2_dp.setObjectName("wheel_ed_color_2_dp")
        self.gridLayout_4.addWidget(self.wheel_ed_color_2_dp, 7, 3, 1, 1)
        self.positive_color_label = QtWidgets.QLabel(self.interface_color_wheel_gbox)
        self.positive_color_label.setMinimumSize(QtCore.QSize(250, 20))
        self.positive_color_label.setMaximumSize(QtCore.QSize(250, 20))
        self.positive_color_label.setObjectName("positive_color_label")
        self.gridLayout_4.addWidget(self.positive_color_label, 8, 0, 1, 1)
        self.positive_color_0_dp = QtWidgets.QSpinBox(self.interface_color_wheel_gbox)
        self.positive_color_0_dp.setMinimumSize(QtCore.QSize(60, 0))
        self.positive_color_0_dp.setMaximumSize(QtCore.QSize(60, 16777215))
        self.positive_color_0_dp.setMaximum(255)
        self.positive_color_0_dp.setProperty("value", 0)
        self.positive_color_0_dp.setObjectName("positive_color_0_dp")
        self.gridLayout_4.addWidget(self.positive_color_0_dp, 8, 1, 1, 1)
        self.positive_color_1_dp = QtWidgets.QSpinBox(self.interface_color_wheel_gbox)
        self.positive_color_1_dp.setMinimumSize(QtCore.QSize(60, 0))
        self.positive_color_1_dp.setMaximumSize(QtCore.QSize(60, 16777215))
        self.positive_color_1_dp.setMaximum(255)
        self.positive_color_1_dp.setProperty("value", 0)
        self.positive_color_1_dp.setObjectName("positive_color_1_dp")
        self.gridLayout_4.addWidget(self.positive_color_1_dp, 8, 2, 1, 1)
        self.positive_color_2_dp = QtWidgets.QSpinBox(self.interface_color_wheel_gbox)
        self.positive_color_2_dp.setMinimumSize(QtCore.QSize(60, 0))
        self.positive_color_2_dp.setMaximumSize(QtCore.QSize(60, 16777215))
        self.positive_color_2_dp.setMaximum(255)
        self.positive_color_2_dp.setProperty("value", 0)
        self.positive_color_2_dp.setObjectName("positive_color_2_dp")
        self.gridLayout_4.addWidget(self.positive_color_2_dp, 8, 3, 1, 1)
        self.negative_color_label = QtWidgets.QLabel(self.interface_color_wheel_gbox)
        self.negative_color_label.setMinimumSize(QtCore.QSize(250, 20))
        self.negative_color_label.setMaximumSize(QtCore.QSize(250, 20))
        self.negative_color_label.setObjectName("negative_color_label")
        self.gridLayout_4.addWidget(self.negative_color_label, 9, 0, 1, 1)
        self.negative_color_0_dp = QtWidgets.QSpinBox(self.interface_color_wheel_gbox)
        self.negative_color_0_dp.setMinimumSize(QtCore.QSize(60, 0))
        self.negative_color_0_dp.setMaximumSize(QtCore.QSize(60, 16777215))
        self.negative_color_0_dp.setMaximum(255)
        self.negative_color_0_dp.setProperty("value", 0)
        self.negative_color_0_dp.setObjectName("negative_color_0_dp")
        self.gridLayout_4.addWidget(self.negative_color_0_dp, 9, 1, 1, 1)
        self.negative_color_1_dp = QtWidgets.QSpinBox(self.interface_color_wheel_gbox)
        self.negative_color_1_dp.setMinimumSize(QtCore.QSize(60, 0))
        self.negative_color_1_dp.setMaximumSize(QtCore.QSize(60, 16777215))
        self.negative_color_1_dp.setMaximum(255)
        self.negative_color_1_dp.setProperty("value", 0)
        self.negative_color_1_dp.setObjectName("negative_color_1_dp")
        self.gridLayout_4.addWidget(self.negative_color_1_dp, 9, 2, 1, 1)
        self.negative_color_2_dp = QtWidgets.QSpinBox(self.interface_color_wheel_gbox)
        self.negative_color_2_dp.setMinimumSize(QtCore.QSize(60, 0))
        self.negative_color_2_dp.setMaximumSize(QtCore.QSize(60, 16777215))
        self.negative_color_2_dp.setMaximum(255)
        self.negative_color_2_dp.setProperty("value", 0)
        self.negative_color_2_dp.setObjectName("negative_color_2_dp")
        self.gridLayout_4.addWidget(self.negative_color_2_dp, 9, 3, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(64, 17, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem2, 9, 4, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(248, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem3, 10, 0, 1, 2)
        self.verticalLayout.addWidget(self.interface_color_wheel_gbox)
        self.interface_graph_view_gbox = QtWidgets.QGroupBox(self.setti_interface)
        self.interface_graph_view_gbox.setObjectName("interface_graph_view_gbox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.interface_graph_view_gbox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.circle_dist_label = QtWidgets.QLabel(self.interface_graph_view_gbox)
        self.circle_dist_label.setMinimumSize(QtCore.QSize(250, 20))
        self.circle_dist_label.setMaximumSize(QtCore.QSize(250, 20))
        self.circle_dist_label.setObjectName("circle_dist_label")
        self.gridLayout_3.addWidget(self.circle_dist_label, 0, 0, 1, 1)
        self.circle_dist_sp = QtWidgets.QSpinBox(self.interface_graph_view_gbox)
        self.circle_dist_sp.setMaximum(50)
        self.circle_dist_sp.setObjectName("circle_dist_sp")
        self.gridLayout_3.addWidget(self.circle_dist_sp, 0, 1, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(333, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem4, 0, 2, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(248, 15, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem5, 1, 0, 1, 2)
        self.verticalLayout.addWidget(self.interface_graph_view_gbox)
        self.setti_items.addTab(self.setti_interface, "")
        self.setti_rule = QtWidgets.QWidget()
        self.setti_rule.setObjectName("setti_rule")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.setti_rule)
        self.verticalLayout_2.setContentsMargins(4, 8, 4, 4)
        self.verticalLayout_2.setSpacing(4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.rule_color_square_gbox = QtWidgets.QGroupBox(self.setti_rule)
        self.rule_color_square_gbox.setObjectName("rule_color_square_gbox")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.rule_color_square_gbox)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.show_hsv_cbox = QtWidgets.QCheckBox(self.rule_color_square_gbox)
        self.show_hsv_cbox.setMinimumSize(QtCore.QSize(300, 22))
        self.show_hsv_cbox.setMaximumSize(QtCore.QSize(300, 22))
        self.show_hsv_cbox.setChecked(False)
        self.show_hsv_cbox.setObjectName("show_hsv_cbox")
        self.gridLayout_8.addWidget(self.show_hsv_cbox, 0, 0, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(314, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_8.addItem(spacerItem6, 0, 1, 1, 1)
        self.show_rgb_cbox = QtWidgets.QCheckBox(self.rule_color_square_gbox)
        self.show_rgb_cbox.setMinimumSize(QtCore.QSize(300, 22))
        self.show_rgb_cbox.setMaximumSize(QtCore.QSize(300, 22))
        self.show_rgb_cbox.setChecked(False)
        self.show_rgb_cbox.setObjectName("show_rgb_cbox")
        self.gridLayout_8.addWidget(self.show_rgb_cbox, 1, 0, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(148, 27, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_8.addItem(spacerItem7, 2, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.rule_color_square_gbox)
        self.color_wheel_gbox = QtWidgets.QGroupBox(self.setti_rule)
        self.color_wheel_gbox.setObjectName("color_wheel_gbox")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.color_wheel_gbox)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.h_range_label = QtWidgets.QLabel(self.color_wheel_gbox)
        self.h_range_label.setMinimumSize(QtCore.QSize(200, 20))
        self.h_range_label.setMaximumSize(QtCore.QSize(200, 20))
        self.h_range_label.setObjectName("h_range_label")
        self.gridLayout_5.addWidget(self.h_range_label, 0, 0, 1, 1)
        self.h_range_0_dp = QtWidgets.QDoubleSpinBox(self.color_wheel_gbox)
        self.h_range_0_dp.setMinimumSize(QtCore.QSize(60, 0))
        self.h_range_0_dp.setMaximumSize(QtCore.QSize(60, 16777215))
        self.h_range_0_dp.setMaximum(360.0)
        self.h_range_0_dp.setSingleStep(10.0)
        self.h_range_0_dp.setObjectName("h_range_0_dp")
        self.gridLayout_5.addWidget(self.h_range_0_dp, 0, 1, 1, 1)
        self.h_range_to_label = QtWidgets.QLabel(self.color_wheel_gbox)
        self.h_range_to_label.setMinimumSize(QtCore.QSize(30, 20))
        self.h_range_to_label.setMaximumSize(QtCore.QSize(30, 20))
        self.h_range_to_label.setObjectName("h_range_to_label")
        self.gridLayout_5.addWidget(self.h_range_to_label, 0, 2, 1, 1)
        self.h_range_1_dp = QtWidgets.QDoubleSpinBox(self.color_wheel_gbox)
        self.h_range_1_dp.setMinimumSize(QtCore.QSize(60, 0))
        self.h_range_1_dp.setMaximumSize(QtCore.QSize(60, 16777215))
        self.h_range_1_dp.setMaximum(360.0)
        self.h_range_1_dp.setSingleStep(10.0)
        self.h_range_1_dp.setProperty("value", 0.0)
        self.h_range_1_dp.setObjectName("h_range_1_dp")
        self.gridLayout_5.addWidget(self.h_range_1_dp, 0, 3, 1, 1)
        spacerItem8 = QtWidgets.QSpacerItem(71, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem8, 0, 4, 1, 1)
        self.s_range_label = QtWidgets.QLabel(self.color_wheel_gbox)
        self.s_range_label.setMinimumSize(QtCore.QSize(200, 20))
        self.s_range_label.setMaximumSize(QtCore.QSize(200, 20))
        self.s_range_label.setObjectName("s_range_label")
        self.gridLayout_5.addWidget(self.s_range_label, 1, 0, 1, 1)
        self.s_range_0_dp = QtWidgets.QDoubleSpinBox(self.color_wheel_gbox)
        self.s_range_0_dp.setMinimumSize(QtCore.QSize(60, 0))
        self.s_range_0_dp.setMaximumSize(QtCore.QSize(60, 16777215))
        self.s_range_0_dp.setMaximum(1.0)
        self.s_range_0_dp.setSingleStep(0.1)
        self.s_range_0_dp.setObjectName("s_range_0_dp")
        self.gridLayout_5.addWidget(self.s_range_0_dp, 1, 1, 1, 1)
        self.s_range_to_label = QtWidgets.QLabel(self.color_wheel_gbox)
        self.s_range_to_label.setMinimumSize(QtCore.QSize(30, 20))
        self.s_range_to_label.setMaximumSize(QtCore.QSize(30, 20))
        self.s_range_to_label.setObjectName("s_range_to_label")
        self.gridLayout_5.addWidget(self.s_range_to_label, 1, 2, 1, 1)
        self.s_range_1_dp = QtWidgets.QDoubleSpinBox(self.color_wheel_gbox)
        self.s_range_1_dp.setMinimumSize(QtCore.QSize(60, 0))
        self.s_range_1_dp.setMaximumSize(QtCore.QSize(60, 16777215))
        self.s_range_1_dp.setMaximum(1.0)
        self.s_range_1_dp.setSingleStep(0.1)
        self.s_range_1_dp.setProperty("value", 0.0)
        self.s_range_1_dp.setObjectName("s_range_1_dp")
        self.gridLayout_5.addWidget(self.s_range_1_dp, 1, 3, 1, 1)
        self.v_range_label = QtWidgets.QLabel(self.color_wheel_gbox)
        self.v_range_label.setMinimumSize(QtCore.QSize(200, 20))
        self.v_range_label.setMaximumSize(QtCore.QSize(200, 20))
        self.v_range_label.setObjectName("v_range_label")
        self.gridLayout_5.addWidget(self.v_range_label, 2, 0, 1, 1)
        self.v_range_0_dp = QtWidgets.QDoubleSpinBox(self.color_wheel_gbox)
        self.v_range_0_dp.setMinimumSize(QtCore.QSize(60, 0))
        self.v_range_0_dp.setMaximumSize(QtCore.QSize(60, 16777215))
        self.v_range_0_dp.setMaximum(1.0)
        self.v_range_0_dp.setSingleStep(0.1)
        self.v_range_0_dp.setObjectName("v_range_0_dp")
        self.gridLayout_5.addWidget(self.v_range_0_dp, 2, 1, 1, 1)
        self.v_range_to_label = QtWidgets.QLabel(self.color_wheel_gbox)
        self.v_range_to_label.setMinimumSize(QtCore.QSize(30, 20))
        self.v_range_to_label.setMaximumSize(QtCore.QSize(30, 20))
        self.v_range_to_label.setObjectName("v_range_to_label")
        self.gridLayout_5.addWidget(self.v_range_to_label, 2, 2, 1, 1)
        self.v_range_1_dp = QtWidgets.QDoubleSpinBox(self.color_wheel_gbox)
        self.v_range_1_dp.setMinimumSize(QtCore.QSize(60, 0))
        self.v_range_1_dp.setMaximumSize(QtCore.QSize(60, 16777215))
        self.v_range_1_dp.setMaximum(1.0)
        self.v_range_1_dp.setSingleStep(0.1)
        self.v_range_1_dp.setProperty("value", 0.0)
        self.v_range_1_dp.setObjectName("v_range_1_dp")
        self.gridLayout_5.addWidget(self.v_range_1_dp, 2, 3, 1, 1)
        self.hm_rule_label = QtWidgets.QLabel(self.color_wheel_gbox)
        self.hm_rule_label.setMinimumSize(QtCore.QSize(200, 20))
        self.hm_rule_label.setMaximumSize(QtCore.QSize(200, 20))
        self.hm_rule_label.setObjectName("hm_rule_label")
        self.gridLayout_5.addWidget(self.hm_rule_label, 3, 0, 1, 1)
        self.hm_rule_comb = QtWidgets.QComboBox(self.color_wheel_gbox)
        self.hm_rule_comb.setMinimumSize(QtCore.QSize(120, 22))
        self.hm_rule_comb.setMaximumSize(QtCore.QSize(120, 22))
        self.hm_rule_comb.setObjectName("hm_rule_comb")
        self.gridLayout_5.addWidget(self.hm_rule_comb, 3, 1, 1, 2)
        self.overflow_label = QtWidgets.QLabel(self.color_wheel_gbox)
        self.overflow_label.setMinimumSize(QtCore.QSize(200, 20))
        self.overflow_label.setMaximumSize(QtCore.QSize(200, 20))
        self.overflow_label.setObjectName("overflow_label")
        self.gridLayout_5.addWidget(self.overflow_label, 4, 0, 1, 1)
        self.overflow_comb = QtWidgets.QComboBox(self.color_wheel_gbox)
        self.overflow_comb.setMinimumSize(QtCore.QSize(120, 22))
        self.overflow_comb.setMaximumSize(QtCore.QSize(120, 22))
        self.overflow_comb.setObjectName("overflow_comb")
        self.gridLayout_5.addWidget(self.overflow_comb, 4, 1, 1, 2)
        self.color_wheel_inner_space = QtWidgets.QWidget(self.color_wheel_gbox)
        self.color_wheel_inner_space.setMinimumSize(QtCore.QSize(0, 20))
        self.color_wheel_inner_space.setMaximumSize(QtCore.QSize(16777215, 20))
        self.color_wheel_inner_space.setObjectName("color_wheel_inner_space")
        self.gridLayout_5.addWidget(self.color_wheel_inner_space, 5, 0, 1, 5)
        self.press_move_cbox = QtWidgets.QCheckBox(self.color_wheel_gbox)
        self.press_move_cbox.setMinimumSize(QtCore.QSize(300, 22))
        self.press_move_cbox.setMaximumSize(QtCore.QSize(300, 22))
        self.press_move_cbox.setChecked(False)
        self.press_move_cbox.setObjectName("press_move_cbox")
        self.gridLayout_5.addWidget(self.press_move_cbox, 6, 0, 1, 3)
        spacerItem9 = QtWidgets.QSpacerItem(308, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_5.addItem(spacerItem9, 7, 0, 1, 4)
        self.verticalLayout_2.addWidget(self.color_wheel_gbox)
        self.rule_graph_view_gbox = QtWidgets.QGroupBox(self.setti_rule)
        self.rule_graph_view_gbox.setObjectName("rule_graph_view_gbox")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.rule_graph_view_gbox)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.zoom_step_label = QtWidgets.QLabel(self.rule_graph_view_gbox)
        self.zoom_step_label.setMinimumSize(QtCore.QSize(200, 20))
        self.zoom_step_label.setMaximumSize(QtCore.QSize(200, 20))
        self.zoom_step_label.setObjectName("zoom_step_label")
        self.gridLayout_7.addWidget(self.zoom_step_label, 0, 0, 1, 1)
        self.zoom_step_dp = QtWidgets.QDoubleSpinBox(self.rule_graph_view_gbox)
        self.zoom_step_dp.setMinimumSize(QtCore.QSize(60, 0))
        self.zoom_step_dp.setMaximumSize(QtCore.QSize(60, 16777215))
        self.zoom_step_dp.setMinimum(1.0)
        self.zoom_step_dp.setMaximum(10.0)
        self.zoom_step_dp.setSingleStep(0.05)
        self.zoom_step_dp.setProperty("value", 1.0)
        self.zoom_step_dp.setObjectName("zoom_step_dp")
        self.gridLayout_7.addWidget(self.zoom_step_dp, 0, 1, 1, 1)
        spacerItem10 = QtWidgets.QSpacerItem(164, 18, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem10, 0, 2, 1, 1)
        self.move_step_label = QtWidgets.QLabel(self.rule_graph_view_gbox)
        self.move_step_label.setMinimumSize(QtCore.QSize(200, 20))
        self.move_step_label.setMaximumSize(QtCore.QSize(200, 20))
        self.move_step_label.setObjectName("move_step_label")
        self.gridLayout_7.addWidget(self.move_step_label, 1, 0, 1, 1)
        self.move_step_dp = QtWidgets.QSpinBox(self.rule_graph_view_gbox)
        self.move_step_dp.setMinimumSize(QtCore.QSize(60, 0))
        self.move_step_dp.setMaximumSize(QtCore.QSize(60, 16777215))
        self.move_step_dp.setMinimum(1)
        self.move_step_dp.setMaximum(100)
        self.move_step_dp.setProperty("value", 1)
        self.move_step_dp.setObjectName("move_step_dp")
        self.gridLayout_7.addWidget(self.move_step_dp, 1, 1, 1, 1)
        spacerItem11 = QtWidgets.QSpacerItem(298, 31, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_7.addItem(spacerItem11, 2, 0, 1, 2)
        self.verticalLayout_2.addWidget(self.rule_graph_view_gbox)
        self.setti_items.addTab(self.setti_rule, "")
        self.setti_system = QtWidgets.QWidget()
        self.setti_system.setObjectName("setti_system")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.setti_system)
        self.verticalLayout_3.setContentsMargins(4, 8, 4, 4)
        self.verticalLayout_3.setSpacing(4)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.system_work_space_gbox = QtWidgets.QGroupBox(self.setti_system)
        self.system_work_space_gbox.setMinimumSize(QtCore.QSize(0, 0))
        self.system_work_space_gbox.setObjectName("system_work_space_gbox")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.system_work_space_gbox)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.lang_label = QtWidgets.QLabel(self.system_work_space_gbox)
        self.lang_label.setMinimumSize(QtCore.QSize(200, 20))
        self.lang_label.setMaximumSize(QtCore.QSize(200, 20))
        self.lang_label.setObjectName("lang_label")
        self.gridLayout_6.addWidget(self.lang_label, 0, 0, 1, 1)
        self.lang_comb = QtWidgets.QComboBox(self.system_work_space_gbox)
        self.lang_comb.setMinimumSize(QtCore.QSize(160, 0))
        self.lang_comb.setMaximumSize(QtCore.QSize(200, 16777215))
        self.lang_comb.setObjectName("lang_comb")
        self.gridLayout_6.addWidget(self.lang_comb, 0, 1, 1, 1)
        spacerItem12 = QtWidgets.QSpacerItem(98, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem12, 0, 2, 1, 1)
        self.usr_color_label = QtWidgets.QLabel(self.system_work_space_gbox)
        self.usr_color_label.setMinimumSize(QtCore.QSize(200, 20))
        self.usr_color_label.setMaximumSize(QtCore.QSize(200, 20))
        self.usr_color_label.setObjectName("usr_color_label")
        self.gridLayout_6.addWidget(self.usr_color_label, 1, 0, 1, 1)
        self.usr_color_ledit = QtWidgets.QLineEdit(self.system_work_space_gbox)
        self.usr_color_ledit.setObjectName("usr_color_ledit")
        self.gridLayout_6.addWidget(self.usr_color_ledit, 1, 1, 1, 2)
        self.usr_image_label = QtWidgets.QLabel(self.system_work_space_gbox)
        self.usr_image_label.setMinimumSize(QtCore.QSize(200, 20))
        self.usr_image_label.setMaximumSize(QtCore.QSize(200, 20))
        self.usr_image_label.setObjectName("usr_image_label")
        self.gridLayout_6.addWidget(self.usr_image_label, 2, 0, 1, 1)
        self.usr_image_ledit = QtWidgets.QLineEdit(self.system_work_space_gbox)
        self.usr_image_ledit.setObjectName("usr_image_ledit")
        self.gridLayout_6.addWidget(self.usr_image_ledit, 2, 1, 1, 2)
        self.work_space_inner_space = QtWidgets.QWidget(self.system_work_space_gbox)
        self.work_space_inner_space.setMinimumSize(QtCore.QSize(0, 20))
        self.work_space_inner_space.setMaximumSize(QtCore.QSize(16777215, 20))
        self.work_space_inner_space.setObjectName("work_space_inner_space")
        self.gridLayout_6.addWidget(self.work_space_inner_space, 3, 0, 1, 3)
        self.store_loc_cbox = QtWidgets.QCheckBox(self.system_work_space_gbox)
        self.store_loc_cbox.setMinimumSize(QtCore.QSize(300, 22))
        self.store_loc_cbox.setMaximumSize(QtCore.QSize(300, 22))
        self.store_loc_cbox.setChecked(False)
        self.store_loc_cbox.setObjectName("store_loc_cbox")
        self.gridLayout_6.addWidget(self.store_loc_cbox, 4, 0, 1, 2)
        spacerItem13 = QtWidgets.QSpacerItem(464, 354, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_6.addItem(spacerItem13, 5, 0, 1, 3)
        self.verticalLayout_3.addWidget(self.system_work_space_gbox)
        self.setti_items.addTab(self.setti_system, "")
        self.gridLayout.addWidget(self.setti_items, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(SettingsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Reset)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(SettingsDialog)
        self.setti_items.setCurrentIndex(0)
        self.buttonBox.accepted.connect(SettingsDialog.accept)
        self.buttonBox.rejected.connect(SettingsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SettingsDialog)

    def retranslateUi(self, SettingsDialog):
        _translate = QtCore.QCoreApplication.translate
        self.interface_color_square_gbox.setTitle(_translate("SettingsDialog", "Color Square"))
        self.cubic_ratio_label.setText(_translate("SettingsDialog", "cubic ratio"))
        self.interface_color_wheel_gbox.setTitle(_translate("SettingsDialog", "Color Wheel"))
        self.wheel_ratio_label.setText(_translate("SettingsDialog", "wheel ratio"))
        self.volum_ratio_label.setText(_translate("SettingsDialog", "volum ratio"))
        self.s_tag_radius_label.setText(_translate("SettingsDialog", "s tag radius"))
        self.v_tag_radius_label.setText(_translate("SettingsDialog", "v tag radius"))
        self.wheel_ed_wid_label.setText(_translate("SettingsDialog", "wheel ed wid"))
        self.positive_wid_label.setText(_translate("SettingsDialog", "positive wid"))
        self.negative_wid_label.setText(_translate("SettingsDialog", "negative wid"))
        self.wheel_ed_color_label.setText(_translate("SettingsDialog", "wheel ed color"))
        self.positive_color_label.setText(_translate("SettingsDialog", "positive color"))
        self.negative_color_label.setText(_translate("SettingsDialog", "negative color"))
        self.interface_graph_view_gbox.setTitle(_translate("SettingsDialog", "Graph View"))
        self.circle_dist_label.setText(_translate("SettingsDialog", "circle dist"))
        self.setti_items.setTabText(self.setti_items.indexOf(self.setti_interface), _translate("SettingsDialog", "Interface"))
        self.rule_color_square_gbox.setTitle(_translate("SettingsDialog", "Color Square"))
        self.show_hsv_cbox.setText(_translate("SettingsDialog", "show hsv"))
        self.show_rgb_cbox.setText(_translate("SettingsDialog", "show rgb"))
        self.color_wheel_gbox.setTitle(_translate("SettingsDialog", "Color Wheel"))
        self.h_range_label.setText(_translate("SettingsDialog", "h range"))
        self.h_range_to_label.setText(_translate("SettingsDialog", "to"))
        self.s_range_label.setText(_translate("SettingsDialog", "s_range"))
        self.s_range_to_label.setText(_translate("SettingsDialog", "to"))
        self.v_range_label.setText(_translate("SettingsDialog", "v_range"))
        self.v_range_to_label.setText(_translate("SettingsDialog", "to"))
        self.hm_rule_label.setText(_translate("SettingsDialog", "hm rule"))
        self.overflow_label.setText(_translate("SettingsDialog", "overflow"))
        self.press_move_cbox.setText(_translate("SettingsDialog", "press move"))
        self.rule_graph_view_gbox.setTitle(_translate("SettingsDialog", "Graph View"))
        self.zoom_step_label.setText(_translate("SettingsDialog", "zoom step"))
        self.move_step_label.setText(_translate("SettingsDialog", "move step"))
        self.setti_items.setTabText(self.setti_items.indexOf(self.setti_rule), _translate("SettingsDialog", "Rule"))
        self.system_work_space_gbox.setTitle(_translate("SettingsDialog", "Work Space"))
        self.lang_label.setText(_translate("SettingsDialog", "lang"))
        self.usr_color_label.setText(_translate("SettingsDialog", "usr color"))
        self.usr_image_label.setText(_translate("SettingsDialog", "usr image"))
        self.store_loc_cbox.setText(_translate("SettingsDialog", "store loc"))
        self.setti_items.setTabText(self.setti_items.indexOf(self.setti_system), _translate("SettingsDialog", "System"))
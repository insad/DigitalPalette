# -*- coding: utf-8 -*-

__LICENSE__ = """
DigitalPalette is a free software, which is distributed in the hope 
that it will be useful, but WITHOUT ANY WARRANTY. You can redistribute 
it and/or modify it under the terms of the GNU General Public License 
as published by the Free Software Foundation. See the GNU General Public 
License for more details.
"""

__WEBSITE__ = """
https://liujiacode.github.io/DigitalPalette
"""

__VERSION__ = """
v2.0.3-dev
"""

__AUTHOR__ = """
Liu Jia
"""

__DATE__ = """
2019.11.26
"""

import os
import sys
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import QMainWindow, QApplication, QGridLayout, QMessageBox, QShortcut
from PyQt5.QtCore import QCoreApplication, QUrl, QTranslator
from PyQt5.QtGui import QIcon, QPixmap, QDesktopServices, QKeySequence
from cguis.design.main_window import Ui_MainWindow
from cguis.resource import view_rc
from clibs.args import Args
from wgets.wheel import Wheel
from wgets.graph import Graph
from wgets.cube import CubeTable
from wgets.rule import Rule
from wgets.mode import Mode
from wgets.operation import Operation
from wgets.channel import Channel
from wgets.transformation import Transformation
from wgets.settings import Settings


class DigitalPalette(QMainWindow, Ui_MainWindow):
    """
    DigitalPalette main window framework.
    """

    def __init__(self, resources):
        """
        Init main window.
        """

        super().__init__()
        self.setupUi(self)

        # load args.
        self._args = Args(resources)

        # load translations.
        self._func_tr_()

        # init qt args.
        app_icon = QIcon()
        app_icon.addPixmap(QPixmap(":/images/images/icon_256.png"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(app_icon)
        self.setWindowTitle("DigitalPalette {}".format(self._args.info_version))

        self._setup_workarea()
        self._setup_result()
        self._setup_rule()
        self._setup_mode()
        self._setup_operation()
        self._setup_channel()
        self._setup_transformation()
        self._setup_settings()

        self.tabifyDockWidget(self.transformation_dock_widget, self.mode_dock_widget)
        self.tabifyDockWidget(self.channel_dock_widget, self.rule_dock_widget)

        self.actionImport.triggered.connect(self._wget_operation.import_btn.click)
        self.actionExport.triggered.connect(self._wget_operation.export_btn.click)
        self.actionQuit.triggered.connect(self.close)

        self.actionCreate.triggered.connect(self._wget_operation.create_btn.click)
        self.actionLocate.triggered.connect(self._wget_operation.locate_btn.click)
        self.actionSettings.triggered.connect(self._wget_settings.showup)

        self.actionRule.triggered.connect(self._inner_show_or_hide(self.rule_dock_widget))
        self.actionChannel.triggered.connect(self._inner_show_or_hide(self.channel_dock_widget))
        self.actionOperation.triggered.connect(self._inner_show_or_hide(self.operation_dock_widget))
        self.actionMode.triggered.connect(self._inner_show_or_hide(self.mode_dock_widget))
        self.actionTransformation.triggered.connect(self._inner_show_or_hide(self.transformation_dock_widget))
        self.actionResult.triggered.connect(self._inner_show_or_hide(self.result_dock_widget))

        self.actionHomepage.triggered.connect(lambda x: QDesktopServices.openUrl(QUrl(self._args.info_main_site)))
        self.actionUpdate.triggered.connect(lambda x: QDesktopServices.openUrl(QUrl(self._args.info_update_site)))
        self.actionAbout.triggered.connect(lambda x: self._show_about())

        shortcut = QShortcut(QKeySequence("Alt+I"), self)
        shortcut.activated.connect(self._wget_operation.import_btn.click)
        shortcut = QShortcut(QKeySequence("Ctrl+O"), self)
        shortcut.activated.connect(self._wget_operation.import_btn.click)

        shortcut = QShortcut(QKeySequence("Alt+E"), self)
        shortcut.activated.connect(self._wget_operation.export_btn.click)
        shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        shortcut.activated.connect(self._wget_operation.export_btn.click)

        shortcut = QShortcut(QKeySequence("Alt+Q"), self)
        shortcut.activated.connect(self.close)
        shortcut = QShortcut(QKeySequence("Esc"), self)
        shortcut.activated.connect(self.close)

        shortcut = QShortcut(QKeySequence("Alt+C"), self)
        shortcut.activated.connect(self._wget_operation.create_btn.click)
        shortcut = QShortcut(QKeySequence("Ctrl+W"), self)
        shortcut.activated.connect(self._wget_operation.create_btn.click)

        shortcut = QShortcut(QKeySequence("Alt+L"), self)
        shortcut.activated.connect(self._wget_operation.locate_btn.click)
        shortcut = QShortcut(QKeySequence("Ctrl+G"), self)
        shortcut.activated.connect(self._wget_operation.locate_btn.click)

        shortcut = QShortcut(QKeySequence("Alt+S"), self)
        shortcut.activated.connect(self._wget_settings.showup)
        shortcut = QShortcut(QKeySequence("`"), self)
        shortcut.activated.connect(self._wget_settings.showup)

        # install translator.
        self._tr = QTranslator()
        self._app = QApplication.instance()
        self._install_translator()

        # install stylesheet.
        """
        with open(os.sep.join((resources, "styles", "dark", "style.qss"))) as qf:
            self._app.setStyleSheet(qf.read())
        """

    def _setup_workarea(self):
        """
        Setup workarea (wheel or graph).
        """

        central_widget_grid_layout = QGridLayout(self.central_widget)
        central_widget_grid_layout.setContentsMargins(2, 2, 2, 2)

        self._wget_wheel = Wheel(self._args)
        self._wget_graph = Graph(self._args)
        self._wget_graph.hide()

        central_widget_grid_layout.addWidget(self._wget_wheel)
        central_widget_grid_layout.addWidget(self._wget_graph)

    def _setup_result(self):
        """
        Setup result (cube).
        """

        result_grid_layout = QGridLayout(self.result_dock_contents)
        result_grid_layout.setContentsMargins(2, 2, 2, 2)

        self._wget_cube_table = CubeTable(self._args)
        result_grid_layout.addWidget(self._wget_cube_table)

        self._wget_wheel.ps_color_changed.connect(lambda x: self._wget_cube_table.update_color())
        self._wget_wheel.ps_index_changed.connect(lambda x: self._wget_cube_table.update_index())

        self._wget_graph.ps_color_changed.connect(lambda x: self._wget_cube_table.update_color())

        self._wget_cube_table.ps_color_changed.connect(lambda x: self._wget_wheel.update())
        self._wget_cube_table.ps_color_changed.connect(lambda x: self._wget_graph.update_color_loc())

    def _setup_rule(self):
        """
        Setup rule.
        """

        rule_grid_layout = QGridLayout(self.rule_dock_contents)
        rule_grid_layout.setContentsMargins(2, 2, 2, 2)

        self._wget_rule = Rule(self._args)
        rule_grid_layout.addWidget(self._wget_rule)

        self._wget_rule.ps_rule_changed.connect(lambda x: self._wget_cube_table.modify_rule())

    def _setup_mode(self):
        """
        Setup mode.
        """

        mode_grid_layout = QGridLayout(self.mode_dock_contents)
        mode_grid_layout.setContentsMargins(2, 2, 2, 2)

        self._wget_mode = Mode(self._args)
        mode_grid_layout.addWidget(self._wget_mode)

        self._wget_mode.ps_mode_changed.connect(lambda x: self._wget_cube_table.modify_box_visibility())

    def _setup_operation(self):
        """
        Setup operation.
        """

        operation_grid_layout = QGridLayout(self.operation_dock_contents)
        operation_grid_layout.setContentsMargins(2, 2, 2, 2)

        self._wget_operation = Operation(self._args)
        operation_grid_layout.addWidget(self._wget_operation)

        self._wget_operation.ps_create.connect(lambda x: self._inner_create())
        self._wget_operation.ps_locate.connect(lambda x: self._inner_locate())
        self._wget_operation.ps_update.connect(lambda x: self._wget_cube_table.update_color())
        self._wget_operation.ps_update.connect(lambda x: self._wget_rule.update_rule())

    def _setup_channel(self):
        """
        Setup channel.
        """

        channel_grid_layout = QGridLayout(self.channel_dock_contents)
        channel_grid_layout.setContentsMargins(2, 2, 2, 2)

        self._wget_channel = Channel(self._args)
        channel_grid_layout.addWidget(self._wget_channel)

        self._wget_channel.ps_channel_changed.connect(lambda x: self._wget_graph.open_category())

    def _setup_transformation(self):
        """
        Setup transformation.
        """

        transformation_grid_layout = QGridLayout(self.transformation_dock_contents)
        transformation_grid_layout.setContentsMargins(2, 2, 2, 2)

        self._wget_transformation = Transformation(self._args)
        transformation_grid_layout.addWidget(self._wget_transformation)

        self._wget_transformation.ps_home.connect(lambda x: self._wget_graph.home())
        self._wget_transformation.ps_move.connect(lambda x: self._wget_graph.move(x[0], x[1]))
        self._wget_transformation.ps_zoom.connect(lambda x: self._wget_graph.zoom(x, "default"))

    def _setup_settings(self):
        """
        Setup settings.
        """

        self._wget_settings = Settings(self._args)

        self._wget_settings.ps_rule_changed.connect(lambda x: self._wget_cube_table.modify_rule())
        self._wget_settings.ps_lang_changed.connect(lambda x: self._install_translator())
        self._wget_settings.ps_settings_changed.connect(lambda x: self._inner_update())

    def _inner_create(self):
        """
        For connection in _setup_operation with create sign.
        """

        if self._wget_wheel.isVisible():
            self._wget_cube_table.create_set()

        else:
            self._wget_wheel.show()
            self._wget_graph.hide()

    def _inner_locate(self):
        """
        For connection in _setup_operation with locate sign.
        """

        if self._wget_graph.isVisible():
            self._wget_graph.open_image_dialog()

        else:
            self._wget_wheel.hide()
            self._wget_graph.show()

    def _inner_update(self):
        """
        Update setable wgets.
        """

        self._args.sys_color_set.set_overflow(self._args.overflow)
        self._args.sys_color_set.set_hsv_ranges(self._args.h_range, self._args.s_range, self._args.v_range)
        self._wget_wheel.update()
        self._wget_graph.update_all()
        self._wget_cube_table.update_all()
        self._wget_cube_table.modify_box_visibility()
        self._wget_rule.update_rule()
        self._wget_mode.update_mode()

        self.update()

    def _inner_show_or_hide(self, wget):
        """
        Change hidden wget to shown state and change shown wget to hidden state.
        """

        def _func_(self):
            if wget.isVisible():
                wget.hide()

            else:
                wget.show()

        return _func_

    def _install_translator(self):
        self._app.removeTranslator(self._tr)

        if self._args.lang != "default":
            lang = os.sep.join((self._args.resources, "langs", self._args.lang))
            self._tr.load(lang)
            self._app.installTranslator(self._tr)

        self._wget_channel._func_tr_()
        self._wget_graph._func_tr_()
        self._wget_operation._func_tr_()
        self._wget_rule._func_tr_()
        self._wget_settings.retranslateUi(self._wget_settings)
        self._wget_settings._func_tr_()
        self.retranslateUi(self)
        self._func_tr_()

        self._wget_rule.update_text()
        self._wget_channel.update_text()
        self._wget_graph.update_text()
        self._wget_operation.update_text()
        self._wget_settings.update_text()

        self.update()

    def _show_about(self):
        """
        Show DigitalPalette information.
        """

        info = "DigitalPalette\n"
        info += "---------- ---------- ----------\n"
        info += "{}: {}\n".format(self._info_descs[1], self._args.info_version)
        info += "{}: {}\n".format(self._info_descs[2], self._args.info_author)
        info += "{}: {}\n".format(self._info_descs[3], self._args.info_date)
        info += "{}: {}\n".format(self._info_descs[4], self._args.info_main_site)
        info += "---------- ---------- ----------\n"
        info += self._info_descs[5]

        box = QMessageBox.information(self, self._info_descs[0], info)

    def closeEvent(self, event):
        """
        Actions before close DigitalPalette.
        """

        self._wget_graph.close()
        self._args.save_settings()

        event.accept()

    # ---------- ---------- ---------- Translations ---------- ---------- ---------- #

    def _func_tr_(self):
        _translate = QCoreApplication.translate

        self._info_descs = (
            _translate("DigitalPalette", "About"),
            _translate("DigitalPalette", "Version"),
            _translate("DigitalPalette", "Author"),
            _translate("DigitalPalette", "Update"),
            _translate("DigitalPalette", "Website"),
            _translate("DigitalPalette", "DigitalPalette is a free software, which is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY. You can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation. See the GNU General Public License for more details."),
        )


if __name__ == "__main__":
    appctxt = ApplicationContext()
    DP = DigitalPalette(appctxt.get_resource('.'))
    DP.show()
    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)

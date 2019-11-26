# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QRadioButton, QGridLayout, QScrollArea, QFrame, QSpacerItem, QSizePolicy, QGroupBox
from PyQt5.QtCore import pyqtSignal, QCoreApplication, QSize


class Rule(QWidget):
    """
    Rule object based on QWidget. Init a rule in rule.
    """

    ps_rule_changed = pyqtSignal(bool)

    def __init__(self, args):
        """
        Init rule.
        """

        super().__init__()

        # load args.
        self._args = args

        # load translations.
        self._func_tr_()

        # init qt args.
        rule_grid_layout = QGridLayout(self)
        rule_grid_layout.setContentsMargins(1, 1, 1, 1)

        scroll_area = QScrollArea(self)
        scroll_area.setFrameShape(QFrame.Box)
        scroll_area.setWidgetResizable(True)
        rule_grid_layout.addWidget(scroll_area)

        scroll_contents = QWidget()
        scroll_grid_layout = QGridLayout(scroll_contents)
        scroll_grid_layout.setContentsMargins(1, 1, 1, 1)
        scroll_grid_layout.setHorizontalSpacing(8)
        scroll_grid_layout.setVerticalSpacing(12)
        scroll_area.setWidget(scroll_contents)

        self._rule_gbox = QGroupBox(scroll_contents)
        gbox_grid_layout = QGridLayout(self._rule_gbox)
        gbox_grid_layout.setContentsMargins(8, 8, 8, 8)
        gbox_grid_layout.setHorizontalSpacing(8)
        gbox_grid_layout.setVerticalSpacing(12)
        scroll_grid_layout.addWidget(self._rule_gbox, 0, 1, 1, 1)

        self._rule_btns = []
        for i in range(8):
            btn = QRadioButton(self._rule_gbox)
            gbox_grid_layout.addWidget(btn, i, 0, 1, 1)

            btn.clicked.connect(self.modify_rule(i))
            self._rule_btns.append(btn)

        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        scroll_grid_layout.addItem(spacer, 8, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        scroll_grid_layout.addItem(spacer, 8, 1, 1, 1)

        self._synchronization_gbox = QGroupBox(scroll_contents)
        gbox_grid_layout = QGridLayout(self._synchronization_gbox)
        gbox_grid_layout.setContentsMargins(8, 8, 8, 8)
        gbox_grid_layout.setHorizontalSpacing(8)
        gbox_grid_layout.setVerticalSpacing(12)
        scroll_grid_layout.addWidget(self._synchronization_gbox, 1, 1, 1, 1)

        self._synchronization_btns = []
        for i in range(4):
            btn = QRadioButton(self._synchronization_gbox)
            gbox_grid_layout.addWidget(btn, i, 0, 1, 1)

            btn.clicked.connect(self.modify_synchronization(i))
            self._synchronization_btns.append(btn)

        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        scroll_grid_layout.addItem(spacer, 4, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        scroll_grid_layout.addItem(spacer, 4, 1, 1, 1)

        self.update_rule()
        self._synchronization_btns[self._args.sys_color_set.synchronization].setChecked(True)

        self.update_text()

    # ---------- ---------- ---------- Public Funcs ---------- ---------- ---------- #

    def sizeHint(self):
        return QSize(180, 90)

    def modify_rule(self, idx):
        """
        Modify stored rule set by btn.
        """

        def _func_(value):
            self._args.hm_rule = self._args.global_hm_rules[idx]
            self.ps_rule_changed.emit(True)

        return _func_

    def modify_synchronization(self, idx):
        """
        Modify stored synchronization set by btn.
        """

        def _func_(value):
            self._args.sys_color_set.synchronization = idx
            # synchronization works in mouse moving event in wheel.
            # self.ps_rule_changed.emit(True)

        return _func_

    def update_rule(self):
        """
        Update rule btn by self._args.hm_rule.
        """

        idx = self._args.global_hm_rules.index(self._args.hm_rule)
        self._rule_btns[idx].setChecked(True)

    # ---------- ---------- ---------- Translations ---------- ---------- ---------- #

    def update_text(self):
        self._rule_gbox.setTitle(self._gbox_descs[0])
        self._synchronization_gbox.setTitle(self._gbox_descs[1])

        for i in range(8):
            self._rule_btns[i].setText(self._rule_descs[i])

        for i in range(4):
            self._synchronization_btns[i].setText(self._synchronization_descs[i])

    def _func_tr_(self):
        _translate = QCoreApplication.translate

        self._gbox_descs = (
            _translate("Channel", "Harmony"),
            _translate("Channel", "Synchronization"),
        )

        self._rule_descs = (
            _translate("Rule", "Analogous"),
            _translate("Rule", "Monochromatic"),
            _translate("Rule", "Triad"),
            _translate("Rule", "Tetrad"),
            _translate("Rule", "Pentad"),
            _translate("Rule", "Complementary"),
            _translate("Rule", "Shades"),
            _translate("Rule", "Custom"),
        )

        self._synchronization_descs = (
            _translate("Rule", "Unlimited"),
            _translate("Rule", "H Locked"),
            _translate("Rule", "S Locked"),
            _translate("Rule", "Equidistant"),
        )

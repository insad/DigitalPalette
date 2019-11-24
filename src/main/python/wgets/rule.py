# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QRadioButton, QGridLayout, QScrollArea, QFrame, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSignal, QCoreApplication, QSize


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
        scroll_grid_layout.setContentsMargins(8, 8, 8, 8)
        scroll_grid_layout.setHorizontalSpacing(8)
        scroll_grid_layout.setVerticalSpacing(12)
        scroll_area.setWidget(scroll_contents)

        self._btns = []
        for i in range(8):
            btn = QRadioButton(scroll_contents)
            scroll_grid_layout.addWidget(btn, i, 0, 1, 1)

            btn.clicked.connect(self.modify_rule(i))
            self._btns.append(btn)

        self.update_rule()

        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        scroll_grid_layout.addItem(spacer, 8, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        scroll_grid_layout.addItem(spacer, 8, 1, 1, 1)

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

    def update_rule(self):
        """
        Update rule btn by self._args.hm_rule.
        """

        idx = self._args.global_hm_rules.index(self._args.hm_rule)
        self._btns[idx].setChecked(True)

    # ---------- ---------- ---------- Translations ---------- ---------- ---------- #

    def update_text(self):
        for i in range(8):
            self._btns[i].setText(self._rule_descs[i])

    def _func_tr_(self):
        _translate = QCoreApplication.translate

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

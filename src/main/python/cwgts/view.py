# -*- coding: utf-8 -*-

from cguis.graph_view_form import Ui_graph_view
from PyQt5.QtWidgets import QWidget, QGridLayout
from PyQt5.QtCore import pyqtSignal


class View(QWidget, Ui_graph_view):
    """
    Graph view contain image, graph type and channel boxes.
    """

    selected_gph = pyqtSignal(int)
    selected_chl = pyqtSignal(int)

    selected_move = pyqtSignal(str)
    selected_zoom = pyqtSignal(str)

    def __init__(self):
        """
        Init the graph view area.

        Parameters:
          setting - dict. setting environment.
        """
    
        super().__init__()
        self.setupUi(self)
    
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.gview)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(grid_layout)

        self.cobox_gph.setGeometry(20, 0, 35, 20)
        self.cobox_chl.setGeometry(55, 0, 35, 20)

        self.pbtn_zoom_in.setGeometry(95, 0, 20, 20)
        self.pbtn_move_up.setGeometry(115, 0, 20, 20)
        self.pbtn_zoom_out.setGeometry(135, 0, 20, 20)

        self.pbtn_move_left.setGeometry(95, 20, 20, 20)
        self.pbtn_return_home.setGeometry(115, 20, 20, 20)
        self.pbtn_move_right.setGeometry(135, 20, 20, 20)

        self.pbtn_move_down.setGeometry(115, 40, 20, 20)
        
        
        self.cobox_gph.currentIndexChanged.connect(lambda x: self.selected_gph.emit(self.cobox_gph.currentIndex()))
        self.cobox_chl.currentIndexChanged.connect(lambda x: self.selected_chl.emit(self.cobox_chl.currentIndex()))

        self.pbtn_move_up.clicked.connect(lambda x: self.selected_move.emit("u"))
        self.pbtn_move_down.clicked.connect(lambda x: self.selected_move.emit("d"))
        self.pbtn_move_left.clicked.connect(lambda x: self.selected_move.emit("l"))
        self.pbtn_move_right.clicked.connect(lambda x: self.selected_move.emit("r"))

        self.pbtn_zoom_in.clicked.connect(lambda x: self.selected_zoom.emit("i"))
        self.pbtn_zoom_out.clicked.connect(lambda x: self.selected_zoom.emit("o"))


    # ===== ===== ===== slot functions ===== ===== =====

    def slot_change_gph(self, graph_type):
        if graph_type != self.cobox_gph.currentIndex():
            self.cobox_gph.setCurrentIndex(graph_type)
            self.update()

    def slot_change_chl(self, channel):
        if channel != self.cobox_chl.currentIndex():
            self.cobox_chl.setCurrentIndex(channel)
            self.update()

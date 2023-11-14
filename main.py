import os

from PyQt5.QtGui import QBrush, QColor

from findPathWidget import FindPathWidget
from script import get_dicom_image, censor_personal_information
from slideView import SlideView

# load openslide
# The path can also be read from a config file, etc.
OPENSLIDE_PATH = os.path.join(os.getcwd(), 'openslide-win64/bin')

import os

if hasattr(os, 'add_dll_directory'):
    # Windows
    with os.add_dll_directory(OPENSLIDE_PATH):
        pass
else:
    pass

import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QMainWindow, \
    QWidget, QTableWidget, QTableWidgetItem, QSplitter, QSizePolicy, QHeaderView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__initVal()
        self.__initUi()

    def __initVal(self):
        pass

    def __initUi(self):
        self.setWindowTitle('WSI Viewer')

        findPathWidget = FindPathWidget()
        findPathWidget.added.connect(self.__find)

        self.__sliderViewer = SlideView()

        self.__tableWidget = QTableWidget()
        self.__tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.__tableWidget.setColumnCount(2)
        self.__tableWidget.setHorizontalHeaderLabels(['Key', 'Value'])

        splitter = QSplitter()
        splitter.addWidget(self.__sliderViewer)
        splitter.addWidget(self.__tableWidget)
        splitter.setHandleWidth(1)
        splitter.setChildrenCollapsible(False)
        splitter.setSizes([700, 300])
        splitter.setStyleSheet(
            "QSplitterHandle {background-color: lightgray;}")
        splitter.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

        lay = QVBoxLayout()
        lay.addWidget(findPathWidget)
        lay.addWidget(splitter)

        mainWidget = QWidget()
        mainWidget.setLayout(lay)

        self.setCentralWidget(mainWidget)

    def __find(self, filename):
        self.__slide, level_dimension, region, prop, tiles = get_dicom_image(filename)

        prop = censor_personal_information(prop)

        items = prop.items()

        self.__tableWidget.clear()
        self.__tableWidget.setRowCount(len(items))
        i = 0
        for k, v in items:
            k_item = QTableWidgetItem(k)
            self.__tableWidget.setItem(i, 0, k_item)
            v_item = QTableWidgetItem(v)
            if v == 'CENSORED':
                v_item.setForeground(QBrush(QColor(255, 0, 0)))
            self.__tableWidget.setItem(i, 1, v_item)
            i += 1

        self.__sliderViewer.setSlide(self.__slide, level_dimension, region)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

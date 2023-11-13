from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene

class SlideView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.__initVal()
        self.__initUi()

    def __initVal(self):
        # Define the level of the slide you want to work with
        self.__level = 2  # For example, level 2 is a lower resolution than level 0

    def __initUi(self):
        self.__scene = QGraphicsScene(self)

    def setSlide(self, slide, level_dimension, region):
        # Convert the region to a format that QGraphicsView can use
        # The '1' argument is the alpha channel which is usually not used in OpenSlide
        image = QImage(region.tobytes(), *level_dimension, QImage.Format_ARGB32)

        # Add the QImage to the QGraphicsScene
        pixmap = QPixmap.fromImage(image)
        self.__scene.addPixmap(pixmap)

        # deep zoom sample tutorial
        dims = slide.level_dimensions
        print('no of levels =', len(dims))
        # by how much the levels are downsampled
        print(dims, slide.level_downsamples)  # this image contain only one level

        # Set the scene to the QGraphicsView
        self.setScene(self.__scene)

# pyqt-wsi-viewer
PyQt WSI(Whole Slide Images) viewer

This shows slide image of DICOM file (in normal size currently) which captured by scanner.

Also this shows any metadata which DICOM file had with using QTableWidget, but it censored(de-identification) the personal information of patient. 

## Requirements
* PyQt5>=5.14
* openslide-python

## Preview
![image](https://github.com/yjg30737/pyqt-wsi-viewer/assets/55078043/ad9d6031-e291-424a-b137-f300da0155ab)

## TODO
* Zoom In, Zoom out, Moving from one to another in the picture with mouse

## See Also
* <a href="https://github.com/yjg30737/pyqt-dicom-viewer.git">pyqt-dicom-viewer</a>
* <a href="https://github.com/openslide/openslide-python">openslide-python</a>

# pyqt-wsi-viewer
<img width="946" height="809" alt="PyQt WSI Image Viewer2" src="https://github.com/user-attachments/assets/ceb03840-6a16-43f9-ba5e-6863f6f43e38" />

## Description
A simple DCM viewer with annotation capabilities using PyQt6 and pyvips/openslide

## Requirements
* pillow
  * Required to use pyvips or openslide
* pyvips
  * Needed for processing large images
* PyQt6
  * For GUI
* PyQt6-WebEngine
  * Needed to use webview in PyQt6 

## File Description
* main.py: Entry point of the application
* html_templates.py: This will generate temp_viewer.html, which shows WSI file.
* konva.min.js: Being used to draw annotation on WSI images (primitive)
* openseadragon: Open-source JavaScript library for displaying high-resolution, zoomable images on the web

## DCM file to test
You can get DCM file here: 
https://www.kaggle.com/code/marcaubreville/first-steps-with-the-mitos-wsi-ccmct-data-set/data

## How to run
```bash
1. python -m venv venv
2. pip install -r requirements.txt
3. python main.py
4. Load DCM file
```

## Preview
https://github.com/user-attachments/assets/96e6fb73-f6be-463a-86f5-1395b804faf6


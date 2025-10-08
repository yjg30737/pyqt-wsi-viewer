"""
Configuration constants for WSI Image Viewer
"""

# Application constants
APP_TITLE = "PyQt WSI Image Viewer"
APP_VERSION = "1.0.0"
APP_AUTHOR = "WSI Viewer Team"

# Window settings
DEFAULT_WINDOW_WIDTH = 1200
DEFAULT_WINDOW_HEIGHT = 800
MIN_WINDOW_WIDTH = 800
MIN_WINDOW_HEIGHT = 600

# Viewer settings
VIEWER_WIDTH = 1280
VIEWER_HEIGHT = 768

# File types
SUPPORTED_DCM_EXTENSIONS = ['.dcm']
SUPPORTED_DZI_EXTENSIONS = ['.dzi']
SUPPORTED_EXTENSIONS = SUPPORTED_DCM_EXTENSIONS + SUPPORTED_DZI_EXTENSIONS

# File dialog filters
FILE_DIALOG_FILTER = "DCM Files (*.dcm);;DZI Files (*.dzi);;All Files (*)"

# Progress dialog messages
PROGRESS_ANALYZING = "Analyzing DICOM file..."
PROGRESS_CONVERTING = "Converting to DZI format..."
PROGRESS_COMPLETE = "Conversion complete!"
PROGRESS_DIALOG_TITLE = "Converting"
PROGRESS_DIALOG_CANCEL = "Cancel"
PROGRESS_DIALOG_CONVERTING = "Converting file..."

# Error messages
ERROR_CONVERSION_FAILED = "Failed to convert DICOM file."
ERROR_FILE_NOT_SUPPORTED = "File Not Supported"
ERROR_LOADING_TITLE = "Error"
ERROR_CONVERTING_TITLE = "Converting error"

# Temporary files
TEMP_HTML_FILENAME = "temp_viewer.html"

# Drawing settings
DEFAULT_STROKE_COLOR = "#ff0000"
DEFAULT_STROKE_WIDTH = 3
DRAWING_OPACITY = 0.8
ERASER_WIDTH = 10

# Drawing mode constants
DRAW_MODE_NONE = "none"
DRAW_MODE_DRAW = "draw"
DRAW_MODE_ERASE = "erase"
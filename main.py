from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QApplication, QFileDialog, QProgressDialog, QMessageBox
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, QThread, pyqtSignal
import sys
import os
from pathlib import Path
from utils import convert_wsi_to_dzi, get_dzi_path_for_dcm, dzi_exists_for_dcm
from html_templates import generate_openseadragon_html, generate_error_html
from config import *


class DCMConverterWorker(QThread):
    """Worker thread for DCM to DZI conversion"""
    finished = pyqtSignal(str)  # Signal emitted when conversion is complete
    error = pyqtSignal(str)     # Signal emitted when an error occurs
    progress = pyqtSignal(str)  # Signal emitted to update progress text
    
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        
    def run(self):
        """Run the conversion in a separate thread"""
        try:
            self.progress.emit(PROGRESS_ANALYZING)

            # Convert DCM to DZI
            self.progress.emit(PROGRESS_CONVERTING)
            dzi_file = convert_wsi_to_dzi(self.file_path)

            if dzi_file is None:
                self.error.emit(ERROR_CONVERSION_FAILED)
                return

            self.progress.emit(PROGRESS_COMPLETE)
            self.finished.emit(dzi_file)

        except Exception as e:
            self.error.emit(f"An error occurred during conversion: {str(e)}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = APP_TITLE
        self.setWindowTitle(self.title)
        self.resize(DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT)
        self.setMinimumSize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)

        # Set up the central widget and layout
        self.central_widget = QWidget()
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        # Add a button to load the tutorial
        self.load_button = QPushButton("Open DCM File")
        self.load_button.clicked.connect(self.load_tutorial)
        self.layout.addWidget(self.load_button)

        # Add a QWebEngineView to display the HTML
        self.web_view = QWebEngineView()
        self.layout.addWidget(self.web_view)
        
        # Initialize worker thread and progress dialog
        self.worker = None
        self.progress_dialog = None

    def load_dzi_file(self, dzi_file):
        """Load a DZI file into the web view"""
        try:
            # Generate HTML content with the DZI file
            html_content = generate_openseadragon_html(dzi_file)
            
            # Create a temporary HTML file and load it
            temp_html_path = os.path.join(os.getcwd(), TEMP_HTML_FILENAME)
            with open(temp_html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # Load the HTML file in the web view
            file_url = QUrl.fromLocalFile(os.path.abspath(temp_html_path))
            self.web_view.load(file_url)
            
            print(f"Loaded file in web view: {dzi_file}")
            return True
            
        except Exception as e:
            QMessageBox.critical(self, ERROR_LOADING_TITLE, f"Error loading DZI file: {str(e)}")
            print(f"Error loading DZI file: {e}")
            return False

    def on_conversion_finished(self, dzi_file):
        """Called when DCM conversion is completed"""
        if self.progress_dialog:
            self.progress_dialog.close()
            self.progress_dialog = None
            
        # Load the converted DZI file
        self.load_dzi_file(dzi_file)
            
        # Clean up worker thread
        if self.worker:
            self.worker.deleteLater()
            self.worker = None
    
    def on_conversion_error(self, error_msg):
        """Called when DCM conversion encounters an error"""
        if self.progress_dialog:
            self.progress_dialog.close()
            self.progress_dialog = None
            
        QMessageBox.critical(self, ERROR_CONVERTING_TITLE, error_msg)
        
        # Clean up worker thread
        if self.worker:
            self.worker.deleteLater()
            self.worker = None
    
    def on_conversion_progress(self, progress_text):
        """Called to update progress dialog text"""
        if self.progress_dialog:
            self.progress_dialog.setLabelText(progress_text)

    def start_dcm_conversion(self, file_path):
        """Start DCM to DZI conversion in a separate thread"""
        # Create and show progress dialog
        self.progress_dialog = QProgressDialog(PROGRESS_DIALOG_CONVERTING, PROGRESS_DIALOG_CANCEL, 0, 0, self)
        self.progress_dialog.setWindowTitle(PROGRESS_DIALOG_TITLE)
        self.progress_dialog.setModal(True)
        self.progress_dialog.show()
        
        # Create and configure worker thread
        self.worker = DCMConverterWorker(file_path)
        self.worker.finished.connect(self.on_conversion_finished)
        self.worker.error.connect(self.on_conversion_error)
        self.worker.progress.connect(self.on_conversion_progress)
        
        # Handle progress dialog cancellation
        self.progress_dialog.canceled.connect(self.cancel_conversion)
        
        # Start the conversion
        self.worker.start()
    
    def cancel_conversion(self):
        """Cancel the ongoing conversion"""
        if self.worker and self.worker.isRunning():
            self.worker.terminate()
            self.worker.wait()
            self.worker.deleteLater()
            self.worker = None
            
        if self.progress_dialog:
            self.progress_dialog.close()
            self.progress_dialog = None

    def load_tutorial(self):
        # Open DCM or DZI file
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Open File", 
            "", 
            FILE_DIALOG_FILTER
        )
        
        if file_path:
            try:
                file_ext = Path(file_path).suffix.lower()
                
                if file_ext == '.dzi':
                    # DZI file - can be used directly
                    dzi_file = Path(file_path).name
                    print(f"Loading DZI file: {dzi_file}")
                    self.load_dzi_file(dzi_file)
                    
                elif file_ext == '.dcm':
                    # DCM file - check if DZI already exists first
                    print(f"Processing DCM file: {file_path}")
                    
                    if dzi_exists_for_dcm(file_path):
                        # DZI file already exists, use it directly
                        dzi_file = get_dzi_path_for_dcm(file_path)
                        print(f"Found existing DZI file: {dzi_file}")
                        self.load_dzi_file(dzi_file)
                    else:
                        # DZI file doesn't exist, needs conversion in a separate thread
                        print(f"No existing DZI found, starting conversion for: {file_path}")
                        self.start_dcm_conversion(file_path)
                    
                else:
                    QMessageBox.warning(self, ERROR_FILE_NOT_SUPPORTED, f"File type not supported: {file_ext}")
                    return
                
            except Exception as e:
                QMessageBox.critical(self, ERROR_LOADING_TITLE, f"Error processing file: {str(e)}")
                print(f"Error loading file: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

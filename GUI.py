import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QFont, QPalette, QColor
from PyQt5.QtCore import Qt
from QRGenerationv2 import QR_Generation, create_qr_image
from image import create_qr_image2, create_qr_image3

# Define colors for the app
COLORS = {
    "blue": "#0099ff",
    "green": "#00ff6a",
    "red": "#ff1900",
    "yellow": "#f39c12",
    "light": "#ffffff",
    "dark": "#000000",
    "navy": "#203d5a",
    "white": "#ffffff"
}

# Main App
class QRApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # Init stuff
        self.shape = "square" 
        self.dark_mode = False
        self.qr_color = (0, 0, 0)
        # UI setup
        self.setupUI()
        
    def setupUI(self):
        # Window config
        self.setWindowTitle("QR Code Generator")
        self.setMinimumSize(800, 600)
        self.resize(800, 600)
        # Main widget and layout
        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.main_layout = QVBoxLayout(self.central)
        # Create UI sections
        self.makeHeader()
        self.makeContent()
        self.makeStatusBar()
        # Set theme
        self.applyTheme()
    
    def makeHeader(self):
        header = QWidget()
        header_layout = QHBoxLayout(header)
        # Title
        title = QLabel("QR Code Generator")
        title.setFont(QFont("Garuda", 14, QFont.Bold))
        # Dark mode button
        self.dark_btn = QPushButton("Toggle Dark Mode")
        self.dark_btn.clicked.connect(self.toggleDarkMode)
        # Add to layout
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.dark_btn)
        # Add to main layout
        self.main_layout.addWidget(header)
    
    def makeContent(self):
        content = QWidget()
        content_layout = QHBoxLayout(content)
        # Make left and right panels
        self.makeControlPanel(content_layout)
        self.makeDisplayArea(content_layout)
        # Add to main layout
        self.main_layout.addWidget(content, 1)
    
    def makeControlPanel(self, parent_layout):
        panel = QWidget()
        panel_layout = QVBoxLayout(panel)
        # Buttons panel
        buttons = [
            ("Change QR Colour", self.pickColor),
            ("QR Creation Slideshow", self.showSlides),
            ("Generate QR Code", self.makeQR),
            ("Clear Text", self.clearText),
            ("Change QR Shape", self.pickShape),
            ("Help", self.showHelp)
        ]
        for text, action in buttons:
            btn = QPushButton(text)
            btn.setMinimumWidth(200)
            btn.clicked.connect(action)
            panel_layout.addWidget(btn)
        # Warning button 
        warn_btn = QPushButton("⚠️ QR Code Safety Warning")
        warn_btn.setMinimumWidth(200)
        warn_btn.setStyleSheet(f"background-color: {COLORS['red']}; color: white; font-weight: bold;")
        warn_btn.clicked.connect(self.showWarning)
        panel_layout.addWidget(warn_btn)
        # Push buttons to top
        panel_layout.addStretch()
        # Add to parent
        parent_layout.addWidget(panel)
    
    def makeDisplayArea(self, parent_layout):
        display = QWidget()
        display_layout = QVBoxLayout(display)
        # QR preview area
        self.qr_box = QGroupBox("QR Code Preview")
        qr_layout = QVBoxLayout(self.qr_box)
        self.qr_image = QLabel("QR code will appear here")
        self.qr_image.setAlignment(Qt.AlignCenter)
        self.qr_image.setMinimumHeight(200)
        qr_layout.addWidget(self.qr_image)
        # Text input area
        self.text_box = QGroupBox("Enter Text for QR Code")
        text_layout = QVBoxLayout(self.text_box)
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Enter text for your QR code here...")
        self.text_input.setFont(QFont("Garuda", 11))
        text_layout.addWidget(self.text_input)
        # Add to display layout
        display_layout.addWidget(self.qr_box)
        display_layout.addWidget(self.text_box, 1)
        # Add to parent layout
        parent_layout.addWidget(display, 1)
    
    def makeStatusBar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_label = QLabel("Ready")
        self.status_bar.addWidget(self.status_label)
    
    def makeQR(self):
        # Get text
        text = self.text_input.toPlainText().strip()
        if not text:
            self.status_label.setText("Enter some text first")
            return
        # Generate QR code
        self.status_label.setText("Generating QR code...")
        # Make QR code 
        qr = QR_Generation(text)
        matrix = qr.generate_final_bit_stream()
        # Pick shape function
        if self.shape == "square":
            img = create_qr_image(matrix, color=self.qr_color)
        elif self.shape == "circle":
            img = create_qr_image2(matrix, color=self.qr_color)
        else:  # diamond or any other shape defaults to diamond
            img = create_qr_image3(matrix, color=self.qr_color)
        # Save final image 
        current_dir = os.getcwd()
        img_path = os.path.join(current_dir, "generated_qr.png")
        img.save(img_path)
        # Show image
        pixmap = QPixmap(img_path)
        pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.qr_image.setPixmap(pixmap)
        self.status_label.setText("QR code generated")
    
    def clearText(self):
        self.text_input.clear()
        self.text_input.setPlaceholderText("Enter text for your QR code here...")
    
    def pickColor(self):
        dialog = ColorPicker(self)
        if dialog.exec_():
            name, rgb = dialog.picked_color
            self.qr_color = rgb
            self.status_label.setText(f"Color: {name}")
    
    def pickShape(self):
        dialog = ShapePicker(self, self.shape)
        if dialog.exec_():
            self.shape = dialog.picked_shape
            self.status_label.setText(f"Shape: {self.shape}")
    
    def showSlides(self):
        # Show slideshow
        slideshow = SlideViewer(self)
        slideshow.exec_()
    
    def showHelp(self):
        # Show help dialog
        HelpWindow(self).exec_()
    
    def showWarning(self):
        # Show warning dialog
        WarningWindow(self).exec_()
    
    def toggleDarkMode(self):
        # Toggle dark mode
        self.dark_mode = not self.dark_mode
        self.applyTheme()
    
    def applyTheme(self):
        app = QApplication.instance()
        palette = QPalette()
        # Set colors based on dark mode
        if self.dark_mode:
            # Dark mode
            bg = QColor(COLORS["navy"])
            text = QColor(COLORS["white"])
            palette.setColor(QPalette.Window, bg)
            palette.setColor(QPalette.WindowText, text)
            palette.setColor(QPalette.Base, QColor("#3c3c3c"))
            palette.setColor(QPalette.AlternateBase, bg)
            palette.setColor(QPalette.ToolTipBase, bg)
            palette.setColor(QPalette.ToolTipText, text)
            palette.setColor(QPalette.Text, text)
            palette.setColor(QPalette.Button, bg)
            palette.setColor(QPalette.ButtonText, QColor(COLORS["dark"]))
            palette.setColor(QPalette.Link, QColor(COLORS["blue"]))
            palette.setColor(QPalette.Highlight, QColor(COLORS["blue"]))
            palette.setColor(QPalette.HighlightedText, text)
        else:
            # Light mode
            bg = QColor(COLORS["light"])
            text = QColor(COLORS["dark"])
            palette.setColor(QPalette.Window, bg)
            palette.setColor(QPalette.WindowText, text)
            palette.setColor(QPalette.Base, QColor("white"))
            palette.setColor(QPalette.AlternateBase, bg)
            palette.setColor(QPalette.ToolTipBase, bg)
            palette.setColor(QPalette.ToolTipText, text)
            palette.setColor(QPalette.Text, text)
            palette.setColor(QPalette.Button, bg)
            palette.setColor(QPalette.ButtonText, text)
            palette.setColor(QPalette.Link, QColor(COLORS["blue"]))
            palette.setColor(QPalette.Highlight, QColor(COLORS["blue"]))
            palette.setColor(QPalette.HighlightedText, QColor("white"))
        app.setPalette(palette)
    
    def updateStatus(self, message, status_type="info"):
        # Direct text setting
        self.status_label.setText(message)

class WarningWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUI()
    def setupUI(self):
        self.setWindowTitle("⚠️ QR Code Safety Warning")
        self.setMinimumSize(700, 600)
        # Main layout
        layout = QVBoxLayout(self)
        # Header
        header_layout = QHBoxLayout()
        warning_icon = QLabel("⚠️")
        warning_icon.setFont(QFont("Garuda", 24))
        warning_icon.setStyleSheet(f"color: {COLORS['yellow']};")
        title = QLabel("QR Code Safety: Beware of Scams")
        title.setFont(QFont("Garuda", 16, QFont.Bold))
        title.setStyleSheet(f"color: {COLORS['yellow']};")
        title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(warning_icon)
        header_layout.addWidget(title, 1)
        header_layout.addWidget(QLabel("⚠️"))
        layout.addLayout(header_layout)
        # Divider
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)
        # Warning content
        warning_layout = QVBoxLayout()
        # Warning sections
        sections = [
            ("Understanding QR Code Risks", [
                "QR codes can link you to malicious websites, download malware, or initiate fraudulent payments.",
                "They can appear legitimate but can lead to phishing sites designed to steal your personal information.",
            ]),
            ("Common QR Code Scams", [
                "Phishing Attacks: Fake QR codes that lead to fake websites.",
                "Payment Fraud: QR codes that allow payments to scammers.",
                "Malware Distribution: QR codes that automatically download malicious software to your device.",
            ]),
            ("How to Stay Safe", [
                "Verify the Source: Only scan QR codes from trusted sources.",
                "Check URLs: Before proceeding to a website, verify the URL.",
                "Be Wary of Public QR Codes: Be extra cautious of QR codes in public places.",
            ])
        ]
        # Add sections directly to layout
        for title, items in sections:
            section_title = QLabel(title)
            section_title.setFont(QFont("Garuda", 14, QFont.Bold))
            warning_layout.addWidget(section_title)
            for item in items:
                item_label = QLabel(item)
                item_label.setWordWrap(True)
                item_label.setTextFormat(Qt.RichText)
                warning_layout.addWidget(item_label)
            warning_layout.addSpacing(15)
        # Final warning
        final_warning = QLabel("Remember when in doubt, don't scan!")
        final_warning.setWordWrap(True)
        final_warning.setStyleSheet("font-weight: bold; color: #e74c3c;")
        warning_layout.addWidget(final_warning)
        layout.addLayout(warning_layout)
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

class ColorPicker(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.picked_color = ("Black", (0, 0, 0))
        self.setupUI()
    def setupUI(self):
        self.setWindowTitle("Choose QR Code Colour")
        self.setMinimumSize(400, 250)
        # Main layout
        layout = QVBoxLayout(self)
        # Title
        title = QLabel("Select a colour for your QR code")
        title.setFont(QFont("Garuda", 12, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        # Grid for colour options
        grid = QWidget()
        grid_layout = QGridLayout(grid)
        # Colour options 
        colors = {
            "Black": (0, 0, 0), 
            "Red": (255, 0, 0), 
            "Green": (0, 255, 0),
            "Blue": (0, 0, 255), 
            "Purple": (128, 0, 128), 
            "Orange": (255, 165, 0),
            "Yellow": (255, 255, 0), 
            "Cyan": (0, 255, 255)
        }
        # Add colors to grid
        row, col = 0, 0
        for name, rgb in colors.items():
            # Colour sample
            swatch = QFrame()
            swatch.setFrameShape(QFrame.Box)
            swatch.setMinimumSize(40, 40)
            swatch.setStyleSheet(f"background-color: rgb({rgb[0]}, {rgb[1]}, {rgb[2]}); border: 1px solid black;")
            # Label
            label = QLabel(name)
            label.setAlignment(Qt.AlignCenter)
            # Container
            container = QWidget()
            container_layout = QVBoxLayout(container)
            container_layout.addWidget(swatch, alignment=Qt.AlignCenter)
            container_layout.addWidget(label)
            # Add to grid
            grid_layout.addWidget(container, row, col)
            # Make clickable
            swatch.mousePressEvent = lambda e, n=name, c=rgb: self.selectColor(n, c)
            # Update position
            col += 1
            if col == 4:
                col = 0
                row += 1
        layout.addWidget(grid)
    
    def selectColor(self, name, rgb):
        # Direct assignment and acceptance
        self.picked_color = (name, rgb)
        self.accept()

class ShapePicker(QDialog):
    def __init__(self, parent=None, current_shape="square"):
        super().__init__(parent)
        self.picked_shape = current_shape
        self.setupUI()
    
    def setupUI(self):
        self.setWindowTitle("Choose QR Code Shape")
        self.setMinimumSize(300, 200)
        # Main layout
        layout = QVBoxLayout(self)
        # Title
        title = QLabel("Select a shape for your QR code")
        title.setFont(QFont("Garuda", 12, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        # Shape options
        shapes = ["square", "circle", "diamond"]
        # Radio buttons
        self.radio_group = QButtonGroup(self)
        for i, shape in enumerate(shapes):
            radio = QRadioButton(shape.capitalize())
            if shape == self.picked_shape:
                radio.setChecked(True)
            self.radio_group.addButton(radio, i)
            layout.addWidget(radio)
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.onAccept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def onAccept(self):
        # Direct shape selection
        selected_id = self.radio_group.checkedId()
        shapes = ["square", "circle", "diamond"]
        if 0 <= selected_id < len(shapes):
            self.picked_shape = shapes[selected_id]
        self.accept()

class SlideViewer(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current = 0
        self.slides = []
        # Get QR images from current directory
        self.loadSlides()
        self.setupUI()
        self.showCurrentSlide()
    
    def loadSlides(self):
        # Define the expected QR creation process images
        expected_images = [
            "qr_withfinderpatterns.png",
            "qr_with_seperators.png",
            "qr_with_timing_patterns.png",
            "qr_with_reserve_info.png",
            "qr_with_data_bits_v1.png",
            "generated_qr.png"
        ]
        # Use images directly from script directory 
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.slides = []
        # Add existing process images
        for img in expected_images:
            img_path = os.path.join(script_dir, img)
            if os.path.exists(img_path):
                self.slides.append(img_path)
        # Add the generated QR code at the end 
        current_dir = os.getcwd()
        generated_qr = os.path.join(current_dir, "generated_qr.png")
        if os.path.exists(generated_qr):
            # Check if we already have this file
            if generated_qr not in self.slides:
                self.slides.append(generated_qr)
        
    def setupUI(self):
        self.setWindowTitle("QR Code Creation Slideshow")
        self.setMinimumSize(500, 400)
        # Main layout
        layout = QVBoxLayout(self)
        # Title
        title = QLabel("QR Code Creation Process")
        title.setFont(QFont("Garuda", 12, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        # Image display
        self.image = QLabel()
        self.image.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image)
        # Description
        self.description = QLabel()
        self.description.setAlignment(Qt.AlignCenter)
        self.description.setWordWrap(True)
        layout.addWidget(self.description)
        # Navigation
        nav_layout = QHBoxLayout()
        self.prev_btn = QPushButton("Previous")
        self.prev_btn.clicked.connect(self.prevSlide)
        self.next_btn = QPushButton("Next")
        self.next_btn.clicked.connect(self.nextSlide)
        nav_layout.addWidget(self.prev_btn)
        nav_layout.addWidget(self.next_btn)
        layout.addLayout(nav_layout)
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        # Install event filter for key handling
        self.installEventFilter(self)
    
    # Event filter for key presses
    def eventFilter(self, obj, event):
        if event.type() == event.KeyPress:
            if event.key() == Qt.Key_Left:
                self.prevSlide()
                return True
            elif event.key() == Qt.Key_Right:
                self.nextSlide()
                return True
        return super().eventFilter(obj, event)
    
    # Show the current slide
    def showCurrentSlide(self):
        # Get current file
        current_file = self.slides[self.current]
        # Show image
        pixmap = QPixmap(current_file)
        pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image.setPixmap(pixmap)
        # Get filename for description
        filename = os.path.basename(current_file)
        # Set description based on filename
        if "finder" in filename.lower():
            desc = "Finder Patterns - The three square patterns in the corners help the scanner locate the QR code."
        elif "seperator" in filename.lower():
            desc = "Separators - White space around finder patterns to improve detection."
        elif "timing" in filename.lower():
            desc = "Timing Patterns - Alternating black and white modules that help determine cell size."
        elif "reserve" in filename.lower():
            desc = "Reserved Areas - Space reserved for format and version information."
        elif "data" in filename.lower():
            desc = "Data Bits - The actual encoded data is placed in the remaining area."
        elif "generated_qr" in filename.lower():
            desc = "Final QR Code - The complete QR code with all elements combined."
        self.description.setText(f"Step {self.current + 1}: {desc}")
        # Update buttons
        self.prev_btn.setEnabled(self.current > 0)
        self.next_btn.setEnabled(self.current < len(self.slides) - 1)
    
    # Navigation methods
    def prevSlide(self):
        if self.current > 0:
            self.current -= 1
            self.showCurrentSlide()

    # Next slide method
    def nextSlide(self):
        if self.current < len(self.slides) - 1:
            self.current += 1
            self.showCurrentSlide()

class HelpWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUI()
    
    # Setup the help dialog UI
    def setupUI(self):
        self.setWindowTitle("QR Code Generator Help")
        self.setMinimumSize(500, 400)
        # Main layout
        layout = QVBoxLayout(self)
        # Title
        title = QLabel("QR Code Generator Help")
        title.setFont(QFont("Garuda", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        # Help content 
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        help_widget = QWidget()
        help_layout = QVBoxLayout(help_widget)
        # Help sections
        sections = [
            ("Getting Started", [
                "1. Enter text in the input area on the right side",
                "2. Click 'Generate QR Code' to create your QR code",
                "3. The generated QR code will appear in the preview area"
            ]),
            ("Customising Your QR Code", [
                "• Click 'Change QR Colour' to select a different colour",
                "• Click 'Change QR Shape' to choose between square, circle, or diamond shapes",
                "• Dark mode can be toggled using the button in the top-right corner"
            ]),
            ("Viewing the Creation Process", [
                "• After generating a QR code, click 'QR Creation Slideshow'",
                "• Navigate through the slides using the Previous/Next buttons or arrow keys",
                "• Each slide shows a different stage of the QR code creation process"
            ])
        ]
        # Add sections to layout
        for title, items in sections:
            section_title = QLabel(title)
            section_title.setFont(QFont("Garuda", 12, QFont.Bold))
            help_layout.addWidget(section_title)
            for item in items:
                item_label = QLabel(item)
                item_label.setWordWrap(True)
                help_layout.addWidget(item_label)
            help_layout.addSpacing(10)
        scroll.setWidget(help_widget)
        layout.addWidget(scroll)
        # Close button 
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QRApp()
    window.show()
    sys.exit(app.exec_())

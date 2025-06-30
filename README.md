Key capabilities include:

Dynamically selects QR Code version 1 or 2 depending on the length of the input string.
Implements all the key features of creating a QR code; data encoding, Reed Solomon error correction, finder patterns, timing patterns,
Seperators, format information etc
Applies all masking patterns and evaulates the penalty scores of each and selects the one with the lowest penalty score
Has additional features such as visual customization : you can change the colour of black QR modules, and change the shape of the QR
code which is between square, circle and diamond shapes
You can also switch between light and dark mode for the graphical user interface.
Furthermore has educational slideshow, A built-in feature to visually demonstrate the step-by-step process of QR code creation,
fostering digital literacy and understanding of QR code architecture.


Instructions to run program:

Prerequisites:

Ensure you have python v3 installed
and also various external Python libraries such as Pillow, reedsolo , PyQt and numpy.
to install python, go to the official Python website: https://www.python.org/downloads/windows/ and download the latest one for your
respective operating system
to install external python libaries , go to terminal and type in "pip install (library)"


Program installation and execution:

you can enter "git clone [URL of the github repo]" in the command line
you now have the relevant python modules up and running
navigate into the cloned directory cd [project directory name]

run GUI.py with the command [python GUI.py]

This will launch the QR Code Generator application window.
you'll be presented several options:
-Input Text: Type or paste your desired text/URL into the large text area.
-Get QR Code: Click this button to generate and display the QR code. It will also be saved to your Downloads folder.
-Clear All: Clears the input text area.
-Change Colour: Opens a pop-up window to select the color of the dark modules in the QR code.
-Change QR Shape: Opens a pop-up window to choose between Square, Circle, or Diamond QR code shapes.
-Toggle Dark Mode: Switches the application's theme between light and dark modes.
-QR Creation Slideshow: Opens a new window demonstrating the step-by-step construction of a QR code.
QR Code Safety Warning: can displays how QR codes can potentially be dangerous and link to unsafe websites and that users
should be catious

Note: For the "QR Creation Slideshow" feature to function correctly, you may need to ensure that the intermediate QR image files
(e.g., qr_withfinderpatterns.png, qr_with_timing_patterns.png, etc.) are present in the exact directory specified in the GUI.py file.
If you encounter errors, please check or update these paths in the GUI.py script.



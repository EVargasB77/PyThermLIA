Title: PyThermLIA

Description:

This Python Library code implements a Lock-In Amplified with the Method_Fourier class for analyzing video frames using the Fourier transform. 
It calculates the phase and amplitude of the signal based on a user-defined modulation frequency and frame rate. 
The code also includes a Video class that handles video capture, frame processing, and exporting results to MATLAB files.

Features:

    Calculates phase and amplitude of video frames using Fourier transform
    Configurable modulation frequency and frame rate
    Processes video frames on a frame-by-frame basis
    Exports phase and amplitude data to MATLAB files (.mat)

Installation:

    Prerequisites: Ensure you have Python 3.x installed along with the following libraries:
        OpenCV (pip install opencv-python)
        NumPy (pip install numpy)
        SciPy (pip install scipy)
        Matplotlib (optional, for visualization)

    Clone or download the repository.

    Install dependencies: Navigate to the project directory and run pip install -r requirements.txt (if a requirements.txt file exists).

Usage:

  the easist way to use is follow the example described in __main__ section 
    

Exporting Results:

  When you use the Export2Mat()  function then script automatically exports the calculated phase and amplitude data to MATLAB files named Phase.mat and Amplitude.mat, respectively.

Contributing:

  We welcome contributions to improve this project. Feel free to fork the repository, make changes, and create pull requests.

License:

  this library its based under GLP Licence

Additional Notes:

    You can modify the script further by adding visualization functionalities using Matplotlib or other libraries.
    Consider error handling for video loading or file operations.
    Include an example notebook or script demonstrating usage if applicable.

Example: 


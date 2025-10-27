# file: fourier_lockin.py

import numpy as np
import cmath
from scipy.io import savemat

class FourierLockIn:
    """
    Performs a Lock-In analysis on a sequence of frames using a Discrete Fourier Transform.
    
    This class is responsible only for the numerical algorithm. It receives frames
    (as NumPy arrays) and calculates the phase and amplitude at a specified
    modulation frequency.
    """
    def __init__(self, modulation_freq: float, frame_rate: float, total_frames: int, frame_shape: tuple):
        """
        Initializes the Lock-In processor.
        
        Args:
            modulation_freq (float): The modulation frequency of the signal (fe).
            frame_rate (float): The frame rate of the source signal (fs).
            total_frames (int): The total number of frames to be processed (N).
            frame_shape (tuple): The (height, width) of the frames.
        """
        if not all([modulation_freq > 0, frame_rate > 0, total_frames > 0]):
            raise ValueError("Frequency, frame rate, and total frames must be positive.")
            
        self.modulation_freq = modulation_freq
        self.frame_rate = frame_rate
        self.total_frames = total_frames
        
        # This is the direct translation of: k = round((N*fe)/fs)+1 from MATLAB
        self.digital_frequency = int(round((self.total_frames * self.modulation_freq) / self.frame_rate) + 1)
        
        self._frame_shape = frame_shape
        self._accumulator = np.zeros(self._frame_shape, dtype=np.complex64)
        self.frames_processed = 0

    def process_frame(self, frame: np.ndarray):
        """
        Processes a single frame, accumulating the Fourier transform result.
        
        Args:
            frame (np.ndarray): A 2D NumPy array (grayscale) normalized to [0, 1].
        """
        if self.frames_processed >= self.total_frames:
            print("Warning: Attempting to process more frames than the specified total.")
            return

        # DFT formula: Y = Y + frame * exp(-1j * 2 * pi * (k-1) * n / N)
        n = self.frames_processed
        k = self.digital_frequency
        N = self.total_frames
        
        twiddle_factor = cmath.exp(-1j * 2 * cmath.pi * (k - 1) * n / N)
        
        self._accumulator += frame * twiddle_factor
        self.frames_processed += 1

    def get_amplitude(self) -> np.ndarray:
        """
        Calculates the final amplitude map after all frames are processed.
        The result is scaled by (2/N) to match the signal's true amplitude.
        """
        if self.frames_processed == 0:
            return np.zeros(self._frame_shape)
        return (2 / self.frames_processed) * np.abs(self._accumulator)

    def get_phase(self) -> np.ndarray:
        """
        Calculates the final phase map after all frames are processed.
        """
        return np.angle(self._accumulator)

    def reset(self):
        """Resets the accumulator and frame count for a new analysis."""
        self.frames_processed = 0
        self._accumulator = np.zeros(self._frame_shape, dtype=np.complex64)
        
    @staticmethod
    def export_to_mat(amplitude: np.ndarray, phase: np.ndarray, amp_filename="Amplitude.mat", phase_filename="Phase.mat"):
        """Exports the resulting maps to .mat files."""
        savemat(amp_filename, {'Amplitude': amplitude})
        savemat(phase_filename, {'Phase': phase})


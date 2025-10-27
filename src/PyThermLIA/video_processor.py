# file: video_processor.py

import cv2
import numpy as np

class VideoProcessor:
    """
    Handles video file operations such as reading frames and metadata.
    
    This class acts as a wrapper around OpenCV's VideoCapture to provide
    a clean and reusable interface for accessing video frames.
    """
    def __init__(self, filepath: str):
        """
        Initializes the video processor by opening the video file.
        
        Args:
            filepath (str): The path to the video file.
        """
        self.filepath = filepath
        self._cap = cv2.VideoCapture(self.filepath)
        
        if not self._cap.isOpened():
            raise IOError(f"Could not open video file: {self.filepath}")
            
        self.width = int(self._cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.frame_rate = self._cap.get(cv2.CAP_PROP_FPS)
        self.total_frames = int(self._cap.get(cv2.CAP_PROP_FRAME_COUNT))

    def frames_generator(self, start_frame: int = 0, end_frame: int = None, normalize: bool = True):
        """
        A generator that yields frames from the video as NumPy arrays.
        
        Args:
            start_frame (int): The frame number to start from.
            end_frame (int): The frame number to end at (inclusive). Defaults to the last frame.
            normalize (bool): If True, converts frames to grayscale and normalizes to [0, 1].
            
        Yields:
            np.ndarray: The processed video frame.
        """
        if end_frame is None:
            end_frame = self.total_frames - 1
            
        if not (0 <= start_frame < self.total_frames and start_frame <= end_frame):
            raise ValueError("Invalid start or end frame index.")

        self._cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        
        current_frame = start_frame
        while self._cap.isOpened() and current_frame <= end_frame:
            ret, frame = self._cap.read()
            if not ret:
                break
            
            if normalize:
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                yield gray_frame.astype(np.float32) / 255.0
            else:
                yield frame
                
            current_frame += 1

    def release(self):
        """Releases the video capture object."""
        self._cap.release()
        
    def __del__(self):
        """Ensures the video file is released when the object is destroyed."""
        self.release()


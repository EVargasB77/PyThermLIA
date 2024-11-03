__version__ = '1.0'

from cv2.typing import MatLike
import cv2
import numpy as np
import cmath, math
from scipy.io import savemat

class Event:
    def __init__(self):
        self._observers = []

    def register(self, observer):
        self._observers.append(observer)

    def unregister(self, observer):
        self._observers.remove(observer)

    def notify(self, *args, **kwargs):
        for observer in self._observers:
            observer(*args, **kwargs)

class Method_Fourier(object):
    _status_event       = Event()
    _status             : str       = 'Program Initializing ......'
    _fe                 : float     = 0.1               # Represents the modulation frequency for Lock In Process (fe)
    _fps                : int       = 24                # Represents the frame rate of source video               (fs)
    _frames_by_period   : int       = _fps / _fe
    _ratio_frequency    : float     = 1 / _frames_by_period
    _number_of_frames   : int       = 300               # Represents the total frames to process by lock-in
    _number_of_periods  : int       = _number_of_frames / _frames_by_period
    _digital_Frequency  : int       = (_number_of_periods * _ratio_frequency) + 1
    _count              : int       = 0                 # Represents the number of frames processed

    _frame          : MatLike = np.zeros((128, 320, 3), dtype=np.uint8)
    _temporal_frame : MatLike = np.zeros((128, 320, 3), dtype=np.uint8)

    _w_factor = lambda _ , n: cmath.exp(-1j*2*cmath.pi / n) if n > 0 else 0+0j

    @property
    def Phase(self):
        real = self._temporal_frame.real
        imag = self._temporal_frame.imag
        return np.arctan2(imag, real)

    @property
    def Amplitude(self):
        real = self._temporal_frame.real
        imag = self._temporal_frame.imag
        return np.sqrt(real**2 + imag**2)

    @property
    def Frame(self) -> MatLike:
        return self._frame

    @property
    def Modulation(self):
        return self._fe

    @property
    def Frame_Rate(self):
        return self._fps

    @property
    def FrameByPeriod(self):
        return self._frames_by_period

    @property
    def Total_Frames(self):
        return self._number_of_frames

    @property
    def Periods(self):
        return self._number_of_periods

    @property
    def Digital_Frequency(self)->int:
        return self._digital_Frequency

    @property
    def Frames_Processed(self)->int:
        # Gets the total number of frames processed so far
        return self._count

    @Modulation.setter
    def Modulation(self, frequency:float = 0.1):
        if frequency != 0 :
            self._fe = frequency
            self._frames_by_period  = self.Frame_Rate / frequency
            self._ratio_frequency = 1 / self._frames_by_period if frequency != 0 else 0 
            self._status = f'The modulation frequency for lock-in process has been applied...' 
        else:
            self._status = f'The modulation frequency for lock-in process can not be zero...'
        
        self._status_event.notify(self._status)

    @Frame_Rate.setter
    def Frame_Rate(self , fps:int = 24):
        if fps != 0 :
            self._fps = fps
            self._frames_by_period = fps / self.Modulation
            self._ratio_frequency = 1 / self._frames_by_period if self._frames_by_period != 0 else 0 
            self._status = f'The frame rate value has been applied...'
        else:
            self._status = f'The frame rate of source video can not be zero...'

        self._status_event.notify(self._status)

    @Total_Frames.setter
    def Total_Frames(self, frames: int = 100):
        self._number_of_frames = frames
        self._number_of_periods = int(frames / self.FrameByPeriod) if self.FrameByPeriod != 0 else 0 
        self._digital_Frequency = math.ceil((self._number_of_periods * self._ratio_frequency) + 1)
        self._status = f'The number of frames has been applied...'
        self._status_event.notify(self._status)

    @Frame.setter
    def Frame(self, frame : MatLike):
        if frame is not None:
            if len(frame.shape) == 3:  # the image is (RGB)
                self._frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255.0
            else:  
                self._frame = frame.astype(np.float32) / 255.0
        else:
            self._status = f'The frame can no be null...'
        self.Process()

    def Process(self):
        if self._count == 0:
            self._temporal_frame = self._frame * self._w_factor(self.Periods)
        else:
            self._temporal_frame = self._temporal_frame + (self._frame * self._w_factor(self.Periods))
    
        self._count += 1

    def Export2Mat(self):
        savemat('Phase.mat', {'Phase': self.Phase})
        savemat('Amplitude.mat', {'Amplitude': self.Amplitude})


    def __init__(self, frequency :float = 0.1, fps: int =30, total_frames: int = 0):
        """
        Class constructor.

        Args:
            frequency (float, optional): Frequency. Defaults to 0.1.
            fps (int, optional): Frames per second. Defaults to 30.
            total_frames (int, optional): total frames to be process. Defaults to 0.
        """
        self.Modulation  = frequency
        self.Frame_Rate  = fps
        self.Total_Frames = total_frames

    def __str__(self):
        return str(self._w_factor(self.Periods))

class Video(object):
    
    _cap                : cv2.VideoCapture
    _current_frame      : int       = 0
    _final_frame        : int       = 100
    _initial_frame      : int       = 1
    _path               : str       = ''
    _file               : str       = ''

    Fourier = Method_Fourier(0.3,24,7000)

    @property
    def Frame_Rate(self):
        return self._cap.get(cv2.CAP_PROP_FPS)

    @property
    def Total_Frames(self):
        return int(self._cap.get(cv2.CAP_PROP_FRAME_COUNT))

    @property
    def Current_Frame(self):
        return int(self._cap.get(cv2.CAP_PROP_POS_FRAMES))
    
    @Current_Frame.setter
    def Current_Frame(self, frame:int = 1):
        # Set the video to the initial frame
        self._cap.set(cv2.CAP_PROP_POS_FRAMES, frame)

    @property
    def Final_Frame(self):
        return self._final_frame
    
    @Final_Frame.setter
    def Final_Frame(self, frame:int = 100):
        self._final_frame = min(frame, self.Total_Frames - 1)
        self.Fourier.Total_Frames = self._final_frame - self._initial_frame

    @property
    def Initial_Frame(self):
        return self._initial_frame

    @Initial_Frame.setter
    def Initial_Frame(self, frame:int = 0):
        self._initial_frame = frame if frame > 0 else 1
        self.Current_Frame = self._initial_frame
        self.Fourier.Total_Frames = self.Final_Frame - self._initial_frame

    @property
    def Path(self):
        return self._path

    @Path.setter
    def Path(self, p :str = __file__):
        self._path = p

    @property
    def File(self):
        return self._file

    @File.setter
    def File(self, file):
        self._file = os.path.join(self.Path, file)
        # Capture the video
        self._cap = cv2.VideoCapture(self._file)
        self.Fourier.Frame_Rate = self.Frame_Rate
        self.Fourier.Total_Frames = self.Total_Frames

    def process(self):
        """
        Processes a video frame by frame using the Fourier_Method class, extracting FPS.

        Args:
            video_path (str): Path to the video file.
            initial_frame (int, optional): Index of the first frame to process. If None, the user will be prompted.
            final_frame (int, optional): Index of the last frame to process. If None, the user will be prompted.
        """
        # Iterate over frames
        while self._cap.isOpened() and self.Current_Frame <= self.Final_Frame:
            ret, frame = self._cap.read()
            if not ret:
                break

            # Process the frame with the Fourier_Method class
            self.Fourier.Frame = frame
            print(f'\r Frame Processed: {self.Current_Frame}  ', end='')


        # Release the video capture object
        self._cap.release()
        cv2.destroyAllWindows()

    def __init__(self):
        self.Path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.Path = os.path.join(self.Path, 'videos')

    def __str__(self):
        #print(f'\r Current Frame: {self.Current_Frame}', end='')
        return f'Frames to process: {self.Final_Frame} '
         
if __name__ == '__main__':
    import os
    # f = Method_Fourier(0.3,24,7000)
    v = Video()
    v.File = 'AISI304.avi'
    v.Final_Frame = 8000
    v.Initial_Frame = 3000
    v.Fourier.Modulation = 0.3
    v.process()
    v.Fourier.Export2Mat()

    # f.process_video('AISI304.avi',500)
    # print(f.Amplitude)


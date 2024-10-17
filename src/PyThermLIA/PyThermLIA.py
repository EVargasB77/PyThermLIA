__version__ = '1.0'

from cv2.typing import MatLike
import cv2
import numpy as np
import cmath

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

class Fourier_Method(object):
    
    _status_event       = Event()
    _status             : str       = 'Program Initializing ......'
    _fe                 : float     = 0.1               # Represents the modulation frequency for Lock In Process (fe)
    _fe_period          : float     = 1 / _fe           # Represents the fe period
    _fs                 : int       = 24                # Represents the frame rate of source video               (fs)
    _fs_period          : float     = 1 / _fs           # Represents the fs period
    _ratio_frequency    : float     = _fe / _fs
    _frames_by_period   : int       = _fs / _fe
    _number_of_frames   : int       = 300
    _number_of_periods  : int       = _number_of_frames / _frames_by_period
    _digital_Frequency  : int       = (_number_of_periods * _ratio_frequency) + 1
    _count              : int       = 0 


    _w_factor           : complex 
    _frame          : MatLike = np.zeros((128, 320, 3), dtype=np.uint8)
    _temporal_frame : MatLike = np.zeros((128, 320, 3), dtype=np.uint8)
    
    @property
    def Frame_Processed(self)->int:
        return self._count

    @property
    def Frame(self)->MatLike:
        return self._frame
    
    @Frame.setter
    def Frame(self, frame:MatLike):
        if frame is not None:
            # Convertir a escala de grises si es necesario y normalizar
            if len(frame.shape) == 3:  # Imagen a color (RGB)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                self._frame = gray.astype(np.float32) / 255.0
            else:  # Imagen ya en escala de grises
                self._frame = frame.astype(np.float32) / 255.0

            if self._count == 0:
                self._temporal_frame = self._frame * self.W_Factor
            else:
                # Aplicar la operación con W_Factor
                self._temporal_frame = self._temporal_frame + (self._frame * self.W_Factor)
            
            self._count =+ 1
        else:
            self._status = f'The frame can no be null...'

    @property
    def W_Factor(self)->complex:
        return cmath.exp(-1j*2*cmath.pi / self._number_of_periods)
    
    @property
    def Frame_Rate(self):
        return self._fs
    
    @Frame_Rate.setter
    def Frame_rate(self, fs:int):
        if fs != 0 :
            self._fs = fs
            self._ratio_frequency   = self._fe / fs
            self._status = f'The frame rate value has been applied...'
        else:
            self._status = f'The frame rate of source video can not be zero...'
        self._frames_by_period  = fs / self._fe
        self._status_event.notify(self._status)

    @property
    def Modulation(self):
        return self._fe

    @Modulation.setter
    def Modulation(self, fe:float):
        if fe != 0 :
            self._fe = fe
            self._frames_by_period  = self._fs / fe
            self._status = f'The modulation frequency for lock-in process has been applied...' 
        else:
            self._status = f'The modulation frequency for lock-in process can not be zero...'
        self._ratio_frequency   = fe / self._fs
        self._status_event.notify(self._status)

    # gets the number of total frames that will be processed by lock in
    @property
    def TotalFrames(self):
        return self._number_of_frames

    @TotalFrames.setter
    def TotalFrames(self, frames: int):
        self._number_of_frames = frames
        self._number_of_periods = int(frames / self._frames_by_period)
        self._status = f'The number of frames has been applied...'
        self._status_event.notify(self._status)

    @property
    def Periods(self)->int:
        return self._number_of_periods

    @property
    def Digital_Frequency(self)->int:
        return self._digital_Frequency

    @property
    def Phase(self)->MatLike:
        return self._count

    def convert2img(self)->MatLike:
        return img
        
if __name__ == '__main__':
    f = Fourier_Method()
    print (f'ratio: {f.W_Factor}')

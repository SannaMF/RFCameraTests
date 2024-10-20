import time
import numpy as np
from threading import Thread, Lock
import numbers


class Frame:
    """
    Frame represents a single data frame from the camera.
    It contains:
    - 2d matrix pixel data
    - unique frame number. This can be used to determine whether there are missing frames between two concecutive frames.
    - timestamp in seconds.
    """

    def __init__(self, data: np.array, frame_number: int, timestamp: float):
        """Initializes frame with given numpy 2d data, frame number and timestamp (in seconds)"""
        self.__data = data
        self.__frame_number = frame_number
        self.__timestamp = timestamp

    def data(self) -> np.array:
        """Returns the numpy data array of the frame"""
        return self.__data

    def frame_number(self) -> int:
        """Returns the frame number of the frame"""
        return self.__frame_number

    def timestamp(self) -> float:
        """Returns the timestamp in seconds of the frame"""
        return self.__timestamp


class RingBuffer:
    """
    RingBuffer represents a circular Frame storage.
    Frames are written always to the next index (goes back to first after the last index).
    Frames are read with separate index, always returning the next frame from the previous one.
    """

    def __init__(self, size: int):
        """Initializes ringbuffer to a given size"""
        self.__size = size
        self.__frames = []
        for i in range(0, size):
            self.__frames.append(None)
        self.__lock = Lock()
        self.__write_index = 0
        self.__read_index = 0
        self.__write_count = 0
        self.__read_count = 0

    def push(self, frame: Frame):
        """Writes new Frame to ringbuffer.
        Frame is written to the next available write index.
        This function will overwrite any existing frame in that index."""
        self.__lock.acquire()
        self.__frames[self.__write_index] = frame
        self.__write_index = (self.__write_index + 1) % self.__size
        self.__write_count += 1
        self.__lock.release()

    def pop(self) -> Frame:
        """Reads the next frame from the buffer.
        Read index is rotating through the ringbuffer one step at a time."""
        self.__lock.acquire()
        if self.__read_count > self.__write_count or self.__read_index == self.__write_index:
            self.__lock.release()
            return None

        frame = self.__frames[self.__read_index]
        self.__read_index = (self.__read_index + 1) % self.__size
        self.__read_count += 1
        self.__lock.release()

        return frame

    def sync(self):
        """Sync Frame writer and reader indices.
        This can be used to forcefully start reading the latest frames."""
        self.__lock.acquire()
        self.__read_index = self.__write_index
        self.__read_count = 0
        self.__write_count = 0
        self.__lock.release()


class CameraDataThread(Thread):
    """
    CameraDataThread is a thread that simulates generation of camera frame data.
    It automatically populates its ringbuffer with new incoming frames.
    """

    def __init__(self, buffer: RingBuffer):
        """Initializes camera data simulator with given ringbuffer."""
        super().__init__()
        self.__buffer = buffer
        self.__frame_time_sec = 1.0
        self.__exposure_time = 1.0
        self.__width = 640
        self.__height = 512
        self.__frame_number = 1
        self.__rng = np.random.default_rng(int(time.time()) % 65535)
        self.__is_started = False

    def run(self):
        """Thread's run function that generated new Frames and writes them to the ringbuffer."""
        prev_time = 0
        while self.__is_started:
            t1 = time.time()
            if (t1 - prev_time) > self.__frame_time_sec:
                frame = self.__generateFrame()
                self.__buffer.push(frame)
                prev_time = t1
            else:
                time.sleep(0.0001)

    def __generateFrame(self) -> Frame:
        """Generates new simulated frame."""
        fill_value = 100 * self.__exposure_time
        data = np.full((self.__height, self.__width), fill_value, dtype=np.uint16)
        self.__frame_number = self.__generageFrameNumber()
        timestamp = time.time()
        frame = Frame(data, self.__frame_number, timestamp)
        return frame

    def __generageFrameNumber(self) -> int:
        """Generates new frame number. Also randomly makes missing frames."""
        rand_value = self.__rng.integers(0, 65535)
        frame_count = 1
        if rand_value < 650:
            frame_count += self.__rng.integers(0, 5)
        frame_number = self.__frame_number + frame_count
        return frame_number

    def start(self):
        """Starts the simulator thread."""
        self.stop()
        self.__is_started = True
        super().start()

    def stop(self):
        """Stops the simulator thread."""
        if self.__is_started == False:
            return

        self.__is_started = False
        self.join()

    def setFrameRate(self, framerate: float):
        """Sets the interval in which frames are simulated."""
        self.__frame_time_sec = 1.0 / framerate

    def setExposureTime(self, exposuretime: float):
        """Sets the exposure which simulates exposure time of a camera by increasing / decreasing the signal levels."""
        self.__exposure_time = exposuretime

    def setWidth(self, width: int):
        """Sets the width of the simulated frame."""
        self.__width = width

    def setHeight(self, height: int):
        """Sets the height of the simulated frame."""
        self.__height = height


class Camera:
    """
    Camera class represents a camera device that has the following features:
    - framerate: Frame rate (in Hz) of the camera's output.
    - exposuretime: Exposure time (in ms) defines the signal levels of the cameras pixel data. eg. 2ms has twice signal level to 1ms.
    - width: Width (in pixels) is the width of the camera's pixel matrix
    - height: Height (in pixels) is the height of the camera's pixel matrix
    - start: Starts the frame acquisition of the camera. Use 'get_frame' to retrieve frames.
    - stop: Stop the frame acquisition of the camera.
    - isstarted: Returns True if frame acquisition is currently running.
    """

    def __init__(self):
        """Initializes camera instance."""
        self.__features = {'framerate': 10, 'exposuretime': 1, 'width': 640, 'height': 512, 'start': None, 'stop': None,
                           'isstarted': False}
        self.__buffer = RingBuffer(100)
        self.__thread = None

    #    
    # Public API
    #

    def features(self) -> dict:
        """Returns the available features names."""
        return list(self.__features.keys())

    def set(self, feature_name: str, value=None) -> bool:
        """Sets a feature and returns 'True' when successful."""
        if feature_name == 'framerate':
            return self.__setFrameRate(value)
        elif feature_name == 'exposuretime':
            return self.__setExposureTime(value)
        elif feature_name == 'width':
            return self.__setWidth(value)
        elif feature_name == 'height':
            return self.__setHeight(value)
        elif feature_name == 'start':
            return self.__start()
        elif feature_name == 'stop':
            return self.__stop()
        else:
            return False

    def get(self, feature_name: str):
        """Gets the value of a feature."""
        if feature_name == 'framerate':
            return self.__getFrameRate()
        elif feature_name == 'exposuretime':
            return self.__getExposureTime()
        elif feature_name == 'width':
            return self.__getWidth()
        elif feature_name == 'height':
            return self.__getHeight()
        elif feature_name == 'isstarted':
            return self.__isStarted()
        else:
            return None

    def get_frame(self, timeout: float = 5.0, sync: bool = False) -> Frame:
        """Gets the next available frame from the camera.
        Returns 'None' if no frames available yet.
        timeout is given in seconds and this is the max amount of time the function will wait for incoming frames.
        Settings sync to True will force the synchronization of the ringbuffer."""
        t1 = time.time()
        time_spent = 0
        frame = None

        if sync == True:
            self.__buffer.sync()

        while frame is None and time_spent < timeout:
            frame = self.__buffer.pop()
            if frame is None:
                time.sleep(0.001)
            else:
                return frame

            t2 = time.time()
            time_spent = (t2 - t1)

    #
    # Private API
    #

    def __setFrameRate(self, framerate: float) -> bool:
        """Sets framerate of the camera. Returns true on success."""
        if isinstance(framerate, numbers.Number) == False or framerate < 1.0 or framerate > 50.0:
            return False

        framerate = float(framerate)
        self.__features['framerate'] = framerate
        self.__features['exposuretime'] = self.__adjustExposureTime(framerate)
        self.__createThread()
        self.__thread.setFrameRate(self.__features['framerate'])
        self.__thread.setExposureTime(self.__features['exposuretime'])

        return True

    def __getFrameRate(self) -> float:
        """Gets the framerate of the camera."""
        return self.__features['framerate']

    def __setExposureTime(self, exposuretime: float) -> bool:
        """Sets exposure time of the camera. Returns true on success."""
        if isinstance(exposuretime, numbers.Number) == False or exposuretime < 0.1 or exposuretime > 30.0:
            return False

        exposuretime = float(exposuretime)
        self.__features['exposuretime'] = exposuretime
        self.__createThread()
        self.__thread.setExposureTime(exposuretime)
        return True

    def __getExposureTime(self) -> float:
        """Gets the exposure time of the camera."""
        return self.__features['exposuretime']

    def __adjustExposureTime(self, framerate: float) -> float:
        """Adjust the exposure time to be within the frame time."""
        frame_time = 1000.0 / framerate
        exposure_time = self.__features['exposuretime']

        exposure_time = min(exposure_time, frame_time)

        return exposure_time

    def __setWidth(self, width: int) -> bool:
        """Sets the width of the camera incoming frames. Returns true on success."""
        if isinstance(width, numbers.Number) == False or width < 100 or width > 1000:
            return False

        width = int(width)
        self.__features['width'] = width
        self.__thread.setWidth(width)
        return True

    def __getWidth(self) -> int:
        """Gets the width of the camera's incoming frames."""
        return self.__features['width']

    def __setHeight(self, height: int) -> bool:
        """Sets the height of the camera incoming frames. Returns true on success."""
        if isinstance(height, numbers.Number) == False or height < 100 or height > 1000:
            return False

        height = int(height)
        self.__features['height'] = height
        self.__thread.setHeight(height)
        return True

    def __getHeight(self) -> int:
        """Gets the height of the camera's incoming frames."""
        return self.__features['height']

    def __createThread(self):
        """Creates a new instance of CameraDataThread thread if needed."""
        if self.__thread is None:
            self.__thread = CameraDataThread(self.__buffer)

    def __start(self):
        """Starts the acquisition of frames."""
        try:
            self.__features['isstarted'] = True
            self.__createThread()
            self.__thread.setFrameRate(self.get('framerate'))
            self.__thread.setExposureTime(self.get('exposuretime'))
            self.__thread.setWidth(self.get('width'))
            self.__thread.setHeight(self.get('height'))
            self.__buffer.sync()
            self.__thread.start()
            return True
        except:
            return False

    def __stop(self):
        """Stops the acquisition of frames."""
        try:
            self.__features['isstarted'] = False
            self.__thread.stop()
            self.__thread = None
            return True
        except:
            return False

    def __isStarted(self) -> bool:
        """Returns True if acquisition of frames is active."""
        return self.__features['isstarted']

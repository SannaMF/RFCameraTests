from camera import Camera


class CameraLibrary:

    def __init__(self):
        self.camera = None

    def create_camera(self):
        self.camera = Camera()
        return self.camera

    def camera_start(self):
        return self.camera.set('start')

    def camera_stop(self):
        return self.camera.set('stop')

    def is_camera_started(self):
        return self.camera.get('isstarted')

    def get_camera_frame(self, timeout=5.0):
        return self.camera.get_frame(timeout)

    def get_camera_framerate(self):
        return self.camera.get('framerate')

    def get_camera_exposuretime(self):
        return self.camera.get('exposuretime')

    def get_camera_width(self):
        return self.camera.get('width')

    def get_camera_height(self):
        return self.camera.get('height')

    def set_camera_framerate(self, value):
        return self.camera.set('framerate', value)

    def set_camera_exposuretime(self, value):
        return self.camera.set('exposuretime', value)

    def set_camera_width(self, value):
        return self.camera.set('width', value)

    def set_camera_height(self, value):
        return self.camera.set('height', value)

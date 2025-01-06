import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget

# import numpy as np  # isort:skip
from camera import Camera, CameraPosition
from objects import Mandelbrot, RandomImage
from renderer import Renderer

if __name__ == "__main__":
    app = QApplication(sys.argv)

    cam = Camera(
        cam_pos=CameraPosition(xmin=-2, xmax=2, ymin=-2, ymax=2, resolution=(100, 100))
    )

    random_obj = RandomImage(camera=cam)

    obj = Mandelbrot(max_iter=20, camera=cam)

    a = Renderer(obj_to_display=random_obj, upscale=8)
    a.show()

    sys.exit(app.exec())

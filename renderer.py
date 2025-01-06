import sys
import time

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

from objects import DisplayObject

__all__ = ["Renderer"]


class Renderer(QWidget):
    def __init__(
        self, obj_to_display: DisplayObject, upscale: int = 1, render_queue=None
    ):
        super().__init__()
        print("init renderer")
        # self.render_queue = render_queue
        self.obj_to_display = obj_to_display
        self.upscale = upscale

        self.setWindowTitle("Renderer")
        self.image_label = QLabel(self)
        self.image_label.setScaledContents(True)
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        self.setLayout(layout)

        resolution = self.obj_to_display.cam.resolution
        self.resize(resolution[0] * self.upscale, resolution[1] * self.upscale)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_image)
        self.timer.start(int(1000 / 60))  # 60 fps

        self._last_frame = time.time()
        self._last_fps_check = time.time()
        self._n_frames_fps_check = 10
        self._frame = 0

    def update_image(self):
        """Update the displayed image if a new one is available."""
        # if not self.render_queue.empty():
        # image = self.render_queue.get()
        self._frame += 1

        since_last_frame = time.time() - self._last_frame  # noqa:F841
        print(f"update ({since_last_frame=:.2f}s)")

        self._last_frame = time.time()

        since_last_fps_check = time.time() - self._last_fps_check
        if self._frame % self._n_frames_fps_check == 0 or since_last_fps_check > 0.5:
            self.window().setWindowTitle(
                f"{self.obj_to_display.object_name} "
                f"({self._n_frames_fps_check/since_last_fps_check:.2f}fps)"
            )
            self._last_fps_check = time.time()

        image = self.obj_to_display.generate_image()
        height, width, _ = image.shape
        qimage = QImage(image.data, width, height, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        self.image_label.setPixmap(pixmap)

    def cleanup(self):
        self.timer.stop()
        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.cleanup()

    # def closeEvent(self, event):
    #     super().closeEvent(event)

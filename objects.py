from abc import ABC, abstractmethod

import numpy as np

from camera import Camera

__all__ = ["DisplayObject"]


class DisplayObject(ABC):
    object_name: str = "DisplayObject"

    def __init__(self, /, camera: Camera | None = None):
        print("init Complex")
        if camera is None:
            camera = Camera()
        self.cam = camera

    @abstractmethod
    def generate_image(self) -> np.ndarray:
        """Generate an image based on the camera"""
        ...


class RandomImage(DisplayObject):
    object_name: str = "RandomImage"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def generate_image(self) -> np.ndarray:
        resolution = self.cam.resolution
        image = np.random.randint(0, 256, [*resolution, 3], dtype=np.uint8)

        return image.astype(np.uint8)


class Mandelbrot(DisplayObject):
    object_name: str = "Mandelbrot"

    def __init__(self, /, max_iter: int = 100, **kwargs):
        super().__init__(**kwargs)
        self.max_iter = max_iter

    def _compute_xy(self, x, y):
        val = 0
        iteration = 0
        while abs(val) < 2 and iteration < self.max_iter:
            val = val * val + x
            iteration += 1

        return iteration

    def generate_image(self):
        resolution = self.cam.resolution

        image = np.zeros((*resolution, 3), dtype=np.uint8)

        for i, j, x, y in self.cam.get_sample():
            divergence = self._compute_xy(x, y)

            divergence = 255 - int((divergence / self.max_iter) * 255)

            # image[i, j] = [
            #     max(divergence - 255 * 2, 0),
            #     max(divergence - 255, 255) - 255,
            #     max(divergence, 255 * 2) - 255 * 2,
            # ]

            # image[i, j] = [divergence % 256, divergence % 128, divergence % 64]

            image[i, j] = [divergence, divergence, divergence]
        return image

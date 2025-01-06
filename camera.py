import numpy as np
from pydantic import BaseModel, field_validator, model_validator

__all__ = ["Camera", "CameraPosition"]


class CameraPosition(BaseModel, validate_assignment=True):
    xmin: float
    xmax: float
    ymin: float
    ymax: float
    resolution: tuple[int, int]

    @field_validator("resolution")
    def validate_resolution(cls, value):
        if value[0] <= 0 or value[1] <= 0:
            raise ValueError("Resolution must be strictly positive")
        return value

    @model_validator(mode="after")
    def correct_bbox(self):
        if self.xmin > self.xmax:
            self.xmin, self.xmax = self.xmax, self.xmin
        if self.ymin > self.ymax:
            self.ymin, self.ymax = self.ymax, self.ymin
        return self


class Camera:
    def __init__(
        self,
        cam_pos: CameraPosition = CameraPosition(
            xmin=-1, xmax=1, ymin=-1, ymax=1, resolution=(800, 600)
        ),
    ):
        self.cam_pos = cam_pos

    @property
    def bbox(self) -> tuple[float, float, float, float]:
        return (
            self.cam_pos.xmin,
            self.cam_pos.xmax,
            self.cam_pos.ymin,
            self.cam_pos.ymax,
        )

    @property
    def resolution(self) -> tuple[int, int]:
        return self.cam_pos.resolution

    def get_sample(self) -> tuple[np.ndarray, np.ndarray]:
        """
        Returns the sample points, based on the camera's bbox and resolution

        yields a list of tuples (i,j,x,y)
        where i,j are integer coordinates in the resulting array
              x,y are the corresponding coordinates in the camera's bbox

        """
        shape = self.cam_pos.resolution
        y = np.linspace(self.cam_pos.xmin, self.cam_pos.xmax, shape[0])
        x = np.linspace(self.cam_pos.ymin, self.cam_pos.ymax, shape[1])
        grid_x, grid_y = np.meshgrid(x, y)
        for i in range(shape[0]):
            for j in range(shape[1]):
                yield i, j, grid_x[i, j], grid_y[i, j]

    def print_bbox(self):
        """
                Slight difference depending on whether len(str(width)) is odd or even.
                Also, the x and y axes's intersection is not at (0,0).

                Examples:

                  ∧       <-------800------->
        +3.00e+00╶┤      ┌───────────────────┐ ∧
                  │      │                   │ ╎
                  │      │                   │ ╎
                  │      │                   │ 600
                  │      │                   │ ╎
                  │      │                   │ ╎
        -3.00e+00╶┤      └───────────────────┘ v
                  │
                  ╎
                   ╶╶╶───┬───────────────────┬─────>
                     +8.50e+00           +1.25e+01


                  ∧       <------1920------>
        +1.22e-01╶┤      ┌──────────────────┐ ∧
                  │      │                  │ ╎
                  │      │                  │ ╎
                  │      │                  │ 1080
                  │      │                  │ ╎
                  │      │                  │ ╎
        -2.70e-01╶┤      └──────────────────┘ v
                  │
                  ╎
                   ╶╶╶───┬──────────────────┬─────>
                     +1.71e-03          +3.25e-02
        """
        cam_pos = self.cam_pos
        xmin = f"{cam_pos.xmin:+.2e}"  # 9 chars long
        xmax = f"{cam_pos.xmax:+.2e}"  # -1.00e+00
        ymin = f"{cam_pos.ymin:+.2e}"  # 123456789
        ymax = f"{cam_pos.ymax:+.2e}"
        # print(xmin, xmax, ymin, ymax)
        xres = str(cam_pos.resolution[0])  # variable length
        yres = str(cam_pos.resolution[1])

        xres_arrow = f"<{xres:-^{16 + len(xres)%2}}>"

        xres_len = len(xres_arrow)

        bbox_in = " " * (xres_len)
        bbox_top = "┌" + "─" * (xres_len) + "┐"
        bbox_bot = "└" + "─" * (xres_len) + "┘"

        xaxis = "┬" + "─" * (xres_len) + "┬"

        msg = f"""
          ∧       {xres_arrow}
{ymax   }╶┤      {bbox_top    } ∧
          │      │{bbox_in   }│ ╎
          │      │{bbox_in   }│ ╎
          │      │{bbox_in   }│ {yres}
          │      │{bbox_in   }│ ╎
          │      │{bbox_in   }│ ╎
{ymin   }╶┤      {bbox_bot    } v
          │                      
          ╎                      
           ╶╶╶───{xaxis       }─────>
             {xmin   }{' '*(len(xres_arrow)-8)}{xmax   }
"""
        print(msg)


if __name__ == "__main__":
    cam = Camera(
        cam_pos=CameraPosition(
            xmin=0,
            xmax=10,
            ymin=-2,
            ymax=2,
            resolution=(100, 40),
        )
    )
    cam.print_bbox()

    sample = cam.get_sample()

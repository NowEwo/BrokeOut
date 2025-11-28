import random

from core.context import Context
from systems.logging import Logger
from systems.config import config

class ScreenShake(Context):
    """Manages screen shake effects"""

    def __init__(self) -> None:
        self.logger: Logger = Logger("effects.screen_shake")

        self.offset: list = [0, 0]
        self.duration: int = 0
        self.magnitude: int = config.graphics.shake.magnitude

        super().__init__()

    def start(self,
              duration: int = config.graphics.shake.duration,
              magnitude: int = config.graphics.shake.magnitude) -> None:
        """Start a screen shake effect"""
        self.logger.log(f"Screen shake triggered with {duration=} frames and {magnitude=}")
        self.duration = duration
        self.magnitude = magnitude

    def get_offset(self) -> tuple:
        """Get current shake offset and update duration"""
        if self.duration > 0:
            self.offset[0] = random.randint(-self.magnitude, self.magnitude)
            self.offset[1] = random.randint(-self.magnitude, self.magnitude)
            self.duration -= 1
        else:
            self.offset[0] = 0
            self.offset[1] = 0
        return tuple(self.offset)

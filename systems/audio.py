import pygame.mixer

from systems.logging import Logger
from systems.config import config

class AudioEngine:
    def __init__(self) -> None:
        self.logger: Logger = Logger("systems.audio")

        self.current_volume: float = config.audio.volume.master
        self.requested_volume: float = self.current_volume

        pygame.mixer.init()

        self.logger.success(f"New AudioEngine initialised : {self}")

    def play_file(self, file, loop=False) -> None:
        pygame.mixer.music.load(file)
        if not pygame.mixer.music.get_busy():
            self.logger.log(f"Playing audio file {file} with {loop=}")
            pygame.mixer.music.play(-1 if loop else 0)
        else:
            self.logger.error("AudioEngine busy, cannot play music file")

    def set_volume(self, volume: float) -> None:
        self.logger.log(f"Volume change requested from {self.current_volume} to {volume}")
        self.requested_volume = volume

    def toggle(self, loop: bool = False) -> bool:
        self.logger.log("Toggling music state")
        if self.state():
            pygame.mixer.music.stop()
        else:
            pygame.mixer.music.play(-1 if loop else 0)

        return self.state()

    def stop(self) -> None:
        self.logger.log("Stopping music")
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        else:
            self.logger.error("Music not playing, cannot stop")

    def play(self, loop: bool = False) -> None:
        self.logger.log("Playing loaded music")
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1 if loop else 0)
        else:
            self.logger.warn("AudioEngine busy, stopping the current music")
            pygame.mixer.music.stop()

    def move(self, pos: int) -> None:
        self.logger.log(f"Moving music time to {pos}")
        if self.state():
            pygame.mixer.music.set_pos(pos)

    def update(self) -> None:
        if self.current_volume < self.requested_volume:
            self.current_volume += 0.01
            pygame.mixer.music.set_volume(self.current_volume)
        elif self.current_volume > self.requested_volume:
            self.current_volume -= 0.01
            pygame.mixer.music.set_volume(self.current_volume)

    @staticmethod
    def state() -> bool:
        return pygame.mixer.music.get_busy()

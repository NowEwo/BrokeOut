# type: ignore

import pygame
import pygame.freetype

from core.scene_manager import Scene
from systems import renderer

from objects.gui import mouse

class DevelopmentScene(Scene):
    # noinspection PyDefaultArgument
    def __init__(self) -> None:
        self.color = (159, 0, 0)
        self.shaders = renderer.Renderer()

        super().__init__()

    def run(self) -> None:
        self.mouse = mouse.Mouse()

        self.game.event_manager.subscribe(self, "WindowFocusLost")

    def WindowFocusLost(self, event: pygame.Event) -> None:
        self.game.running = False

    def update(self) -> None:
        pass

    def draw(self) -> None:
        self.game.window.fill(self.color)

        surface = pygame.Surface(self.game.window.get_size(), pygame.SRCALPHA)

        self.mouse.draw()

        self.game.window.blit(surface, (0, 0))

        self.shaders.render_frame()

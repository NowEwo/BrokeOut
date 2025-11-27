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

    def run(self):
        self.mouse = mouse.Mouse()

        self.game.event_manager.subscribe(self, "WindowFocusLost")

    def WindowFocusLost(self, event):
        self.game.running = False

    def update(self):
        pass

    def draw(self):
        self.game.window.fill(self.color)

        surface = pygame.Surface(self.game.window.get_size(), pygame.SRCALPHA)

        self.mouse.draw()

        self.game.window.blit(surface, (0, 0))

        self.shaders.render_frame()

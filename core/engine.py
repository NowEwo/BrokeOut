import pygame

from core import context, error_handler, scene_manager, event_manager
from systems import discord, logging
from systems.config import config


class Game:
    def __init__(self) -> None:
        self.config = config

        self.logger = logging.Logger("core.engine")
        self.error_handler = error_handler.ErrorHandler() if self.config.debug.misc.error_handler else None

        context.GameContext.set_game(self)

        self.scene_manager = scene_manager.SceneManager()
        self.event_manager = event_manager.EventManager()

    def handle_events(self):
        return self.scene_manager.active.handle_events()

    def update_window_title(self, text=""):
        pygame.display.set_caption("BrokeOut"+
                                   f"{self.config.release.version} ({self.config.release.state})"+
                                   " - " if text != '' else ""+
                                   text)

    def update(self):
        self.scene_manager.update()

    def draw(self):
        self.scene_manager.draw()

    def run(self):

        self.discordrpc = discord.DiscordRPC()

        self.logger.log("Initialising Pygame window")
        pygame.init()

        self.window = pygame.display.set_mode(
            (self.config.graphics.window.width, self.config.graphics.window.height),
            pygame.OPENGL | pygame.DOUBLEBUF
        )

        self.update_window_title()

        pygame.mouse.set_visible(False)

        self.clock = pygame.time.Clock()

        if self.config.debug.startup.scene != "default":
            self.active_scene = self.scene_manager.set_active_scene(self.config.debug.startup.scene)
        else:
            self.active_scene = self.scene_manager.set_active_scene("splash")

        self.logger.success(f"Changed current active scene")

        while True:
            if not self.handle_events():
                break
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(self.config.graphics.fps)

        self.logger.highlight(f"Have a nice day :3")

        pygame.quit()

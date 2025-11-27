# type: ignore

import random

import pygame

from core.scene_manager import Scene
from effects import screen_shake
from effects.gaussian_blur import gaussian_blur
from objects.gui import hint, mouse, button
from objects.level import player, ball, brick
from objects.level.stats import StatsElement, ProgressBar
from systems import renderer, audio
from assets.levels.levels import levels

import numpy as np

class LevelScene(Scene):

    def __init__(self) -> None:
        super().__init__()

    def run(self):
        self.game.update_window_title("Classic Game")

        self.game.event_manager.subscribe(self, "Quit")
        self.game.event_manager.subscribe(self, "MouseButtonDown")
        self.game.event_manager.subscribe(self, "KeyDown")

        self.levels = levels

        self.audio = audio.AudioEngine()
        self.audio.play_file("assets/sounds/music/audio0.opus", True)

        self.font = pygame.freetype.Font("assets/fonts/Monocraft.ttf", 36)

        self.bounds = {
            "x_min": 0,
            "y_min": 0,
            "x_max": self.game.config.graphics.render.width,
            "y_max": self.game.config.graphics.render.height
        }

        self.game_started = False
        self.lives = self.game.config.game.initial_lives if not self.game.config.debug.game.infinite_lives else -1
        self.level = 1
        self.level_size = np.count_nonzero(self.levels[(self.level - 1) % len(self.levels)])
        self.score = 0

        self.color = [255, 153, 191]

        self.screen_shake = screen_shake.ScreenShake()
        self.offset_x, self.offset_y = 0, 0

        self.player = player.Player()
        self.ball = ball.Ball()

        self.brick_group = brick.BrickGroup()
        self.skeleton = brick.BricksSkeleton()
        self.brick_group.generate_bricks()

        self.stats = [StatsElement(), ProgressBar(), hint.HintElement()]

        self.shaders = renderer.Renderer("crt")
        self.blur_radius = 0

        self.pause = False

        pygame.mouse.set_visible(False)

        if self.game.config.debug.game.autostart:
            self.ball.on_player = False
            self.ball.set_velocity_by_angle(60)
            self.game_started = True

        self.LoseMessages = [
            "Oopsie :3", "Maybe do better next time", "Actually that was fun",
            "Ew you don't play very well", "You have to touch the ball actually",
            "Stop being bad, it makes me sad", "-3/10", "Lives are falling like this ball",
            "Try harder :P","nothing beats a jet2 holiday","keep them coming","...",
        ]

        center = self.game.window.get_rect().center

        self.pause_buttons = {
            "Resume": button.Button((center[0], center[1]), [305, 51], "Resume"),
            "Settings": button.Button((center[0] - 77, center[1] + 53), [151, 51], "Settings"),
            "Quit Game": button.Button((center[0] + 77, center[1] + 53), [151, 51], "Main Menu"),
            "Quit Desktop": button.Button((center[0], center[1]+106),[305,51], "Exit the game")
        }

        self.game.discordrpc.set_rich_presence("Playing in classic mode", f"Level {self.level}")

    def background_color(self):
        return [c // 3 for c in self.color]

    def reset_game(self):
        self.screen_shake.start(10, 5)

        self.brick_group.generate_bricks()

        self.color = [255, 153, 191]
        self.game_started = False
        self.level = 1
        self.lives = self.game.config.game.initial_lives
        self.score = 0

        self.ball.speed = self.game.config.game.ball.speed
        self.player.width = self.player.base_width

        self.stats[2].show_hint(f"Level {self.level}", size=24)
        self.game.discordrpc.set_rich_presence("Playing in classic mode", f"Level {self.level}")

    def trigger_next_level(self):
        self.level += 1

        self.color = [random.randint(150, 255) for _ in range(3)]
        self.skeleton = brick.BricksSkeleton()
        self.brick_group.generate_bricks()

        self.screen_shake.start(10, 5)
        self.level_size = np.count_nonzero(self.levels[(self.level-1)%len(self.levels)])
        self.lives += 4

        self.logger.log(f"{self.level_size=}")

        self.stats[2].show_hint(f"Level {self.level}", size=24)
        self.game.discordrpc.set_rich_presence("Playing in classic mode", f"Level {self.level}")

    def trigger_lose(self):
        if self.lives != 1:
            self.stats[2].show_hint(random.choice(self.LoseMessages), size=24)
            self.lives -= 1
            self.logger.log(
                f"Player lose this round, now having {self.lives} more lives"
            )
        else:
            self.logger.log("Player lose the game, resetting all states")
            self.reset_game()
        self.ball.on_player = True

    def Quit(self, event):
        exit(0)

    def MouseButtonDown(self, event):
        if event.button == 1 and self.ball.on_player and not self.pause:
            self.ball.on_player = False
            self.ball.set_velocity_by_angle(60)

            if not self.game_started:
                self.level = 1
                self.game_started = True

        if self.pause:
            if self.pause_buttons["Resume"].get_collided():
                self.pause = False
            elif self.pause_buttons["Quit Game"].get_collided():
                self.game.scene_manager.set_active_scene("menu")
            elif self.pause_buttons["Quit Desktop"].get_collided():
                self.game.running = False

    def KeyDown(self, event):
        if event.key == pygame.K_ESCAPE:
            # self.game.scene_manager.set_active_scene("menu")
            self.blur_radius = 0
            self.pause = not self.pause

            self.shaders.update_values = not self.shaders.update_values
            self.shaders.set_curvature(0)
        if event.key == pygame.K_SPACE:
            self.trigger_next_level()

    def update(self):
        # self.color = [random.randint(150,255) for i in range(3)]

        if self.blur_radius < 10 and self.pause:
            self.blur_radius += (10 - self.blur_radius) * 0.3

        if not self.pause:
            [i.update() for i in self.stats]
            self.brick_group.update()
            self.player.update()
            self.ball.update()
        else:
            for i in self.pause_buttons:
                self.pause_buttons[i].update()

    def draw(self):
        self.offset_x, self.offset_y = self.screen_shake.get_offset()

        self.game.window.fill([c // 3 for c in self.color])

        self.surface = pygame.Surface(self.game.window.get_size(), pygame.SRCALPHA)

        self.skeleton.draw()
        self.brick_group.draw()
        self.player.draw()
        self.ball.draw()

        [i.draw() for i in self.stats]

        self.game.window.blit(self.surface, [self.offset_x, self.offset_y])

        if self.pause:
            pause_surface = pygame.Surface(self.game.window.get_size(), pygame.SRCALPHA)

            self.game.window = gaussian_blur(self.game.window, self.blur_radius)

            # Menu pause code
            for i in self.pause_buttons:
                self.pause_buttons[i].draw(pause_surface)

            self.game.window.blit(pause_surface)

            mouse.Mouse().draw()

        self.shaders.render_frame()

# type: ignore

import pygame

from core.context import GameContext
from objects.prototype import Entity


class Player(Entity, GameContext):
    def __init__(self) -> None:
        super().__init__()

        self.base_width = self.game.config.game.player.width_multiplier * self.game.config.game.ball.radius
        self.width = self.base_width

        self.x = (self.scene.bounds['x_min'] - self.scene.bounds['x_max']) / 2
        self.y = self.scene.bounds['y_max'] - self.game.config.game.ball.radius - 5

        self.autoplay = self.game.config.debug.game.autoplay

    def collides_with_ball(self, ball):
        """Check collision with ball"""
        vertical = abs(self.y - ball.y) < 2 * self.game.config.game.ball.radius
        horizontal = abs(self.x - ball.x) < self.width / 2 + self.game.config.game.ball.radius
        return vertical and horizontal

    def update(self):
        x = pygame.mouse.get_pos()[0] if not self.autoplay else self.scene.ball.x
        if x - self.width / 2 < self.scene.bounds['x_min']:
            self.x = self.scene.bounds['x_min'] + self.width / 2
        elif x + self.width / 2 > self.scene.bounds['x_max']:
            self.x = self.scene.bounds['x_max'] - self.width / 2
        else:
            self.x = x

        if self.width > self.base_width:
            self.width = self.width - 0.1

    def draw(self):
        rect = pygame.Rect(
            int(self.x - self.width / 2 + self.scene.offset_x),
            int(self.y - self.game.config.game.ball.radius + self.scene.offset_y),
            self.width,
            2 * self.game.config.game.ball.radius
        )
        pygame.draw.rect(self.scene.surface, self.scene.color, rect, 0)

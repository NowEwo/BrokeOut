import math
import random

import numpy as np
import pygame

from objects.prototype import Entity


class Ball(Entity):
    """Ball object that also manages the trail"""

    def __init__(self):
        super().__init__()

        self.x, self.y = 500, 500
        self.speed = self.game.config.game.ball.speed
        self.vx = 0
        self.vy = 0
        self.on_player = True
        self.trail = []
        self.set_velocity_by_angle(60)

        self.gravity_enabled = False

    def set_velocity_by_angle(self, angle):
        """Set ball velocity based on angle"""
        self.vx = self.speed * math.cos(math.radians(angle))
        self.vy = -self.speed * math.sin(math.radians(angle))

    def draw(self):
        """Draw ball and trail"""
        current_pos = (int(self.x - self.game.config.game.ball.radius),
                       int(self.y - self.game.config.game.ball.radius))
        self.trail.insert(0, current_pos)

        if len(self.trail) > self.game.config.graphics.ball.trail_length:
            self.trail.pop()

        # Draw trail with gradient effect generated from numpy (What did I do that ? -Ewo)
        gradient = np.arange(0, 255, self.game.config.graphics.ball.trail_length)
        if self.scene.game_started:
            for i, pos in enumerate(reversed(self.trail)):
                pygame.draw.circle(self.scene.surface,
                                   (self.scene.color[0], self.scene.color[1], self.scene.color[2], gradient[i]), pos,
                                   self.game.config.game.ball.radius, 0)

        # Draw actual ball
        pygame.draw.circle(self.scene.surface, self.scene.color, current_pos, self.game.config.game.ball.radius, 0)

    def bounce_off_player(self, player):
        """Calculate bounce angle based on player hit x"""
        diff = player.x - self.x
        total_length = player.width / 2 + self.game.config.game.ball.radius
        angle = 90 + 80 * diff / total_length
        self.set_velocity_by_angle(angle)

    def update(self):  # type: ignore
        """Update ball position and handle collisions"""
        if self.on_player:
            self.y = self.scene.player.y - 1.5 * self.game.config.game.ball.radius
            self.x = self.scene.player.x + self.game.config.game.ball.radius
        else:
            self.x += self.vx
            self.vy += 0.3 * self.gravity_enabled
            self.y += self.vy

            # Player collision
            if self.scene.player.collides_with_ball(self) and self.vy > 0:
                if not self.scene.player.autoplay:
                    self.bounce_off_player(self.scene.player)
                else:
                    self.vx = self.speed * math.cos(math.radians(random.randint(0, 180)))
                    self.vy = -self.vy

            # Wall collisions
            if (self.x + self.game.config.game.ball.radius > self.scene.bounds['x_max'] or
                    self.x - self.game.config.game.ball.radius < self.scene.bounds['x_min']):
                self.vx = -self.vx

            # Lose the game (Bottom)
            if self.y + self.game.config.game.ball.radius > self.scene.bounds['y_max']:
                self.scene.trigger_lose()

            # Top
            if self.y - self.game.config.game.ball.radius < self.scene.bounds['y_min']:
                self.vy = -self.vy

        return None

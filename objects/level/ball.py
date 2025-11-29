import random
import math

import numpy as np
import pygame

from objects.prototype import Entity


class Ball(Entity):
    """Ball object that also manages the trail"""

    def __init__(self) -> None:
        super().__init__()

        self.pos: list = [500, 500]
        self.velocity: list = [0, 0]

        self.speed: int = self.game.config.game.ball.speed

        self.on_player: bool = True

        self.trail: list = []

        self.set_velocity_by_angle(60)

    def set_velocity_by_angle(self, angle: int) -> None:
        """Set ball velocity based on angle"""
        self.velocity = [
            self.speed * math.cos(math.radians(angle)),
            -self.speed * math.sin(math.radians(angle)),
        ]

    def draw(self) -> None:
        """Draw ball and trail"""
        current_pos = (
            self.pos[0] - self.game.config.game.ball.radius,
            self.pos[1] - self.game.config.game.ball.radius,
        )
        self.trail.insert(0, current_pos)

        if len(self.trail) > self.game.config.graphics.ball.trail_length:
            self.trail.pop()

        # Draw trail with gradient effect generated from numpy (What did I do that ? -Ewo)
        gradient = np.arange(0, 255, self.game.config.graphics.ball.trail_length)
        if self.scene.game_started:
            for i, pos in enumerate(reversed(self.trail)):
                pygame.draw.circle(
                    self.scene.surface,
                    (
                        self.scene.color[0],
                        self.scene.color[1],
                        self.scene.color[2],
                        gradient[i],
                    ),
                    pos,
                    self.game.config.game.ball.radius,
                    0,
                )

        # Draw actual ball
        pygame.draw.circle(
            self.scene.surface,
            self.scene.color,
            current_pos,
            self.game.config.game.ball.radius,
            0,
        )

    def bounce_off_player(self) -> None:
        """Calculate bounce angle based on player hit x"""
        diff = self.scene.player.pos[0] - self.pos[0]
        total_length = self.scene.player.width / 2 + self.game.config.game.ball.radius
        angle: int = 90 + 80 * diff / total_length
        self.set_velocity_by_angle(angle)

    def update(self) -> None:  # type: ignore
        """Update ball position and handle collisions"""
        if self.on_player:
            self.pos = [
                self.scene.player.pos[0] + self.game.config.game.ball.radius,
                self.scene.player.pos[1] - 1.5 * self.game.config.game.ball.radius,
            ]
        else:
            self.pos = [self.pos[0] + self.velocity[0], self.pos[1] + self.velocity[1]]

            # Player collision
            if self.scene.player.collides_with_ball(self) and self.velocity[1] > 0:
                if not self.scene.player.autoplay:
                    self.bounce_off_player()
                else:
                    self.velocity = [
                        self.speed * math.cos(math.radians(random.randint(0, 180))),
                        -self.velocity[1],
                    ]

            # Wall collisions
            if (
                self.pos[0] + self.game.config.game.ball.radius
                > self.scene.bounds["x_max"]
                or self.pos[0] - self.game.config.game.ball.radius
                < self.scene.bounds["x_min"]
            ):
                self.velocity[0] *= -1

            # Lose the game (Bottom)
            if (
                self.pos[1] + self.game.config.game.ball.radius
                > self.scene.bounds["y_max"]
            ):
                self.scene.trigger_lose()

            # Top
            if (
                self.pos[1] - self.game.config.game.ball.radius
                < self.scene.bounds["y_min"]
            ):
                self.velocity[1] *= -1

        return None

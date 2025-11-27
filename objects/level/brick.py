import random
import math

import pygame

from objects.prototype import Entity
from systems.logging import Logger


class Brick(Entity):
    """Brick object, That's, Ewww, A Brick"""

    def __init__(self, x, y, scene):
        super().__init__()
        self.logger = Logger("objects.brick", False)

        self.x = x
        self.y = y
        self.life = random.randint(1, 3)
        self.text = ""
        self.width = 50
        self.height = 30

        # Random color variation
        divisor = random.randint(2, 5)
        self.scene = scene
        self.color = [c // (divisor // 2) for c in scene.color]

        # self.logger.log(f"New brick with props [{x=} {y=} {self.width=} {self.height=} {self.life=} {self.color=}] as {self}")

    def is_alive(self):
        """Check if brick is still alive (This was a trial, I'm making a note here: Huge success)"""
        return self.life > 0

    def draw_text(self):
        self.text_rect = self.scene.font.get_rect("•" * self.life, size=16)
        self.text_rect.center = (self.x, self.y)

        self.scene.font.render_to(self.scene.surface, self.text_rect, "•" * self.life, self.scene.background_color(),
                                  size=16)

    def draw(self):
        """Draw the brick"""
        rect = pygame.Rect(
            int(self.x - self.width / 2 + self.scene.offset_x),
            int(self.y - self.height / 2 + self.scene.offset_y),
            self.width,
            self.height
        )
        pygame.draw.rect(self.scene.surface, self.color, rect, 0)
        self.draw_text()

    def draw_skeleton(self):
        width, height = self.width*0.9, self.height*0.9
        rect = pygame.Rect(
            int(self.x - width / 2 + self.scene.offset_x),
            int(self.y - height / 2 + self.scene.offset_y),
            width,
            height
        )
        pygame.draw.rect(self.scene.surface, self.color + [25], rect, 0)

    def handle_hit(self):
        self.life -= 1
        self.logger.log(f"Brick {self} got hit ({self.life} left)")

        score_change = 1500
        self.scene.score += score_change

    def check_ball_collision(self):
        """Check and handle collision with ball"""
        ball = self.scene.ball

        rect = pygame.Rect(
            self.x - self.width / 2,
            self.y - self.height / 2,
            self.width,
            self.height
        )

        closest_x = max(rect.left, min(ball.x, rect.right))
        closest_y = max(rect.top, min(ball.y, rect.bottom))

        dx = ball.x - closest_x
        dy = ball.y - closest_y

        if (dx * dx + dy * dy) < self.game.config.game.ball.radius ** 2:
            overlap_x = self.game.config.game.ball.radius - abs(dx)
            overlap_y = self.game.config.game.ball.radius - abs(dy)

            if overlap_x < overlap_y:
                ball.vx = -ball.vx
                ball.x += math.copysign(overlap_x, dx) # overlap_x value but dx sign
            else:
                ball.vy = -ball.vy
                ball.y += math.copysign(overlap_y, dy) # overlap_y value but dy sign

            self.handle_hit()

            self.scene.screen_shake.start(duration=3, magnitude=3)
            self.scene.shaders.set_curvature(0.41)

            return True

        return False

class LargeBrick(Brick):
    def __init__(self, x, y, scene):
        super().__init__(x, y, scene)

    def handle_hit(self):
        if self.scene.player.width>=220:
            self.scene.player.width=220
        else:
            self.scene.player.width += 50
        self.life = -1

    def draw_text(self):
        self.text_rect = self.scene.font.get_rect("<->", size=16)
        self.text_rect.center = (self.x, self.y)

        self.scene.font.render_to(self.scene.surface, self.text_rect, "<->", self.scene.background_color(),
                                  size=16)

class FastBrick(Brick):
    def __init__(self, x, y, scene):
        super().__init__(x, y, scene)

    def handle_hit(self):
        if self.scene.ball.speed>= 16:
            self.scene.ball.speed =16
        else:
            self.scene.ball.speed += 2
        self.life = -1

    def draw_text(self):
        self.text_rect = self.scene.font.get_rect(">>>", size=16)
        self.text_rect.center = (self.x, self.y)

        self.scene.font.render_to(self.scene.surface, self.text_rect, ">>>", self.scene.background_color(),
                                  size=16)




class BrickGroup(Entity):
    def __init__(self) -> None:
        self.logger = Logger("objects.brick.brickgroup")
        self.bricks = []

        super().__init__()

        self.logger.log("Initialised brick group")

    def generate_bricks(self):
        """Generate brick layout"""
        self.bricks = []
        level = self.scene.levels[(self.scene.level-1)%len(self.scene.levels)]
        self.logger.log(f"{level=}", "group_verbose")
        for line in range(len(level)):
            for brick in range(len(level[line])):
                if level[line][brick] != 0 :
                    brick = (
                        level[line][brick]
                        (((line % 2) * 13) + 51 + (brick * 53), 59 + (line * 33), self.scene)
                    )
                    self.bricks.append(brick)

    def update(self):
        if not self.bricks:
            self.logger.log(f"All bricks are broken, advancing level {self.scene.level}")
            self.scene.trigger_next_level()
            self.generate_bricks()

        new_bricks = []
        for brick in self.bricks:
            if brick.is_alive():
                brick.check_ball_collision()
                new_bricks.append(brick)
        self.bricks = new_bricks

    def draw(self):
        for brick in self.bricks:
            if brick.is_alive():
                brick.draw()
            else:
                self.bricks.remove(brick)

class BricksSkeleton(Entity):
    def __init__(self) -> None:
        self.logger = Logger("objects.brick.bricks_skeleton")
        self.bricks = []

        super().__init__()

        self.logger.log("Initialised brick group")
        self.level = self.scene.levels[self.scene.level%len(self.scene.levels)]
        for line in range(len(self.level)):
            for brick in range(len(self.level[line])):
                if self.level[line][brick] != 0 :
                    brick = (
                        self.level[line][brick]
                        (((line % 2) * 13) + 51 + (brick * 53), 59 + (line * 33), self.scene)
                    )
                    self.bricks.append(brick)

    def draw(self):
        for brick in self.bricks:
            brick.draw_skeleton()
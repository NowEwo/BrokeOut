# type: ignore

import pygame
import pygame.freetype

from objects import prototype


class Button(prototype.Entity):
    def __init__(self, pos, size, text, onclick=None) -> None:
        # Pos = (x, y), Size = (x, y), text="str" onclick=function()
        self.font = pygame.freetype.Font("assets/fonts/Monocraft.ttf", 36)
        self.size = self.base_size = size
        self.text = text
        self.pos = pos

        self.onclick = onclick
        super().__init__()

        self.game.event_manager.subscribe(self, "MouseButtonDown")

    def get_collided(self):
        button = pygame.Rect(
            (self.pos[0]-(self.size[0]//2), self.pos[1]-(self.size[1]//2)),
            (self.size)
        )
        return button.collidepoint(pygame.mouse.get_pos())

    def MouseButtonDown(self, event):
        if self.get_collided() and event.button == 1:
            if self.onclick is not None:
                self.onclick()

    def draw(self, surface, bg_color=(173, 95, 125), fg_color=(246, 172, 201)):
        mouse = pygame.mouse.get_pos()
        button = pygame.Rect(
            (self.pos),
            (self.size)
        )
        self.text_rect = self.font.get_rect(self.text, size=21)
        button.center = self.text_rect.center = self.pos

        pygame.draw.rect(surface, (bg_color[0], bg_color[1], bg_color[2], 93 if button.collidepoint(mouse) else 51), button, border_radius=3)
        for i in range(1, 3):
            pygame.draw.rect(surface, fg_color, (self.pos[0] - (self.size[0]//2) + 3 - i, self.pos[1] - (self.size[1]//2) + 3 - i, self.size[0], self.size[1]), 1, border_radius=2)
        self.font.render_to(surface, self.text_rect, self.text, [c for c in fg_color], size=21)

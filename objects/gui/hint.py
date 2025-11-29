from objects.prototype import Entity


class HintElement(Entity):

    def __init__(self) -> None:
        self.timer: int = 120
        self.hint_text: str = "Click to start game"
        self.size: int = 24

        super().__init__()

    def update(self) -> None:
        self.timer -= 1

    def draw(self) -> None:
        if self.timer > 0:
            text_rect = self.scene.font.get_rect(self.hint_text, size=self.size)
            text_rect.center = (
                self.scene.surface.get_rect().center[0],
                self.game.config.graphics.render.height - 139,
            )

            self.scene.font.render_to(
                self.scene.surface,
                text_rect,
                self.hint_text,
                (
                    self.scene.color[0],
                    self.scene.color[1],
                    self.scene.color[2],
                    self.timer,
                ),
                size=self.size,
            )

    def show_hint(self, text: str, duration: int = 120, size: int = 24) -> None:
        """Display a hint message (Subtitle-like)"""
        self.timer = duration
        self.hint_text = text
        self.size = size

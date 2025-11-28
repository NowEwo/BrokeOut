from core.engine import Game

from systems.logging import Logger

def main() -> None:
    Logger("main").highlight("Welcome to BrokeOut")
    Game().run()

if __name__ == "__main__":
    main()
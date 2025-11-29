"""
main - Entry point of the engine

EwoFluffy - BrokeTeam - 2025
"""

from core.engine import Game
from systems.logging import Logger

retries: int = 0
logger: Logger = Logger("main")


def main() -> None:
    global retries
    logger.highlight("Welcome to BrokeOut")
    try:
        Game().run()
    except KeyboardInterrupt:
        pass
    except Exception:
        if retries < 3:
            logger.error("Game crashed, let's try restarting")
            retries += 1
            main()
        else:
            logger.critical(f"Ew, something's off. Game crashed {retries} time")
    finally:
        logger.highlight("Have a nice day")


if __name__ == "__main__":
    main()

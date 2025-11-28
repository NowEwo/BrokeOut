from systems.config import config

from datetime import datetime

from systems.config import config

import colorama

class Logger:
    def __init__(self, name: str = "Logger element", verbose: bool = True) -> None:
        self.name: str = name

        if verbose:
            self.log(f"Logger element created for {name} as {self}")

    def check_enabled(self, group: str | None) -> bool:
        r = False
        if "special.all" in config.debug.logs:
            if config.debug.logs["special.all"]:
                r = True

        if self.name in config.debug.logs:
            if not config.debug.logs[self.name]:
                r = False
            else:
                r = True

        if not group is None:
            if self.name+"."+group in config.debug.logs:
                if not config.debug.logs[self.name+"."+group]:
                    r = False
                else:
                    r = True

        return r

    def log(self, message: str, group: str | None = None) -> None:
        if config.engine.log_level > 3 and self.check_enabled(group):
                print(f"{colorama.Fore.BLUE}({datetime.now()}) [{self.name}] {message}{colorama.Fore.RESET}")

    def highlight(self, message: str, group: str | None = None) -> None:
        if config.engine.log_level > -1 and self.check_enabled(group):
               print(
                f"{colorama.Back.WHITE}{colorama.Fore.BLACK}({datetime.now()}) [{self.name}] {message}{colorama.Fore.RESET}{colorama.Back.RESET}")

    def warn(self, message: str, group: str | None = None) -> None:
        if config.engine.log_level > 2 and self.check_enabled(group):
                print(f"{colorama.Fore.YELLOW}({datetime.now()}) [{self.name}{('.'+group) if group else ''}] {message}{colorama.Fore.RESET}")

    def success(self, message: str, group: str | None = None) -> None:
        if config.engine.log_level > 3 and self.check_enabled(group):
                print(f"{colorama.Fore.GREEN}({datetime.now()}) [{self.name}{('.'+group) if group else ''}] {message}{colorama.Fore.RESET}")

    def error(self, message: str, group: str | None = None) -> None:
        if config.engine.log_level > 1 and self.check_enabled(group):
                print(f"{colorama.Fore.RED}({datetime.now()}) [{self.name}{('.'+group) if group else ''}] {message}{colorama.Fore.RESET}")

    def critical(self, message: str, group: str | None = None) -> None:
        if config.engine.log_level > 0 and self.check_enabled(group):
                print(f"{colorama.Back.RED}({datetime.now()}) [{self.name}{('.'+group) if group else ''}] {message}{colorama.Back.RESET}")

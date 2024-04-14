import time
from scripts.log import Log


class Sleep:
    def __init__(self, log: Log, symbols: list[str] = None) -> None:
        self.log = log
        self.symbol = symbols if symbols else ["⣾", "⣷", "⣯", "⣟", "⡿", "⢿", "⣻", "⣽"]

    def sleep(
        self, seconds: int, message: str, erase_len: int = 100, up_cursor: int = -1
    ) -> None:
        for _ in range(seconds):
            msg = message.replace("{{symbol}}", self.symbol[_ % len(self.symbol)])
            msg = msg.replace("{{time_asc}}", str(_))
            msg = msg.replace("{{time_desc}}", str(seconds - _))
            self.log.verbose(
                f"\r{msg}",
                end="",
                flush=True,
            )
            time.sleep(1)
            self.log.verbose(
                f"\033[{up_cursor}A\r" + " " * erase_len + "\r", end="", flush=True
            )

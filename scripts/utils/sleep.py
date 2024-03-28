import time
from utils.log import Log


class Sleep:
    def __init__(self, log: Log, symbols: list[str] = None) -> None:
        self.log = log
        self.symbol = symbols if symbols else ["⣾", "⣷", "⣯", "⣟", "⡿", "⢿", "⣻", "⣽"]

    def sleep(self, seconds: int, message: str) -> None:
        for _ in range(seconds):
            msg = message.replace("{{symbol}}", self.symbol[_ % len(self.symbol)])
            msg = msg.replace("{{time_asc}}", _)
            msg = msg.replace("{{time_desc}}", seconds - _)
            self.log.verbose(
                msg,
                end="",
                flush=True,
            )
            time.sleep(1)
            self.log.verbose("\r" + " " * 100 + "\r", end="", flush=True)

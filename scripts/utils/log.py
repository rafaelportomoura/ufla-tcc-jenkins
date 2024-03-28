class Log:
    RESET = "\x1b[0m"
    RED = "\x1b[0;31m"
    CYAN = "\x1b[36m"
    GRAY = "\x1b[90m"

    def __init__(self, log_level=1):
        self.log_level = log_level

    def beautify(self, ansi, string) -> str:
        return f"{ansi}{string}{Log.RESET}"

    def error(self, *args, end="\n", flush=False) -> None:
        if self.log_level >= 0:
            self.__out("❌", *args, ansi=Log.RED, end=end, flush=flush)

    def checkpoint(self, *args, end="\n", flush=False) -> None:
        if self.log_level >= 1:
            self.__out("🚀", *args, ansi=Log.CYAN, end=end, flush=flush)

    def info(self, *args, ansi=None, end="\n", flush=False) -> None:
        if self.log_level >= 2:
            self.__out(*args, ansi=ansi, end=end, flush=flush)

    def cmd(self, *args, end="\n", flush=False) -> None:
        if self.log_level >= 3:
            self.__out("$", *args, ansi=Log.GRAY, end=end, flush=flush)

    def verbose(self, *args, ansi=None, end="\n", flush=False) -> None:
        if self.log_level >= 3:
            self.__out(*args, ansi=ansi, end=end, flush=flush)

    def __out(self, *args, ansi=None, end: str, flush: bool) -> None:
        if not ansi:
            print(*args, end=end, flush=flush)
            return

        string = " ".join(args)

        print(self.beautify(ansi, string), end=end, flush=flush)

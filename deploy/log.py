class Log:
    RESET = '\x1b[0m'
    RED = '\x1b[0;31m'
    CYAN = '\x1b[36m'
    GRAY = '\x1b[90m'

    def __init__(self, log_level = 1):
        self.log_level = log_level
    

    def beautify(self,ansi,string) -> str:
        return f"{ansi}{string}{Log.RESET}"
    
    def error(self, *args) -> None:
        if (self.log_level >= 0): self.__out("❌",*args, ansi=Log.RED)

    def checkpoint(self, *args) -> None:
        if (self.log_level >= 1): self.__out("🚀",*args, ansi=Log.CYAN)

    def info(self, *args, ansi= None) -> None:
        if (self.log_level >= 2): self.__out(*args, ansi=ansi)

    def cmd(self, *args) -> None:
        if (self.log_level >= 3): self.__out("$",*args, ansi=Log.GRAY)

    def verbose(self, *args, ansi= None) -> None:
        if (self.log_level >= 3): self.__out(*args, ansi=ansi)

    def __out(self,  *args, ansi= None) -> None:
        if (not ansi):
            print(*args)
            return
        
        string = " ".join(args)

        print(self.beautify(ansi,string))
    
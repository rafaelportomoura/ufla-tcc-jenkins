import sys

boolean_arg = lambda a, x: a.startswith(f"--{x}")
string_arg = lambda a, x: a.startswith(f"{x}=")


def get_args(params: dict) -> dict:
    response = {}
    for param in params.keys():
        ty = params[param]["type"]
        required = params[param]["required"]

        if ty == "bool":
            response[param] = False
        else:
            response[param] = params[param]["default"] if not required else None

        value = get_param(param, ty)

        if value == None and required:
            print(f"Param {param} is required")
            sys.exit(1)
        elif value != None:
            response[param] = value
    return response


def get_param(param: str, ty: str) -> str | int | float | bool | None | list[str]:
    for arg in sys.argv[1:]:
        if arg.startswith(f"{param}="):
            response = arg.split("=")[1]
            if ty == "list":
                response = response.split(",")
            elif ty == "int":
                response = int(response, base=10)
            elif ty == "float":
                response = float(response)
            sys.argv.remove(arg)
            return response
        elif arg == f"--{param}":
            return True
    return None

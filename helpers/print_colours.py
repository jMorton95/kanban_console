from environment.colours import Terminal


#Wrapper for our pre-defined console output colours.
#Could be generic enough to take in the colour as an arg, but cleaner to work with in important areas by having it all handled by a function. 
def print_green(message: str):
    print(Terminal.OKGREEN + message + Terminal.ENDC)

def print_red(message: str):
    print(Terminal.FAIL + message + Terminal.ENDC)

def print_blue(message: str):
    print(Terminal.OKBLUE + message + Terminal.ENDC)

def print_yellow(message: str):
    print(Terminal.WARNING + message + Terminal.ENDC)

def print_beige(message: str):
    print(Terminal.HEADER + message + Terminal.ENDC)

def prompt_underline(message: str):
    return input(Terminal.UNDERLINE + message + Terminal.ENDC)
from pyfiglet import Figlet

## Print een banner uit in de console wanneer de bot opstart

def print_banner():
    f = Figlet(font="slant")
    print(f.renderText("NAWIDS BOT"))
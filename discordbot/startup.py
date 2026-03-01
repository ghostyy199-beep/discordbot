import os
import sys
from pathlib import Path


def add_to_startup():
    startup_folder = Path(os.getenv("APPDATA")) / r"Microsoft\Windows\Start Menu\Programs\Startup"
    project_path = Path(__file__).parent.resolve()
    python_exe = sys.executable
    bat_file = startup_folder / "nawidsbot_startup.bat"

    if bat_file.exists():
        print("Startup bestand bestaat al.")
        return

    bat_content = f'''@echo off
cd "{project_path}"
"{python_exe}" main.py
'''

    with open(bat_file, "w") as f:
        f.write(bat_content)

    print("Bot succesvol toegevoegd aan startup.")


if __name__ == "__main__":
    add_to_startup()
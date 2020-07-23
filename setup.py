import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"],
                     "include_files":["bg.png", "cursor.png", "game_music.wav", "death.wav", "explosion.wav",
                                      "menu_music.mp3", "self_hit.wav", "shoot.wav", "CutiveMono-Regular.ttf",
                                      "DancingScript-Regular.ttf", "IndieFlower.ttf", "Roboto-Thin.ttf", "Walkway.ttf",
                                      "music-on.png", "music-off.png", "sensitivity.png"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"


setup(  name = "",
        version = "0.1",
        description = "Game",
        options = {"build_exe": build_exe_options},
        executables = [Executable("main.py", base=base)])
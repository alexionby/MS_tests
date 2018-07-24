import os
from cx_Freeze import setup, Executable

include_files = ["static/" , "templates/"]
if "visits.db" in os.listdir():
    include_files.append("visits.db")

build_exe_options = {"packages": ["flask","asyncio","pandas","jinja2","numpy"], 
                     "excludes": ["tkinter"], 
                     "include_files": include_files,
                     "optimize": 0
                    }

setup(
    name = "MS_Tests",
    version = "0.2.1",
    copyright = "b",
    trademark = "b",
    description = "Multiple Sclerosis testing app",
    executables = [Executable("app.py", 
                    targetName="MS_Tests.exe", 
                    icon="brain.ico",
                    shortcutName="Multiple Sclerosis Tests",
                    shortcutDir="DesktopFolder"
                    )],
    options = {"build_exe": build_exe_options},
)

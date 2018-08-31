import os
from cx_Freeze import setup, Executable

include_files = ["static/" , "templates/"]

if "visits.db" in os.listdir():
    include_files.append("visits.db")

build_exe_options = {"packages": ["numpy", "jinja2", "asyncio"], 
                     "excludes": ["tkinter"], 
                     "include_files": include_files,
                    }

setup(
    name = "MS_Tests",
    version = "0.2.1",
    description = "Multiple Sclerosis testing app",
    executables = [Executable("app.py",
                    #base = "Win32GUI", 
                    base='console',
                    targetName="MS_Tests.exe", 
                    icon="brain.ico",
                    shortcutName="Multiple Sclerosis Tests",
                    shortcutDir="DesktopFolder"
                    )],
    options = {"build_exe": build_exe_options},
)

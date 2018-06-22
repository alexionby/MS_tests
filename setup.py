from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["flask","asyncio","pandas","jinja2","numpy"], 
                     "excludes": ["tkinter"], 
                     "include_files": ["static/" , "templates/", "visits.db"],
                     "optimize": 0
                    }

setup(
    name = "MS_Tests",
    version = "0.2",
    copyright = "BSMU IT lab. 2018",
    trademark = "BSMU IT lab. 2018",
    description = "Multiple Sclerosis testing app",
    executables = [Executable("app.py", 
                    targetName="MS_Tests.exe", 
                    icon="brain.ico",
                    shortcutName="Multiple Sclerosis Tests",
                    shortcutDir="DesktopFolder"
                    )],
    options = {"build_exe": build_exe_options},
)

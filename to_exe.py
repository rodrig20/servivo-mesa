from subprocess import Popen
from pathlib import Path

dir_path = str(Path.cwd()).replace("\\", "/")

comando = f'pyinstaller --noconfirm --onedir --windowed --exclude-module PyQt5 --exclude-module tkinter --exclude-module _tkinter --add-data "{dir_path}/app;app/" --add-data "{dir_path}/config;config/" --add-data "{dir_path}/interface;interface/" --icon="{dir_path}/interface/Ui/images/icon.ico" --distpath "{dir_path}/executavel/dist" --workpath "{dir_path}/executavel/build" --specpath "{dir_path}/executavel" "{dir_path}/main.py"'


process = Popen(comando.strip())
process.wait()

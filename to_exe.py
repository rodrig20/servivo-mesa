from subprocess import Popen
from pathlib import Path

dir_path = str(Path.cwd()).replace("\\","/")

comando = 'pyinstaller --noconfirm --onedir --windowed --exclude-module PyQt5 --exclude-module tkinter --exclude-module _tkinter --add-data "var(dir)/app;app/" --add-data "var(dir)/config;config/" --add-data "var(dir)/interface;interface/" --icon="var(dir)/interface/Ui/images/icon.ico" --distpath "var(dir)/executavel/dist" --workpath "var(dir)/executavel/build" --specpath "var(dir)/executavel" "var(dir)/main.py"'
comando = comando.replace("var(dir)",dir_path)

process = Popen(comando.strip())
process.wait()
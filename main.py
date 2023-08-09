import ctypes
ctypes.windll.user32.SetProcessDPIAware()

from interface import start_window
import argparse
from app import *


if __name__ == "__main__":
    # Criar um objeto ArgumentParser
    parser = argparse.ArgumentParser(description='App para serviço de mesa')

    # Adicionar a flag --fast-start
    parser.add_argument('--fast-start', action='store_true', help='Iniciar app sem necessidade de GUI')

    # Fazer o parsing dos argumentos da linha de comando
    args = parser.parse_args()
    if args.fast_start:
        from config.config import ConfigServer
        from threading import Thread
        import signal
        import json
        import time
        import os
        
        config = ConfigServer()
        try:
            with open(config.config_path+"network_access.json") as na:
                info = json.load(na)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            print("Não existem configurações feitas!")
        else:
            config.prepare_config(info)
            fun = run_app(config)
            print(config.password)
            
            thread = Thread(target=fun)
            thread.start()
            input("-> Enter para Parar \n")
            if "loophole" in config.type:
                config.run_loophole = 0
                while config.run_loophole != 2:
                    time.sleep(0.1)
                        
            os.kill(os.getpid(), signal.SIGINT)   
        
    else:
        start_window(run_app)
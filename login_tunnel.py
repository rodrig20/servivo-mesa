import subprocess
import time

def login_loophole(folder, file):
    if folder != '':
        sep = '\\'
    else:
        sep =''
    command = f"{folder}{sep}loophole.exe account login > {folder}{sep}{file}"

    # Execute o comando e redirecione a saída para um PIPE
    process = subprocess.Popen(command.split(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)# Inicia o processo
    time.sleep(1)
    inicio = "\x1b[33m"
    fim = "\x1b[0m"
    substrings = []
    index_inicio = 0
    index_fim = 0   
    with open(folder+"/"+file, "r") as f:
        string = f.readline()
    while True:
        index_inicio = string.find(inicio, index_fim)
        if index_inicio == -1:
            break
        
        index_fim = string.find(fim, index_inicio + 1)
        if index_fim == -1:
            break
        
        substrings.append(string[index_inicio + len(inicio):index_fim])

    if process.poll() is None:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC


        chrome_driver_path = 'chromeDriver/chromedriver.exe'

        # Inicie o serviço do driver do Google Chrome
        service = Service(chrome_driver_path)

        # Opções para rodar o navegador sem abrir a janela do navegador
        options = Options()
        options.headless = True

        # Inicie o navegador passando o serviço e as opções como parâmetros
        driver = webdriver.Chrome(service=service, options=options)
        wait = WebDriverWait(driver, 10)

        driver.get(substrings[0])

        #Esperar o elemento "code" ficar visível e enviá-lo
        code = wait.until(EC.visibility_of_element_located((By.NAME, "code")))
        code.send_keys(str(substrings[1]))

        enviar = driver.find_element(By.NAME, "action")
        enviar.click()

        # Esperar o elemento "action" ficar clicável e clicar nele
        confirmar = wait.until(EC.element_to_be_clickable((By.NAME, "action")))
        confirmar.click()
        
        wait.until(EC.visibility_of_element_located((By.NAME, "email")))
        
        email = driver.find_element(By.NAME, "email")
        email.send_keys("Your_Email")

        password = driver.find_element(By.NAME, "password")
        password.send_keys("Your_Password")

        submit = driver.find_element(By.NAME, "submit")
        submit.click()
        
        wait.until(EC.url_contains("https://loophole.eu.auth0.com/device/success"))

        driver.quit()
        
def start_loophole(subdomain,port):
    sub = f"--hostname={subdomain}"
    command = f'tunnel\\loophole.exe http {port} {sub}'.split()
    return subprocess.Popen(command,creationflags=subprocess.CREATE_NO_WINDOW,stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
 
if __name__ =='__main__':
    login_loophole("tunnel","log.txt")
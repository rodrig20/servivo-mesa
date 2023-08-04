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
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.common.by import By

        op = webdriver.ChromeOptions()
        op.add_argument('headless')

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=op)
        
        driver.get(substrings[0])

        #Escrever o Codigo
        code = driver.find_element(By.NAME,"code")
        code.send_keys(str(substrings[1]))
        time.sleep(0.1)

        enviar = driver.find_element(By.NAME,"action")
        enviar.click()

        time.sleep(0.1)

        confirmar = driver.find_elements(By.NAME,"action")
        confirmar[0].click()
        time.sleep(2)
        
        email = driver.find_element(By.NAME,"email")
        email.send_keys("Your_Email")


        password = driver.find_element(By.NAME,"password")
        password.send_keys("Your_Password")

        submit = driver.find_element(By.NAME,"submit")
        submit.click()

        time.sleep(0.5)
        driver.quit()
 
if __name__ =='__main__':       
    login_loophole("tunnel","log.txt")
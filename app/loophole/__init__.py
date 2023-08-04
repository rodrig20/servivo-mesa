import subprocess
import requests
import time
import json
import os
from random import randint

def PollForToken(device_code, interval):
    grant_type = "urn:ietf:params:oauth:grant-type:device_code"

    polling_interval = interval
    print(f"Polling with interval: {polling_interval} seconds")

    while True:
        payload = {
            "grant_type": grant_type,
            "device_code": device_code,
            "client_id": "9ocnSAnfJSb6C52waL8xcPidCkRhUwBs"
        }
        
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        
        time.sleep(polling_interval)
        response = requests.post("https://loophole.eu.auth0.com/oauth/token", data=payload, headers=headers)
        
        if response.status_code >= 200 and response.status_code <= 299:
            json_response = response.json()
            token_spec = {
                "access_token": json_response["access_token"],
                "refresh_token": json_response["refresh_token"],
                "id_token": json_response["id_token"],
                "token_type": json_response["token_type"],
                "expires_in": json_response["expires_in"]
            }
            return token_spec, None
        elif response.status_code >= 400 and response.status_code <= 499:
            json_response = response.json()
            if json_response["error"] == "authorization_pending" or json_response["error"] == "slow_down":
                continue
            elif json_response["error"] == "expired_token" or json_response["error"] == "invalid_grand":
                return None, "The device token expired, please reinitialize the login"
            elif json_response["error"] == "access_denied":
                return None, "The device token got denied, please reinitialize the login"
        else:
            return None, f"Unexpected response from authorization server: {response.content}"


def save_token(token):
    tokens_location = os.path.join(f"C:\\Users\\{os.getlogin()}", ".loophole", "tokens.json")

    token_data = json.dumps(token)
    try:
        with open(tokens_location, "w") as file:
            file.write(token_data)
    except IOError as e:
        raise Exception(f"There was a problem writing tokens file: {str(e)}")

    return None

def get_info():
    device_code_url = "https://loophole.eu.auth0.com/oauth/device/code"
    client_id = "9ocnSAnfJSb6C52waL8xcPidCkRhUwBs"
    scope = "openid offline_access profile email"
    audience = "https://api.loophole.cloud"

    payload = {
        "client_id": client_id,
        "scope": scope,
        "audience": audience
    }

    response = requests.post(device_code_url, data=payload)

    if response.status_code != 200:
        raise Exception("There was a problem executing request for device code")

    json_response = response.json()
    return json_response


def make_login(url):
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    service = Service(".app\\loophole\\tunnel\\chromeDriver\\chromedriver.exe")
    
    # Opções para rodar o navegador sem abrir a janela do navegador
    options = Options()
    options.add_argument("--headless=new")
    #options.add_argument("--disable-animations")

    # Inicie o navegador passando o serviço e as opções como parâmetros
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 10)

    driver.get(url)
    
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
    
def login_loophole():
    json_info = get_info()
    make_login(json_info["verification_uri_complete"])
    token, _ = PollForToken(json_info["device_code"],0.1)
    save_token(token)

def isLogged():
    return os.path.exists(os.path.join(f"C:\\Users\\{os.getlogin()}", ".loophole", "tokens.json"))


def enable_tunnel(domain,port,start=1):
    print(domain.value)
    process = subprocess.Popen(["app\\loophole\\tunnel\\loophole.exe", "http", str(port), "--hostname", domain.value.decode()])
    process.wait()  # Aguarda a conclusão do processo
    print(domain.value)
    if process.returncode != 0:
        if start:
            domain.value = (domain.value.decode()+"_0").encode()
        else:
            if int(domain.value.decode()[-1]) == 9:
                domain.value = (domain.value.decode()+"0").encode()
            else:
                domain.value = (domain.value.decode()[:-1]+str(int(domain.value.decode()[-1])+1)).encode()
       
        enable_tunnel(domain,port,0)

def start_loophole(domain,port):
    if not isLogged():
        print("loginnnnn")
        login_loophole()
    enable_tunnel(domain,port)


if __name__ == "__main__":
    class Dominio:
        def __init__(self,val):
            self.value = val
    dominio = Dominio(b'foka')
    start_loophole(dominio,80)
    
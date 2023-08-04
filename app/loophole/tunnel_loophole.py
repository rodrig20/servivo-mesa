import subprocess
import requests
import time
import json
import platform
import json
import os
import io
import paramiko
import json
import os
import json
from pathlib import Path

def get_local_storage_file(file_name, directory_name):
    home = str(Path.home())
    dir_name = os.path.join(home, ".loophole", directory_name)
    os.makedirs(dir_name, exist_ok=True)

    return os.path.join(dir_name, file_name)


def get_access_token():
    tokens_location = get_local_storage_file("tokens.json", "")
    try:
        with open(tokens_location, "r") as file:
            tokens = json.load(file)
            access_token = tokens.get("access_token", "")
            return access_token
    except IOError as e:
        raise Exception(f"There was a problem reading tokens: {str(e)}")
    except json.JSONDecodeError as e:
        raise Exception(f"There was a problem decoding tokens: {str(e)}")

def parsePublicKey(identityFile):
    try:
        privateKey, err = readPrivateKeyFile(identityFile)
        if err is not None:
            return None, None, err

        publicKey, err = getPublicKeyFromPrivateKey(privateKey)
        if err is not None:
            return None, None, err
        
        return publicKey, privateKey, None

    except Exception as e:
        print("ERRO\n",e)
        return None, None, e


def readPrivateKeyFile(file):
    try:
        with open(file, "r") as f:
            privateKey = f.read()

        return privateKey, None

    except Exception as e:
        return None, e


def getPublicKeyFromPrivateKey(privateKey):
    try:
        pkey = paramiko.RSAKey.from_private_key(io.StringIO(privateKey))
        publicKey = pkey.get_base64()

        return publicKey, None

    except Exception as e:
        return None, e

def user_agent():
    return f"loophole-cli/development-unknown ({platform.system()}/{platform.machine()})"

def get_refresh_token():
    tokens_location = os.path.join(f"C:\\Users\\{os.getlogin()}", ".loophole", "tokens.json")

    try:
        with open(tokens_location, 'r') as tokens_file:
            tokens = json.load(tokens_file)
    except FileNotFoundError as e:
        return "", f"There was a problem reading tokens: {e}"
    except json.JSONDecodeError as e:
        return "", f"There was a problem decoding tokens: {e}"

    return tokens.get("refresh_token", ""), None

def refresh_token():
    grant_type = "refresh_token"
    token, err = get_refresh_token()
    if err is not None:
        return err

    payload = {
        "grant_type": grant_type,
        "client_id": "9ocnSAnfJSb6C52waL8xcPidCkRhUwBs",
        "refresh_token": token
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        response = requests.post("https://loophole.eu.auth0.com/oauth/token", data=payload, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return e

    response_data = response.json()
    if 400 <= response.status_code < 500:
        error = response_data.get("error")
        error_description = response_data.get("error_description")
        print(f"Error response: error={error}, errorDescription={error_description}")

        if error == "expired_token" or error == "invalid_grand":
            return "The device token expired, please reinitialize the login"
        elif error == "access_denied":
            return "The device token got denied, please reinitialize the login"

    elif 200 <= response.status_code < 300:
        response_data["refresh_token"] = token

        err = save_token(response_data)
        if err is not None:
            return err

    else:
        return f"Unexpected response from authorization server: {response.text}"

    return None

def RegisterSite(publicKeyString, requestedSiteID,token_was_refreshed=False):
    apiURL = "api.loophole.cloud"

    accessToken = get_access_token()

    data = {
        "key": publicKeyString
    }
    if requestedSiteID:
        data["id"] = requestedSiteID
    
    jsonData = json.dumps(data)

    url = f"https://{apiURL}:443/api/site"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": user_agent(),
        "Authorization": f"Bearer {accessToken}"
    }

    req = requests.post(url, headers=headers, data=jsonData)
    
    if req.status_code == 401:
        if not token_was_refreshed:
            try:
                refresh_token()
                token_was_refreshed = True
                return RegisterSite(publicKeyString, requestedSiteID,token_was_refreshed)
            except Exception as err:
                print(err)
                return None
        else:
            return None
    return req.ok


def PollForToken(device_code, interval):
    grant_type = "urn:ietf:params:oauth:grant-type:device_code"

    polling_interval = interval

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

def enable_tunnel(domain,port,config):
    process = subprocess.Popen(["app\\loophole\\tunnel\\loophole.exe", "http", str(port), "--hostname", domain],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,creationflags=subprocess.CREATE_NO_WINDOW)
    while config.run_loophole:
        time.sleep(1)
    process.terminate()
    config.run_loophole = 2

def validDomain(domain):
    file = os.path.join(f"C:\\Users\\{os.getlogin()}", ".loophole", ".ssh","id_rsa")
    publicKey,_,_ = parsePublicKey(file)
    return RegisterSite(publicKey,domain)

def start_loophole(config,port,i):
    if not isLogged():
        login_loophole()
    start = 1
    while not validDomain(config.urls[i]):
        if start:
            config.urls[i] = (config.urls[i]+"_0")
        else:
            if int(config.urls[i][-1]) == 9:
                config.urls[i] = (config.urls[i]+"0")
            else:
                config.urls[i] = (config.urls[i][:-1]+str(int(config.urls[i][-1])+1))
        start = 0
    config.final = 1

    enable_tunnel(config.urls[i],port,config)
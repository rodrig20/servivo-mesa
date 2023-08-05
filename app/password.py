from datetime import datetime
from typing import Optional
import platform
import hashlib
import psutil
import wmi

def get_mac_address() -> str:
    interfaces = psutil.net_if_addrs()
    for _, addresses in interfaces.items():
        for addr in addresses:
            if addr.family == psutil.AF_LINK:
                return addr.address
    return "unknow"

def get_hard_drive_serial_number() -> Optional[str]:
    c = wmi.WMI()
    for physical_disk in c.Win32_DiskDrive():
        return physical_disk.SerialNumber.strip()
    return None

def get_hardware_info() -> str:
    # Obter informações específicas do hardware
    hardware_info = platform.uname()
    serial_number = get_hard_drive_serial_number()
    mac_address = get_mac_address()

    # Combinar informações em uma string
    hardware_string = (f"{hardware_info.node}-{serial_number}-{mac_address}")
    
    return hardware_string

def getHash(string) -> str:
    hash_object = hashlib.sha256(string.encode())
    return hash_object.hexdigest()

def generate_unique_id() -> str:
    # Obter as informações do hardware
    hardware_info = get_hardware_info()
    hash = getHash(hardware_info)

    return hash

def get_secret_key() -> str:
    unique_id = generate_unique_id()

    # Obter o dia e hora atuais
    agora = datetime.now() 
    dia = str(agora.day)
    mes = str(agora.month)
    ano = str(agora.year)
    hora = str(agora.hour)

    data = ano+dia+mes+hora
    hash_data = hashlib.sha256(data.encode())
    sha256_hash_data = hash_data.hexdigest()
    info = [sha256_hash_data[0:len(sha256_hash_data) // 2],sha256_hash_data[len(sha256_hash_data) // 2:]]
    full_id = info[0]+unique_id+info[1]

    return full_id

def number_to_string(number,size) -> str:
    str_number = str(number)
    while len(str_number) < size:
        str_number = "0" + str_number

    return str_number

def get_password(domain) -> str:
    agora = datetime.now()
    
    dia = agora.day
    mes = agora.month
    ano = agora.year
    hora = agora.hour
    data = ano+dia+mes+hora
    hash_data = getHash(str(data))
    
    int_hash_data = int(hash_data,16)
    pass_number = number_to_string(int_hash_data%10000,4)
    return domain+":"+pass_number

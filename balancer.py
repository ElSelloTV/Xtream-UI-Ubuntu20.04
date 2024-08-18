#!/usr/bin/env python3

import subprocess
import os
import base64
import urllib.request
from itertools import cycle

# Variables Globales
DOWNLOAD_URL = "https://bitbucket.org/xoceunder/x-ui/raw/master/sub_xui_xoceunder.tar.gz"
PACKAGES = ["libcurl4", "libxslt1-dev", "libgeoip-dev", "e2fsprogs", "wget", "mcrypt", "nscd", "htop", "zip", "unzip", "mc", "libzip-dev"]

def get_version():
    """Obtiene la versión de la distribución de Linux"""
    try:
        output = subprocess.check_output("lsb_release -d".split()).decode().strip()
        return output.split(":")[-1].strip()
    except subprocess.CalledProcessError:
        return ""

def prepare():
    """Prepara el sistema para la instalación"""
    global PACKAGES
    # Elimina archivos de bloqueo de dpkg
    for file in ["/var/lib/dpkg/lock-frontend", "/var/cache/apt/archives/lock", "/var/lib/dpkg/lock"]:
        try:
            os.remove(file)
        except FileNotFoundError:
            pass

    # Actualiza el sistema e instala paquetes necesarios
    os.system("apt-get update > /dev/null")
    for package in PACKAGES:
        os.system(f"apt-get install {package} -y > /dev/null")

    # Crea usuario y directorio para Xtream Codes
    os.system("adduser --system --shell /bin/false --group --disabled-login xtreamcodes > /dev/null")
    os.makedirs("/home/xtreamcodes", exist_ok=True)

    return True

def install():
    """Descarga e instala el paquete Xtream Codes"""
    url = DOWNLOAD_URL
    os.system(f'wget -q -O "/tmp/xtreamcodes.tar.gz" "{url}"')

    if os.path.exists("/tmp/xtreamcodes.tar.gz"):
        os.system('tar -zxvf "/tmp/xtreamcodes.tar.gz" -C "/home/xtreamcodes/" > /dev/null')
        try:
            os.remove("/tmp/xtreamcodes.tar.gz")
        except FileNotFoundError:
            pass
        return True
    return False

def encrypt(host="127.0.0.1", username="user_iptvpro", password="", database="xtream_iptvpro", server_id=1, port=7999):
    """Crea un archivo de configuración encriptado"""
    config_path = "/home/xtreamcodes/iptv_xtream_codes/config"
    try:
        os.remove(config_path)
    except FileNotFoundError:
        pass

    with open(config_path, 'wb') as file:
        data = f'{{"host":"{host}","db_user":"{username}","db_pass":"{password}","db_name":"{database}","server_id":"{server_id}","db_port":"{port}"}}'
        encrypted = ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(data, cycle('5709650b0d7806074842c6de575025b1')))
        file.write(base64.b64encode(encrypted.encode('ascii')))

def configure():
    """Configura el entorno y servicios necesarios"""
    if "/home/xtreamcodes/iptv_xtream_codes/" not in open("/etc/fstab").read():
        with open("/etc/fstab", "a") as fstab_file:
            fstab_file.write("tmpfs /home/xtreamcodes/iptv_xtream_codes/streams tmpfs defaults,noatime,nosuid,nodev,noexec,mode=1777,size=90% 0 0\n")
            fstab_file.write("tmpfs /home/xtreamcodes/iptv_xtream_codes/tmp tmpfs defaults,noatime,nosuid,nodev,noexec,mode=1777,size=2G 0 0\n")

    if "xtreamcodes" not in open("/etc/sudoers").read():
        os.system('echo "xtreamcodes ALL = (root) NOPASSWD: /sbin/iptables" >> /etc/sudoers')

    if not os.path.exists("/etc/init.d/xtreamcodes"):
        with open("/etc/init.d/xtreamcodes", "w") as init_file:
            init_file.write("#! /bin/bash\n/home/xtreamcodes/iptv_xtream_codes/start_services.sh")
        os.chmod("/etc/init.d/xtreamcodes", 0o755)

    try:
        os.remove("/usr/bin/ffmpeg")
    except FileNotFoundError:
        pass

    if not os.path.exists("/home/xtreamcodes/iptv_xtream_codes/tv_archive"):
        os.makedirs("/home/xtreamcodes/iptv_xtream_codes/tv_archive/")

    os.symlink("/home/xtreamcodes/iptv_xtream_codes/bin/ffmpeg", "/usr/bin/ffmpeg")

    os.system("chattr -i /home/xtreamcodes/iptv_xtream_codes/GeoLite2.mmdb > /dev/null")
    os.system("wget -q https://bitbucket.org/le_lio/assets/raw/master/GeoLite2.mmdb -O /home/xtreamcodes/iptv_xtream_codes/GeoLite2.mmdb")
    os.system("wget -q https://bitbucket.org/le_lio/assets/raw/master/pid_monitor.php -O /home/xtreamcodes/iptv_xtream_codes/crons/pid_monitor.php")

    os.system("chown xtreamcodes:xtreamcodes -R /home/xtreamcodes > /dev/null")
    os.system("chmod -R 0777 /home/xtreamcodes > /dev/null")
    os.system("chattr +i /home/xtreamcodes/iptv_xtream_codes/GeoLite2.mmdb > /dev/null")

    os.system("sed -i 's|chown -R xtreamcodes:xtreamcodes /home/xtreamcodes|chown -R xtreamcodes:xtreamcodes /home/xtreamcodes 2>/dev/null|g' /home/xtreamcodes/iptv_xtream_codes/start_services.sh")
    os.chmod("/home/xtreamcodes/iptv_xtream_codes/start_services.sh", 0o755)

    os.system("mount -a")
    os.chmod("/home/xtreamcodes/iptv_xtream_codes/config", 0o700)
    os.system("sed -i 's|echo \"Xtream Codes Reborn\";|header(\"Location: https://www.google.com/\");|g' /home/xtreamcodes/iptv_xtream_codes/wwwdir/index.php")

    with open("/etc/hosts", "a") as hosts_file:
        hosts_file.write("127.0.0.1    api.xtream-codes.com\n")
        hosts_file.write("127.0.0.1    downloads.xtream-codes.com\n")
        hosts_file.write("127.0.0.1    xtream-codes.com\n")

    if "@reboot root /home/xtreamcodes/iptv_xtream_codes/start_services.sh" not in open("/etc/crontab").read():
        os.system('@echo "@reboot root /home/xtreamcodes/iptv_xtream_codes/start_services.sh" >> /etc/crontab')

def firewall():
    """Configura el firewall"""
    os.system("apt-get install -y iptables-persistent netfilter-persistent")
    os.system("iptables -F INPUT")
    os.system("iptables -A INPUT -i lo -j ACCEPT")
    os.system("iptables -A INPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT")
    os.system("iptables -A INPUT -p tcp --dport 80 -j ACCEPT")
    os.system("iptables -A INPUT -p tcp --dport 7999 -j ACCEPT")
    os.system("iptables -A INPUT -j DROP")
    os.system("iptables-save > /etc/iptables/rules.v4")
    os.system("netfilter-persistent save")

def networking():
    """Reinicia la red"""
    os.system("systemctl restart networking")
    os.system("ifdown eth0 && ifup eth0")

if __name__ == "__main__":
    if get_version() == "Ubuntu 22.04.2 LTS":
        if prepare():
            if install():
                encrypt()
                configure()
                firewall()
                networking()
                print("Xtream Codes Reborn ha sido instalado y configurado exitosamente.")
            else:
                print("No se pudo instalar Xtream Codes Reborn.")
        else:
            print("No se pudo preparar el sistema.")
    else:
        print("Versión de OS no soportada.")

#!/usr/bin/python3
# -*- coding: utf-8 -*-
import subprocess, os, random, string, sys, shutil, socket, zipfile, urllib.request, urllib.error, urllib.parse, json, base64
from itertools import cycle
from zipfile import ZipFile
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

rDownloadURL = {
    "main": "https://bitbucket.org/xoceunder/x-ui/raw/master/main_xui_xoceunder.tar.gz",
    "sub": "https://bitbucket.org/xoceunder/x-ui/raw/master/sub_xui_xoceunder.tar.gz"
}

rPackages = [
    "libcurl4", "libxslt1-dev", "libgeoip-dev", "libonig-dev", "e2fsprogs", "wget", "mcrypt", "nscd", "htop", "zip",
    "unzip", "mc", "mariadb-server", "libpng16-16", "libzip-dev", "python3-paramiko", "python-is-python3"
]

rInstall = {"MAIN": "main", "LB": "sub"}
rUpdate = {"UPDATE": "update"}

# Ajuste de archivo de configuración de MySQL
rMySQLCnf = base64.b64decode(
    "IyBYdHJlYW0gQ29kZXMKCltjbGllbnRdCnBvcnQgICAgICAgICAgICA9IDMzMDYKCltteXNxbGRfc2FmZV0KbmljZSAgICAgICAgICAgID0gMAoKW215c3FsZF0KdXNlciAgICAgICAgICAgID0gbXlzcWwKcG9ydCAgICAgICAgICAgID0gNzk5OQpiYXNlZGlyICAgICAgICAgPSAvdXNyCmRhdGFkaXIgICAgICAgICA9IC92YXIvbGliL215c3FsCnRtcGRpciAgICAgICAgICA9IC90bXAKbGMtbWVzc2FnZXMtZGlyID0gL3Vzci9zaGFyZS9teXNxbApza2lwLWV4dGVybmFsLWxvY2tpbmcKc2tpcC1uYW1lLXJlc29sdmU9MQoKYmluZC1hZGRyZXNzICAgICAgICAgICAgPSAqCmtleV9idWZmZXJfc2l6ZSA9IDEyOE0KCm15aXNhbV9zb3J0X2J1ZmZlcl9zaXplID0gNE0KbWF4X2FsbG93ZWRfcGFja2V0ICAgICAgPSA2NE0KbXlpc2FtLXJlY292ZXItb3B0aW9ucyA9IEJBQ0tVUAptYXhfbGVuZ3RoX2Zvcl9zb3J0X2RhdGEgPSA4MTkyCnF1ZXJ5X2NhY2hlX2xpbWl0ICAgICAgID0gNE0KcXVlcnlfY2FjaGVfc2l6ZSAgICAgICAgPSAwCnF1ZXJ5X2NhY2hlX3R5cGUJPSAwCgpleHBpcmVfbG9nc19kYXlzICAgICAgICA9IDEwCm1heF9iaW5sb2dfc2l6ZSAgICAgICAgID0gMTAwTQoKbWF4X2Nvbm5lY3Rpb25zICA9IDIwMDAgI3JlY29tbWVuZGVkIGZvciAxNkdCIHJhbSAKYmFja19sb2cgPSA0MDk2Cm9wZW5fZmlsZXNfbGltaXQgPSAxNjM4NAppbm5vZGJfb3Blbl9maWxlcyA9IDE2Mzg0Cm1heF9jb25uZWN0X2Vycm9ycyA9IDMwNzIKdGFibGVfb3Blbl9jYWNoZSA9IDQwOTYKdGFibGVfZGVmaW5pdGlvbl9jYWNoZSA9IDQwOTYKCgp0bXBfdGFibGVfc2l6ZSA9IDFHCm1heF9oZWFwX3RhYmxlX3NpemUgPSAxRwoKaW5ub2RiX2J1ZmZlcl9wb29sX3NpemUgPSAxMkcgI3JlY29tbWVuZGVkIGZvciAxNkdCIHJhbQppbm5vZGJfYnVmZmVyX3Bvb2xfaW5zdGFuY2VzID0gMQppbm5vZGJfcmVhZF9pb190aHJlYWRzID0gNjQKaW5ub2Rf..."
)

rVersions = {
    "22.04": "jammy"
}

class col:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'  # orange on some systems
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    LIGHT_GRAY = '\033[37m'
    DARK_GRAY = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'


def generate(length=19):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def getVersion():
    try:
        return os.popen("lsb_release -d").read().split(":")[-1].strip()
    except:
        return ""


def printc(rText, rColour=col.BRIGHT_GREEN, rPadding=0, rLimit=46):
    print("%s ┌─────────────────────────────────────────────────┐ %s" % (rColour, col.ENDC))
    for _ in range(rPadding):
        print("%s │                                                 │ %s" % (rColour, col.ENDC))
    array = [rText[i:i + rLimit] for i in range(0, len(rText), rLimit)]
    for i in array:
        print("%s │ %s%s%s │ %s" % (rColour, " " * round(23 - (len(i) / 2)), i, " " * round(46 - (22 - (len(i) / 2)) - len(i)), col.ENDC))
    for _ in range(rPadding):
        print("%s │                                                 │ %s" % (rColour, col.ENDC))
    print("%s └─────────────────────────────────────────────────┘ %s" % (rColour, col.ENDC))
    print(" ")


def prepare(rType="MAIN"):
    global rPackages
    if rType != "MAIN":
        rPackages = rPackages[:-1]
    printc("Preparing Installation")
    if os.path.isfile('/home/xtreamcodes/iptv_xtream_codes/config'):
        shutil.copyfile('/home/xtreamcodes/iptv_xtream_codes/config', '/tmp/config.xtmp')
    if os.path.isfile('/home/xtreamcodes/iptv_xtream_codes/config'):
        os.system('chattr -i /home/xtreamcodes/iptv_xtream_codes/GeoLite2.mmdb > /dev/null')
    for rFile in ["/var/lib/dpkg/lock-frontend", "/var/cache/apt/archives/lock", "/var/lib/dpkg/lock"]:
        try:
            os.remove(rFile)
        except:
            pass
    printc("Updating Operating System")
    os.system("apt-get update > /dev/null")
    os.system("apt-get -y full-upgrade > /dev/null")
    if rType == "MAIN":
        printc("Install MariaDB 10.5 repository")
        os.system("apt-get install -y software-properties-common > /dev/null")
        os.system("curl -LsS https://r.mariadb.com/downloads/mariadb_repo_setup | sudo bash > /dev/null 2>&1")
        os.system("apt-get update > /dev/null")
    for rPackage in rPackages:
        printc("Installing %s" % rPackage)
        os.system("apt-get install %s -y > /dev/null" % rPackage)
    printc("Installing pip2 and python2 paramiko")
    os.system("apt-get install -y python2 > /dev/null")
    os.system("curl https://bootstrap.pypa.io/pip/2.7/get-pip.py | python2 > /dev/null 2>&1")
    os.system("pip2 install paramiko > /dev/null 2>&1")
    printc("Cleaning")
    os.system("apt-get clean > /dev/null")
    os.system("dpkg --configure -a > /dev/null")


def install(rType="MAIN"):
    rDir = os.getcwd()
    prepare(rType)
    rScript = rDownloadURL[rInstall[rType]]
    rScriptFile = rDir + '/XUI.zip'
    printc("Downloading Main Installer")
    try:
        urllib.request.urlretrieve(rScript, rScriptFile)
    except HTTPError as e:
        print('HTTPError: {}'.format(e.code))
    except URLError as e:
        print('URLError: {}'.format(e.reason))
    except Exception as e:
        print('Error: {}'.format(e))
    with zipfile.ZipFile(rScriptFile, 'r') as zf:
        printc("Extracting Installer")
        zf.extractall(rDir)
    shutil.rmtree(rDir + '/iptv_xtream_codes/.git/')
    printc("Moving Files")
    os.system("mv %s/iptv_xtream_codes /home/xtreamcodes/ > /dev/null" % rDir)
    if os.path.isfile('/tmp/config.xtmp'):
        shutil.copyfile('/tmp/config.xtmp', '/home/xtreamcodes/iptv_xtream_codes/config')
    printc("Configuring")
    os.system('cp -r /etc/mysql/ /etc/mysql.backup')
    shutil.rmtree('/etc/mysql', ignore_errors=True)
    os.mkdir('/etc/mysql')
    os.system("echo '%s' > /etc/mysql/my.cnf" % rMySQLCnf.decode())
    os.system("cp -r /etc/mysql.backup/my.cnf /etc/mysql/")
    shutil.rmtree('/etc/mysql.backup', ignore_errors=True)
    os.system("mysql_install_db > /dev/null")
    os.system("chown -R mysql:mysql /var/lib/mysql/")
    printc("Starting MariaDB")
    os.system("service mysql start > /dev/null 2>&1")
    printc("Securing Installation")
    os.system("mysql_secure_installation")
    os.system("mysql -e \"SET PASSWORD FOR 'root'@'localhost' = PASSWORD('');FLUSH PRIVILEGES;\"")
    os.system("mysql -e \"DELETE FROM mysql.user WHERE User='';\"")
    os.system("mysql -e \"DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost');\"")
    os.system("mysql -e \"DROP DATABASE test;\"")
    os.system("mysql -e \"DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';\"")
    printc("Importing Databases")
    os.system("mysql -u root < /home/xtreamcodes/iptv_xtream_codes/sql/iptv_xtream_codes.sql")
    os.system("mysql -u root < /home/xtreamcodes/iptv_xtream_codes/sql/db_clean.sql")
    printc("Installation Completed", rColour=col.BRIGHT_YELLOW)
    os.system("rm -rf %s > /dev/null" % rDir)


if __name__ == '__main__':
    rType = sys.argv[1] if len(sys.argv) > 1 else "MAIN"
    if rType.upper() == "UPDATE":
        printc("Starting Update", rColour=col.BRIGHT_BLUE)
        rDir = os.getcwd()
        printc("Updating", rColour=col.BRIGHT_BLUE)
        os.system("cd %s && git pull && chmod 775 install.sh && ./install.sh" % rDir)
    else:
        install(rType)


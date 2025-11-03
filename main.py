import os
import sys
import platform
import json
import subprocess
import urllib.request
import tarfile
import zipfile

# ======== BEÁLLÍTÁSOK ========
WALLET_ADDRESS = "44U82k9NtMoVvotg98e7qJejfymXtQqhGg21x25qBQJvWfnysKzpKoY6ch6Gu5z4zKb1mULwP78BNHNwF7EVTj1o7fteioL"
POOL_URL = "xmr-eu.kryptex.network:7029"
XMRI_GITHUB_RELEASE = "https://github.com/xmrig/xmrig/releases/download/v6.24.0/xmrig-6.24.0-linux-static-x64.tar.gz"
# ============================

def download_xmrig(url, filename):
    print("[*] Letöltés:", url)
    urllib.request.urlretrieve(url, filename)
    print("[+] Letöltve:", filename)

def extract_xmrig(filename, extract_to="."):
    print("[*] Kibontás:", filename)
    if filename.endswith(".tar.gz"):
        with tarfile.open(filename, "r:gz") as tar:
            tar.extractall(path=extract_to)
    elif filename.endswith(".zip"):
        with zipfile.ZipFile(filename, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
    else:
        print("[-] Ismeretlen archívum:", filename)
        sys.exit(1)
    print("[+] Kibontva:", extract_to)

def create_config(wallet_address, pool_url, template_path="config_template.json", output_path="config.json"):
    with open(template_path, "r") as f:
        config = json.load(f)
    config['pools'][0]['user'] = wallet_address
    config['pools'][0]['url'] = pool_url
    with open(output_path, "w") as f:
        json.dump(config, f, indent=4)
    print("[+] Config létrehozva:", output_path)

def run_miner(xmrig_path="./xmrig"):
    print("[*] Miner indítása...")
    subprocess.run([xmrig_path])

def main():
    system = platform.system()
    print("[*] Rendszer:", system)

    # 1️⃣ Letöltés
    xmrig_archive = XMRI_GITHUB_RELEASE.split("/")[-1]
    if not os.path.exists(xmrig_archive):
        download_xmrig(XMRI_GITHUB_RELEASE, xmrig_archive)
    else:
        print("[*] xmrig már letöltve:", xmrig_archive)

    # 2️⃣ Kibontás
    extract_xmrig(xmrig_archive, ".")

    # 3️⃣ Config létrehozás
    create_config(WALLET_ADDRESS, POOL_URL)

    # 4️⃣ Futtatás
    # Feltételezzük, hogy az xmrig bináris a kibontott mappában van
    xmrig_exe = [f for f in os.listdir(".") if "xmrig" in f and os.access(f, os.X_OK)]
    if xmrig_exe:
        run_miner("./" + xmrig_exe[0])
    else:
        print("[-] Nem található xmrig bináris!")

if __name__ == "__main__":
    main()

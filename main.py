import platform
from src.extractor import fetch_browser_data, QUERIES
from src.decrypt import decrypt_secret
from src.browser_enum import get_browsers_path, get_browser_secret

# color codes
RED = "\033[31m"
RESET = "\033[0m"
BOLD = "\033[1m"
MAGENTA = "\033[95m"

def censor_string(text: str | None) -> str:
    """Show first 3 characters then replace rest with plain blocks"""
    if not text:
        return ""
    if len(text) <= 3:
        return "█" * len(text)
    return text[:3] + "█" * (len(text) - 2)


BANNER = r"""                                                                                     
▄█████ ▄▄▄▄▄  ▄▄▄▄ ▄▄▄▄  ▄▄▄▄▄ ▄▄▄▄▄▄ ▄▄▄▄     ▄█████ ▄▄▄▄▄▄ ▄▄▄▄▄  ▄▄▄  ▄▄    ▄▄▄▄▄ ▄▄▄▄  
▀▀▀▄▄▄ ██▄▄  ██▀▀▀ ██▄█▄ ██▄▄    ██  ███▄▄ ▄▄▄ ▀▀▀▄▄▄   ██   ██▄▄  ██▀██ ██    ██▄▄  ██▄█▄ 
█████▀ ██▄▄▄ ▀████ ██ ██ ██▄▄▄   ██  ▄▄██▀     █████▀   ██   ██▄▄▄ ██▀██ ██▄▄▄ ██▄▄▄ ██ ██ 


        THIS TOOL WAS INTENDED FOR ACADEMIC AND NON-MALICIOUS PURPOSES ONLY.                                                                      
"""

if platform.system() == 'Windows' or platform.system() == 'Darwin':
    print(f"{RED}You seem to be running { 'MacOS' if platform.system() == 'Darwin' else platform.system() }.{RESET}")
    print(f"{RED}This tool only supports Linux-based systems.\nExiting...{RESET}")
    exit(1)

print(f"\n\n{BOLD}{MAGENTA}" + BANNER + f"{RESET}\n")

browsers = get_browsers_path()

if not browsers:
    print("[!] No browsers found.")
    exit(1)

browsers_data = {}

for browser_name, browser_path in browsers.items():
    browsers_data[browser_name] = browser_path, get_browser_secret(browser_name)

print(f"[+] Found {len(browsers_data.items())} browsers:\n")

for i, (name, (browser, secret)) in enumerate(browsers_data.items(), start=1):
    print(f"{i}. {BOLD}{MAGENTA}{name.capitalize()}{RESET} | Path: {MAGENTA}{browser}{RESET} | Secret: {MAGENTA}{censor_string(secret)}{RESET}")

try:
    choice = int(input("> ")) - 1
except ValueError:
    print("Invalid input")
    exit(1)

try:
    browser = list(browsers_data.keys())[choice]
except IndexError:
    print("Invalid choice")
    exit(1)

path, keyring_secret = browsers_data[browser]
print("\n[+] Choose what to retrieve:\n")

for i, query in enumerate(QUERIES.keys(), start=1):
    print(f"{i}. {BOLD}{MAGENTA}{query.capitalize()}{RESET}")

print(f"\n{BOLD}{RED}WARNING: Make sure your browser is closed, otherwise the DB will be locked!{RESET}")

try:
    choice = int(input("> ")) - 1
except ValueError:
    print("Invalid input")
    exit(1)

try:
    data = list(QUERIES.keys())[choice]
except IndexError:
    print("Invalid choice")
    exit(1)

browser_secrets = fetch_browser_data(path, data)

if choice == 0: # Logins
    # filter out empty passwords and usernames
    browser_secrets = [secret for secret in browser_secrets if secret[1] and secret[2]]
    print(f"\n[+] Found {len(browser_secrets)} saved passwords with valid credentials:\n")
    print("-" * 40)
    for url, user, passw in browser_secrets:
        print(f"{MAGENTA}URL:{RESET} {url[:55]}...")
        print(f"{MAGENTA}User:{RESET} {RED}{censor_string(user)}{RESET}")
        if bytes.fromhex(passw[:2*3]) == b"v11":
            print(f"{MAGENTA}Password:{RESET} {RED}{censor_string(decrypt_secret(passw, keyring_secret).decode('utf-8'))}{RESET}")
        elif bytes.fromhex(passw[:2*3]) == b"v10":
            print(f"{MAGENTA}Password:{RESET} {RED}{censor_string(decrypt_secret(passw).decode('utf-8'))}{RESET}")
        print("-" * 40)
elif choice == 3: # History
    print(f"\n[+] Found {len(browser_secrets)} history entries:\n")
    print("-" * 40)
    for url, in browser_secrets:
        print(f"{MAGENTA}URL:{RESET} {url}")
        print("-" * 40)
else:
    print("\n[+] Not implemented yet")

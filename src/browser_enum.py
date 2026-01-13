import os, subprocess

def get_browsers_path() -> dict[str, str]:
    """Returns a dictionary of browser names and their installation paths"""
    home = os.path.expanduser("~")

    browser_paths = {
        "chrome": os.path.join(home, ".config", "google-chrome"),
        "chromium": os.path.join(home, ".config", "chromium"),
        "brave": os.path.join(home, ".config", "BraveSoftware", "Brave-Browser")
    }

    existing = {}

    for name, path in browser_paths.items():
        if os.path.exists(path):
            existing[name] = path
    
    return existing

def get_browser_secret(browser_name: str) -> str | None:
    """Returns browser's secret by accessing the DE's keyring through secret-tool"""
    try:
        # NOTE: secret-tool isn't universal and tools differ in other DEs
        # TODO: Research other tools and implement them to this function
        return subprocess.check_output(["secret-tool", "lookup", "application", browser_name],
                            text=True, stderr=subprocess.DEVNULL).strip()

    except subprocess.CalledProcessError:
        return None

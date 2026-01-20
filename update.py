import os
import requests

PLUGIN_BASE_URL = "https://api.wordpress.org/plugins/info/1.2/"
PLUGIN_OUTPUT_FILE = "plugins/top_plugins.txt"

THEME_BASE_URL = "https://api.wordpress.org/themes/info/1.2/"
THEME_OUTPUT_FILE = "themes/top_themes.txt"

def update_plugins():
    print("[!] Updating the plugin list, this might take a while...")

    plugins = []
    page = 1

    while True:
        resp = requests.get(
            PLUGIN_BASE_URL,
            params={
                "action": "query_plugins",
                "request[page]": page,
                "request[per_page]": 250
            },
            timeout=15
        )

        data = resp.json()
        if not data.get("plugins"):
            break

        for plugin in data["plugins"]:
            plugins.append(plugin["slug"])

        page += 1

    # Ensure directory exists
    os.makedirs(os.path.dirname(PLUGIN_OUTPUT_FILE), exist_ok=True)

    # Write (overwrite) file
    with open(PLUGIN_OUTPUT_FILE, "w", encoding="utf-8") as f:
        for slug in plugins:
            f.write(f"{slug}\n")

    print(f"[+] Updated {len(plugins)} plugins.")

def update_themes():
    print("[!] Updating the theme list, this might take a while...")

    themes = []
    page = 1

    while True:
        resp = requests.get(
            THEME_BASE_URL,
            params={
                "action": "query_themes",
                "request[page]": page,
                "request[per_page]": 250
            },
            timeout=15
        )

        data = resp.json()
        if not data.get("themes"):
            break

        for theme in data["themes"]:
            themes.append(theme["slug"])

        page += 1

    # Ensure directory exists
    os.makedirs(os.path.dirname(THEME_OUTPUT_FILE), exist_ok=True)

    # Write (overwrite) the file
    with open(THEME_OUTPUT_FILE, "w", encoding="utf-8") as f:
        for slug in themes:
            f.write(f"{slug}\n")

    print(f"Updated {len(themes)} themes.")
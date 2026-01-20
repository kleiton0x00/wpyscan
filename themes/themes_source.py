# theme_enum.py
import requests
from bs4 import BeautifulSoup
import re
from avoidance.user_agents import get_random_user_agent

def extract_installed_themes(url):
    try:
        headers = {'User-Agent': get_random_user_agent()}
        response = requests.get(url, headers=headers)
        # response = requests.get(url)
        if 200 <= response.status_code < 300 or response.status_code == 401 or response.status_code == 403 or response.status_code == 500:
            soup = BeautifulSoup(response.text, 'html.parser')
            stylesheet_links = soup.find_all('link', attrs={'rel': 'stylesheet'}) 
            installed_themes = []
            for link in stylesheet_links:
                href = link.get('href')
                if 'themes' in href:
                    theme_name = re.search(r'/themes/([^/]+)/', href)
                    if theme_name:
                        theme_info = {
                            'name': theme_name.group(1),
                            'url': href
                        }
                        installed_themes.append(theme_info)

            # backup method
            if not installed_themes:
                pattern = r"/wp-content/themes/([^/]+)/"
                match = re.search(pattern, response.text)
                
                if match:
                    installed_themes.append(match.group(1))

            return installed_themes

    except requests.RequestException as e:
        print(f"[-] An error occurred: {e}")
        return None
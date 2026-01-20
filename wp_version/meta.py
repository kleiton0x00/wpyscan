# comments.py

import requests
import re
from avoidance.user_agents import get_random_user_agent

def extract_wordpress_version_meta(url):
    method = "Meta Generator (Passive Detection)"
    method2 = "WP Block Image CSS (Passive Detection)"
    method3 = "Dashicon (Passive Detection)"

    try:
        # response = requests.get(url)
        headers = {'User-Agent': get_random_user_agent()}
        response = requests.get(url, headers=headers, allow_redirects=True)
        response.raise_for_status()

        # Extract version from varios methods
        meta_generator_match = re.search(r'<meta name="generator" content="WordPress ([0-9.]+)"', response.text) # the most stable one
        css_blockimage_match = re.search(r'wp-includes/blocks/image/style\.min\.css\?ver=([0-9]+(?:\.[0-9]+)+)', response.text)
        dashicon_match = re.search(r'wp-includes/css/dashicons\.min\.css\?ver=([A-Za-z0-9.\-]+)', response.text)

        if meta_generator_match:
            version = meta_generator_match.group(1)
            return version, method
        
        if css_blockimage_match:
            version = css_blockimage_match.group(1)
            return version, method2
        
        if dashicon_match:
            version = dashicon_match.group(1)
            return version, method3

    except requests.exceptions.RequestException as e:
        print(f"Error accessing {url}: {e}")

    return None, None

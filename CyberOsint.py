import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from colorama import init, Fore, Style

# Initialize colorama for cross-platform ANSI color support
init()

def extract_metadata(soup):
    metadata = soup.find_all('meta')
    meta_info = {}
    for tag in metadata:
        meta_info[tag.get('name', 'N/A')] = tag.get('content', 'N/A')
    return meta_info

def extract_links(soup, base_url):
    links = soup.find_all('a', href=True)
    extracted_links = []
    for link in links:
        href = link['href']
        if href.startswith('http'):
            extracted_links.append(href)
        else:
            extracted_links.append(base_url + href)
    return extracted_links

def extract_scripts(soup):
    scripts = soup.find_all('script', src=True)
    extracted_scripts = []
    for script in scripts:
        extracted_scripts.append(script['src'])
    return extracted_scripts

def extract_emails(soup):
    emails = set()
    for tag in soup.find_all(['a', 'script']):
        if tag.has_attr('href'):
            href = tag['href']
            if href.startswith('mailto:'):
                emails.add(href.split(':')[1])
    return emails

def display_banner():
    banner = """
=================================================================================
===     ==========  ========   ==============  =======  =====   =================
==  ===  =========  ======   =   ============   ======  ===   =   ===============
=  ===============  =====   ===   ===========    =====  ==   ===   ==========  ==
=  ========  =  ==  ==========   ===  =   ===  ==  ===  =======   ===  =  ==    =
=  ========  =  ==    ======    ====    =  ==  ===  ==  =====    ====  =  ===  ==
=  =========    ==  =  =======   ===  =======  ====  =  =======   ====   ====  ==
=  ===========  ==  =  ==   ===   ==  =======  =====    ==   ===   ===   ====  ==
==  ===  ==  =  ==  =  ===   =   ===  =======  ======   ===   =   ===  =  ===  ==
===     ====   ===    ======   =====  =======  =======  =====   =====  =  ===   =
=================================================================================
    """
    print(Fore.GREEN + banner + Style.RESET_ALL)

def web_scanner(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        base_url = urlparse(response.url).scheme + '://' + urlparse(response.url).netloc
        soup = BeautifulSoup(response.content, 'html.parser')
        
        metadata = extract_metadata(soup)
        links = extract_links(soup, base_url)
        scripts = extract_scripts(soup)
        emails = extract_emails(soup)
        
        print("Metadata:")
        for key, value in metadata.items():
            print(f"{key}: {value}")
        
        print("\nLinks:")
        for link in links:
            print(link)
        
        print("\nScripts:")
        for script in scripts:
            print(script)
        
        print("\nEmails:")
        for email in emails:
            print(email)

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def start_scanner():
    display_banner()
    print("Welcome to CyberNext Web Scanner!")
    print("Menu:")
    print("1. Scan website")
    print("2. Exit")
    choice = input("Enter your choice (1 or 2): ")
    if choice == '1':
        url = input("Enter the website address: ")
        web_scanner(url)
    elif choice == '2':
        print("Exiting program. Goodbye!")
    else:
        print("Invalid choice. Please select either 1 or 2.")
        start_scanner()

# Unleash the cyber beast!
start_scanner()

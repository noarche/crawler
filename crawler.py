import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from colorama import Fore, Style, init


init(autoreset=True)

output_file = 'sites_found.txt'

visited_links = set()
links_to_visit = set()

def prompt_for_link():
    """Prompt the user for a starting link or exit command."""
    while True:
        try:
            user_input = input(Fore.CYAN + "Enter the starting link (must be an HTTPS link) or type 'exit' to quit: ").strip()
            if user_input.lower() == 'exit':
                print(Fore.RED + "Exiting program.")
                exit()
            elif user_input.startswith("https://"):
                return user_input
            else:
                print(Fore.YELLOW + "Invalid link. Please start with 'https://'.")
        except KeyboardInterrupt:
            print(Fore.RED + "\nProcess interrupted. Please provide a new link or type 'exit'.")

def save_links(link):
    """Append a unique .net or .com link to sites_found.txt."""
    with open(output_file, 'a') as file:
        file.write(link + '\n')

def crawl_website(url):
    """Crawl a website and extract all the .net and .com links."""
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            full_url = urljoin(url, href)
            parsed_url = urlparse(full_url)

            if parsed_url.scheme in ('http', 'https') and (
                parsed_url.netloc.endswith('.net') or
                parsed_url.netloc.endswith('.com') or
                parsed_url.netloc.endswith('.org') or
                parsed_url.netloc.endswith('.edu') or
                parsed_url.netloc.endswith('.gov')
            ):
                clean_url = parsed_url.scheme + '://' + parsed_url.netloc + parsed_url.path
                if clean_url not in visited_links and clean_url not in links_to_visit:
                    links_to_visit.add(clean_url)

    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Error crawling {url}: {e}")

links_to_visit.add(prompt_for_link())

while True:
    try:
        while links_to_visit:
            url = links_to_visit.pop()
            if url not in visited_links:
                print(Fore.GREEN + f"Crawling: {url}")
                visited_links.add(url)
                crawl_website(url)
                save_links(url)
        print(Fore.GREEN + "Crawling completed.")
        break

    except KeyboardInterrupt:
        print(Fore.RED + "\nProcess interrupted. Let's add another link.")
        links_to_visit.add(prompt_for_link())

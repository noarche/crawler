import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from colorama import Fore, Style, init
import time

init(autoreset=True)

output_file = 'sites_found.txt'
total_bandwidth = 0

def prompt_for_link():
    """Prompt the user for a starting link or exit command."""
    while True:
        try:
            user_input = input(Fore.CYAN + "Enter the starting link (must be a link or type 'exit' to quit): ").strip()
            if user_input.lower() == 'exit':
                print(Fore.RED + "Exiting program.")
                exit()
            if not user_input.startswith("http"):
                user_input = "https://" + user_input
            return user_input
        except KeyboardInterrupt:
            print(Fore.RED + "\nProcess interrupted. Please provide a new link or type 'exit'.")

def prompt_for_delay():
    """Prompt the user for a delay between requests."""
    while True:
        try:
            delay = float(input(Fore.CYAN + "Enter delay in seconds between requests (e.g., 0.5): ").strip())
            if delay >= 0:
                return delay
            print(Fore.RED + "Delay must be a non-negative number.")
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a number.")
        except KeyboardInterrupt:
            print(Fore.RED + "\nProcess interrupted. Please provide a delay time.")

def save_links(link):
    """Append a unique .net or .com link to sites_found.txt."""
    with open(output_file, 'a') as file:
        file.write(link + '\n')

def crawl_website(url, visited_links, links_to_visit):
    """Crawl a website and extract all the .net and .com links."""
    global total_bandwidth
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        bandwidth_used = len(response.text.encode('utf-8')) / (1024 * 1024)
        total_bandwidth += bandwidth_used

        soup = BeautifulSoup(response.text, 'html.parser')

        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            if any(href.endswith(ext) for ext in ['.ico', '.png', '.jpg', '.webp', '.webm', '.pdf', '.doc', '.docx', '.svg', '.jpeg', '.json', '.onion', '.i2p', '.safetensors', '.rar', '.zip', '.gguf', '.ggml', '.shp', '.gif', '.avi', '.mp3', '.wav', '.mkv', '.mp4', '.m4a', '.flac', '.ogg', '.opus', '.avif', '.hc', '.tc', '.xyz', '.exe', '.msi', '.tar', '.7z', '.tif', '.css', '.csv']):
                continue  

            full_url = urljoin(url, href)
            parsed_url = urlparse(full_url)

            if parsed_url.scheme in ('http', 'https') and (
                parsed_url.netloc.endswith('.net') or
                parsed_url.netloc.endswith('.com') or
                parsed_url.netloc.endswith('.edu') or
                parsed_url.netloc.endswith('.gov') or
                parsed_url.netloc.endswith('.io') or
                parsed_url.netloc.endswith('.it') or
                parsed_url.netloc.endswith('.co.uk')
            ):
                clean_url = parsed_url.scheme + '://' + parsed_url.netloc + parsed_url.path
                if clean_url not in visited_links and clean_url not in links_to_visit:
                    links_to_visit.add(clean_url)

    except Exception as e:
        print(Fore.RED + f"Error crawling {url}: {e}")
        return False  
    
    return True  

while True:
    try:
        visited_links = set()
        links_to_visit = {prompt_for_link()}
        delay = prompt_for_delay()

        while links_to_visit:
            url = links_to_visit.pop()
            if url not in visited_links:
                print(Fore.GREEN + f"Crawling: {url}")
                visited_links.add(url)
                if crawl_website(url, visited_links, links_to_visit):
                    save_links(url)
                    print(Fore.YELLOW + f"Total bandwidth used: {total_bandwidth:.2f} MB")
                time.sleep(delay)

        print(Fore.GREEN + "Crawling completed.")
        
    except KeyboardInterrupt:
        print(Fore.RED + "\nProcess interrupted. Let's add another link.")
        continue
    except Exception as e:
        print(Fore.RED + f"\nScript crashed: {e}. Please provide a new link.")
        continue

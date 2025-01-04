import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from colorama import Fore, Style, init
import time
import random
import argparse
from user_agents import USER_AGENTS
import os
import signal
from blacklist import is_blacklisted, manage_blacklist

main_logo = ''' 

crawler hello
'''
infoabt = ''' 
Explain what script does, about, help.
'''

print(main_logo)
print(infoabt)

init(autoreset=True)

output_file = 'sites_found.txt'
total_bandwidth = 0
MAX_REQUESTS_PER_LINK = 999999
DEFAULT_MAX_LINKS = 999999

exit_flag = False
restart_flag = False


def signal_handler(signum, frame):
    global restart_flag
    print(Fore.YELLOW + "\nInterrupt received. Returning to the main menu.")
    restart_flag = True

signal.signal(signal.SIGINT, signal_handler)

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Crawl and extract links from provided URLs.")
    parser.add_argument('-i', '--input', type=str, help="Path to a text file containing URLs (one per line).")
    parser.add_argument('-help', action='store_true', help="Show detailed help information about the script.")
    return parser.parse_args()

def show_help():
    """Display help information."""
    help_text = """
    This script crawls websites and extracts links matching the original TLD of the provided domains. 

    Features:
      - Takes input as a comma-separated list of URLs or reads from a file (one URL per line).
      - Allows setting a delay between requests.
      - Limits the number of links to parse per URL.
      - Saves found links to a file (sites_found.txt).

    Usage:
      - Provide URLs as input separated by commas, or type 'domains.txt' to read from a file.
      - Use -i argument to specify a file containing domains.

    """
    print(Fore.CYAN + help_text)

def prompt_for_links(file_path=None):
    """Prompt the user for starting links or exit command."""
    if file_path:
        try:
            with open(file_path, 'r') as file:
                links = [line.strip() if line.strip().startswith("http") else "https://" + line.strip() for line in file]
                return links
        except FileNotFoundError:
            print(Fore.RED + f"File not found: {file_path}")
            exit()

    while True:
        try:
            user_input = input(Fore.CYAN + "Enter starting links (comma-separated) or type a '.txt' file name (type 'exit' to quit): ").strip()
            if user_input.lower() == 'exit':
                exit()
            if user_input.lower().endswith('.txt'):
                if os.path.isfile(user_input):
                    return prompt_for_links(user_input)
                else:
                    print(Fore.RED + f"File not found: {user_input}")
                    continue
            links = [link.strip() if link.startswith("http") else "https://" + link.strip() for link in user_input.split(',')]
            return links
        except KeyboardInterrupt:
            print(Fore.RED + "\nProcess interrupted. Returning to the main menu.")
            return []

def prompt_for_delay():
    """Prompt the user for a delay between requests."""
    while True:
        try:
            delay_input = input(Fore.CYAN + "Enter delay in seconds between requests (leave empty for 0.02, type 'exit' to quit): ").strip()
            if delay_input.lower() == 'exit':
                exit()
            if delay_input == '':
                return 0.02
            delay = float(delay_input)
            if delay >= 0:
                return delay
            print(Fore.RED + "Delay must be a non-negative number.")
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a number.")

def prompt_for_max_links():
    """Prompt the user for the maximum number of links to parse per URL."""
    while True:
        try:
            max_links_input = input(Fore.CYAN + f"Enter the maximum number of links to parse per URL (leave empty for {DEFAULT_MAX_LINKS}): ").strip()
            if max_links_input.lower() == 'exit':
                exit()
            if max_links_input == '':
                return DEFAULT_MAX_LINKS
            max_links = int(max_links_input)
            if max_links > 0:
                return max_links
            print(Fore.RED + "The maximum number of links must be a positive integer.")
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter an integer.")

def save_links(link):
    """Append a unique .net or .com link to sites_found.txt."""
    with open(output_file, 'a') as file:
        file.write(link + '\n')

def get_random_user_agent():
    """Return a random user agent from the USER_AGENTS list."""
    return random.choice(USER_AGENTS)

from blacklist import is_blacklisted, manage_blacklist

# Add an option to manage the blacklist in your script
def prompt_for_blacklist():
    """Prompt user to manage the blacklist."""
    while True:
        manage_choice = input("Would you like to manage the blacklist? (yes/no): ").strip().lower()
        if manage_choice == 'yes':
            manage_blacklist()
            return
        elif manage_choice == 'no':
            return
        else:
            print("Invalid input. Please type 'yes' or 'no'.")

# Integrate blacklist check in crawl_website function
def crawl_website(url, visited_links, links_to_visit, original_tld):
    """Crawl a website and extract all links matching the original TLD."""
    global total_bandwidth

    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    if is_blacklisted(domain):
        print(Fore.YELLOW + f"Skipping blacklisted domain: {domain}")
        return False

    try:
        headers = {"User-Agent": get_random_user_agent()}
        response = requests.get(url, headers=headers, timeout=2.69)
        response.raise_for_status()

        bandwidth_used = len(response.text.encode('utf-8')) / (1024 * 1024)
        total_bandwidth += bandwidth_used

        soup = BeautifulSoup(response.text, 'html.parser')

        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            if any(href.endswith(ext) for ext in [...]):  # Keep your existing file extension check here
                continue  

            full_url = urljoin(url, href)
            parsed_url = urlparse(full_url)
            domain = parsed_url.netloc

            if is_blacklisted(domain):
                print(Fore.YELLOW + f"Skipping blacklisted domain: {domain}")
                continue

            if parsed_url.scheme in ('http', 'https') and parsed_url.netloc.endswith(original_tld):
                clean_url = parsed_url.scheme + '://' + parsed_url.netloc + parsed_url.path
                if clean_url not in visited_links and clean_url not in links_to_visit:
                    links_to_visit.add(clean_url)

    except Exception as e:
        print(Fore.RED + f"Error crawling {url}: {e}")
        return False  

    return True  

# Before crawling, allow the user to manage the blacklist
prompt_for_blacklist()


args = parse_arguments()
if args.help:
    show_help()
    exit()

while True:
    try:
        visited_links = set()
        links_to_visit = set(prompt_for_links(args.input))
        if not links_to_visit:
            continue

        delay = prompt_for_delay()
        max_links_per_url = prompt_for_max_links()

        while links_to_visit and not restart_flag:
            url = links_to_visit.pop()
            request_count = 0
            parsed_links_count = 0
            original_tld = '.' + urlparse(url).netloc.split('.')[-1]

            while url not in visited_links and request_count < MAX_REQUESTS_PER_LINK and parsed_links_count < max_links_per_url:
                print(Fore.BLUE + f"Crawling: {url}")
                visited_links.add(url)
                if crawl_website(url, visited_links, links_to_visit, original_tld):
                    save_links(url)
                    parsed_links_count += 1
                    print(Fore.RED + f"Total bandwidth used: {total_bandwidth:.2f} MB")
                time.sleep(delay)
                request_count += 1

        if restart_flag:
            restart_flag = False
            print(Fore.CYAN + "Returning to the main menu.")

    except KeyboardInterrupt:
        print(Fore.YELLOW + "\nProcess interrupted. Returning to the main menu.")
        restart_flag = True
        continue
    except Exception as e:
        print(Fore.RED + f"\nScript crashed: {e}. Please provide a new link.")
        continue

# blacklist.py

from colorama import Fore, Style, init
import os

init(autoreset=True)

BLACKLIST_FILE = "blacklist.txt"

def load_blacklist():
    """Load the blacklist from a file."""
    if not os.path.exists(BLACKLIST_FILE):
        return set()
    with open(BLACKLIST_FILE, 'r') as file:
        return set(line.strip() for line in file if line.strip())

def add_to_blacklist(domain):
    """Add a domain to the blacklist."""
    with open(BLACKLIST_FILE, 'a') as file:
        file.write(domain + '\n')

def is_blacklisted(domain):
    """Check if a domain is blacklisted."""
    blacklist = load_blacklist()
    return domain in blacklist

def manage_blacklist():
    """Allow the user to manage the blacklist."""
    while True:
        print(Fore.YELLOW + "\n" + "=" * 30)
        print(Fore.CYAN + Style.BRIGHT + " Blacklist Manager")
        print(Fore.YELLOW + "=" * 30)
        print(Fore.MAGENTA + Style.BRIGHT + "1." + Fore.GREEN + " View blacklist")
        print(Fore.MAGENTA + Style.BRIGHT + "2." + Fore.GREEN + " Add domain to blacklist")
        print(Fore.MAGENTA + Style.BRIGHT + "3." + Fore.RED + " Exit blacklist manager")

        choice = input(Fore.CYAN + Style.BRIGHT + "Enter your choice: ").strip()

        if choice == '1':
            blacklist = load_blacklist()
            print(Fore.YELLOW + "\nBlacklisted Domains:")
            if blacklist:
                for domain in blacklist:
                    print(Fore.GREEN + f"- {domain}")
            else:
                print(Fore.RED + "No domains in the blacklist.")
        elif choice == '2':
            domain = input(Fore.CYAN + Style.BRIGHT + "Enter the domain to blacklist: ").strip()
            if domain:
                add_to_blacklist(domain)
                print(Fore.GREEN + f"{domain} added to blacklist.")
        elif choice == '3':
            print(Fore.YELLOW + "Exiting blacklist manager.")
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again.")

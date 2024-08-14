import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


output_file = 'sites_found.txt'


visited_links = set()
links_to_visit = set()


start_link = input("Enter the starting link (must be an HTTPS link): ").strip()


if start_link.startswith("https://"):
    links_to_visit.add(start_link)
else:
    print("Invalid link. Please start with 'https://'.")
    exit()

def save_links(link):
    """Append a unique .net or .com link to sites_found.txt"""
    with open(output_file, 'a') as file:
        file.write(link + '\n')

def crawl_website(url):
    """Crawl a website and extract all the .net and .com links"""
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            full_url = urljoin(url, href)
            parsed_url = urlparse(full_url)

            
            if parsed_url.scheme in ('http', 'https') and (parsed_url.netloc.endswith('.net') or parsed_url.netloc.endswith('.com') or parsed_url.netloc.endswith('.org') or parsed_url.netloc.endswith('.edu') or parsed_url.netloc.endswith('.gov')):
                clean_url = parsed_url.scheme + '://' + parsed_url.netloc + parsed_url.path
                if clean_url not in visited_links and clean_url not in links_to_visit:
                    links_to_visit.add(clean_url)

    except requests.exceptions.RequestException as e:
        print(f"Error crawling {url}: {e}")


while links_to_visit:
    url = links_to_visit.pop()  
    if url not in visited_links:
        print(f"Crawling: {url}")
        visited_links.add(url)
        crawl_website(url)
        save_links(url)

print("Crawling completed.")

import requests
import concurrent.futures
import random
from colorama import init, Fore
import pyfiglet
import os

# Initialize colorama
init()

# Function to generate colored ASCII art
def generate_colored_ascii_art(text, color):
    ascii_art = pyfiglet.figlet_format(text)
    colored_ascii_art = ''
    for line in ascii_art.splitlines():
        colored_ascii_art += f'{color}{line}\n'
    return colored_ascii_art

# Function to generate a random color from colorama.Fore colors
def random_color():
    colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]
    return random.choice(colors)

# Function to get or generate random color and store it in a file
def get_or_generate_random_color():
    color_file = 'random_color.txt'
    if os.path.exists(color_file):
        with open(color_file, 'r') as f:
            color = f.read().strip()
            if color in [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]:
                return color
    else:
        color = random_color()
        with open(color_file, 'w') as f:
            f.write(color)
        return color

# Function to check if a proxy is active by connecting to Bing
def is_proxy_active(proxy):
    try:
        response = requests.get("https://www.bing.com", proxies={"https": proxy}, timeout=10)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

# Function to fetch proxies from a text file
def fetch_proxies_from_file(file_name):
    try:
        with open(file_name, 'r') as file:
            proxies = [line.strip() for line in file.readlines()]
        return proxies
    except FileNotFoundError:
        print(f"{Fore.RED}File '{file_name}' not found. Fetching free proxies from API...{Fore.RESET}")
        return fetch_proxies_from_api()

# Function to fetch free proxies from API
def fetch_proxies_from_api():
    api_url = "https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&proxy_format=protocolipport&format=text"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.text.splitlines()
    else:
        print(f"{Fore.RED}Failed to fetch proxies from API. Exiting...{Fore.RESET}")
        return []

# Function to filter proxies based on criteria
def filter_proxy(proxy, protocol, anonymity, country):
    if is_proxy_active(proxy):
        # Strip the protocol prefix if present
        proxy = proxy.replace('http://', '').replace('https://', '').replace('socks4://', '').replace('socks5://', '')
        # Placeholder for additional checks like anonymity, speed, and uptime
        print(f"{get_or_generate_random_color()}Active and Working Proxy is [{proxy}]{Fore.RESET}")
        return proxy
    else:
        return None

# Main function to orchestrate the process
def main():
    # Display colored ASCII art for "Active Proxy"
    color = get_or_generate_random_color()
    print(generate_colored_ascii_art("Active - Proxies", color))

    # User input for the name of the text file containing proxies
    file_name = input(f"{Fore.CYAN}Enter the name of your text file (if you have otherwise leave empty) containing proxies (e.g., proxies.txt): {Fore.RESET}").strip()

    # Fetch proxies from the text file or API
    proxies = fetch_proxies_from_file(file_name)

    if not proxies:
        print(f"{Fore.RED}No proxies found. Exiting...{Fore.RESET}")
        return

    # User inputs for protocol, anonymity, and country
    protocols = ['http', 'https', 'socks4', 'socks5']
    anonymities = ['transparent', 'anonymous', 'highly-anonymous', 'elite']

    while True:
        protocol = input(f"{Fore.CYAN}Enter the type of protocol ({', '.join(protocols)}): {Fore.RESET}").strip().lower()
        if protocol in protocols:
            break
        else:
            print(f"{Fore.RED}Invalid protocol. Please choose from the available options.{Fore.RESET}")

    while True:
        anonymity = input(f"{Fore.CYAN}Enter the type of anonymity ({', '.join(anonymities)}): {Fore.RESET}").strip().lower()
        if anonymity in anonymities:
            break
        else:
            print(f"{Fore.RED}Invalid anonymity level. Please choose from the available options.{Fore.RESET}")

    country = input(f"{Fore.CYAN}Enter the country code for proxies (leave empty for any country): {Fore.RESET}").strip().upper()

    # Ask user how many proxies they want
    while True:
        try:
            num_proxies = int(input(f"{Fore.CYAN}Enter the number of proxies you want (leave empty for unlimited): {Fore.RESET}"))
            if num_proxies >= 0:
                break
            else:
                print(f"{Fore.RED}Please enter a non-negative integer.{Fore.RESET}")
        except ValueError:
            num_proxies = 0
            break

    # Implement checks and filtering using concurrent.futures
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for proxy in proxies:
            future = executor.submit(filter_proxy, proxy, protocol, anonymity, country)
            active_proxy = future.result()
            if active_proxy:
                if num_proxies > 0:
                    num_proxies -= 1
                    if num_proxies == 0:
                        break

    # Terminate the program
    print(f"{Fore.CYAN}Program terminated.{Fore.RESET}")
    exit()

# Entry point of the script
if __name__ == "__main__":
    main()

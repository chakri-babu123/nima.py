#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from termcolor import colored
import random
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_usernames(username, num_usernames=20, delay_min=1, delay_max=3):
    url = f"https://www.instagram.com/{username}/"
    try:
        delay = random.uniform(delay_min, delay_max)
        time.sleep(delay)
        logging.info(f"Fetching Instagram profile: {username}")
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        usernames = set()
        suggestions_section = soup.find('div', {'class': 'KC1QD'})
        if suggestions_section:
            for suggestion in suggestions_section.find_all('a', {'class': 'FPmhX notranslate _0imsa '}):
                suggestion_username = suggestion.text
                if username.lower() in suggestion_username.lower() and suggestion_username.lower() != username.lower():
                    usernames.add(suggestion_username)
                if len(usernames) >= num_usernames:
                    break
        logging.info(f"Scraped {len(usernames)} similar usernames")
        return list(usernames)
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching Instagram profile: {e}")
        return []

def check_passwords(usernames, passwords):
    for username in usernames:
        matched = False
        for password in passwords:
            delay = random.uniform(1, 3)
            time.sleep(delay)
            if username in password:
                print(colored(f"{username}: {password} - Matched", 'green'))
                matched = True
                break
        if not matched:
            print(colored(f"{username} - Not matched with any password", 'red'))

def main():
    username = input("Enter Instagram username: ")

    num_usernames = int(input("Enter number of usernames to scrape (default is 20): ") or 20)
    delay_min = float(input("Enter minimum delay between requests in seconds (default is 1): ") or 1)
    delay_max = float(input("Enter maximum delay between requests in seconds (default is 3): ") or 3)

    logging.info("Starting Instagram username scraping")

    usernames = scrape_usernames(username, num_usernames, delay_min, delay_max)

    if usernames:
        logging.info("Listing scraped usernames")
        for i, username in enumerate(usernames, start=1):
            print(f"{i}. {username}")

        password1 = input("Enter password 1: ")
        password2 = input("Enter password 2: ")
        password3 = input("Enter password 3: ")
        passwords = [password1, password2, password3]

        logging.info("Starting password checking")
        check_passwords(usernames, passwords)
    else:
        print(colored("Exiting due to error.", 'red'))

if __name__ == "__main__":
    main()

import sys
import random
from requests import Session
from requests.exceptions import RequestException
from typing import Iterator
from pathlib import Path

# Banner Information
BANNER = """
███    ███  █████  ██ ██       ██████  ███████ ███    ██ 
████  ████ ██   ██ ██ ██      ██       ██      ████   ██ 
██ ████ ██ ███████ ██ ██      ██   ███ █████   ██ ██  ██ 
██  ██  ██ ██   ██ ██ ██      ██    ██ ██      ██  ██ ██ 
██      ██ ██   ██ ██ ███████  ██████  ███████ ██   ████ 
┌───────────────────────────────────────────────────────┐
│ Version: 0.5 │ Github: @fernstedt | Created by math0x │
└───────────────────────────────────────────────────────┘
"""
print(BANNER)  # Print the banner at the start


def load_from_web(urls: list[str]) -> Iterator[str]:
    url: str
    session: Session = Session()
    for url in urls:
        names: list[str] = []
        try:
            response = session.get(url)
        except RequestException:
            continue
        names = response.text.splitlines()
        yield from names


def load_from_files(files: list[Path]) -> Iterator[str]:
    file: Path
    for file in files:
        with file.open("r", encoding="utf-8") as f:
            yield from f.readlines()


def load_hosts(file_path):
    with open(file_path, "r") as file:
        return [line.strip() for line in file.readlines()]


def generate_emails(first_names, last_names, hosts, num_emails):
    emails = []
    for _ in range(num_emails):  # Generate specified number of emails
        first_name = random.choice(first_names).lower()  # Convert to lowercase
        last_name = random.choice(last_names).lower()  # Convert to lowercase
        host = random.choice(hosts).lower()  # Convert to lowercase

        # Generate different email formats
        emails.append(f"{first_name}.{last_name}@{host}")
        emails.append(f"{first_name}{last_name}@{host}")

    return emails


def save_emails(emails, output_file):
    with open(output_file, "w") as file:
        for email in emails:
            file.write(email + "\n")


def print_help():
    help_text = """
Usage: python mailgen.py [options]

Options:
  -h            Show this help message and exit
  -n <number>   Specify the number of emails to create (default: 100)
  -o <file>     Specify the output file name (default: emails.txt)

Example:
  python mailgen.py -n 50 -o my_emails.txt
"""
    print(help_text)


def main():
    # Default values
    num_emails = 100
    output_file = "emails.txt"

    # Command-line argument parsing
    args = sys.argv[1:]
    for i in range(len(args)):
        if args[i] == "-h":
            print_help()
            return
        elif args[i] == "-n" and i + 1 < len(args):
            num_emails = int(args[i + 1])
        elif args[i] == "-o" and i + 1 < len(args):
            output_file = args[i + 1]

    first_name_files: list[str] = [
        "https://raw.githubusercontent.com/fernstedt/SecLists/master/Usernames/Names/femalenames-usa-top1000.txt",
        "https://raw.githubusercontent.com/fernstedt/SecLists/master/Usernames/Names/forenames-india-top1000.txt",
        "https://raw.githubusercontent.com/fernstedt/SecLists/master/Usernames/Names/malenames-usa-top1000.txt",
        "https://raw.githubusercontent.com/fernstedt/SecLists/master/Usernames/Names/names.txt",
    ]  # Add more paths as needed
    last_names: list[str] = list(
        load_from_web(
            [
                "https://raw.githubusercontent.com/fernstedt/SecLists/master/Usernames/Names/familynames-usa-top1000.txt"
            ]
        )
    )  # Update with actual path
    hosts = load_hosts("hosts.txt")  # Update the path to the correct location

    first_names: list[str] = list(load_from_web(first_name_files))
    emails = generate_emails(first_names, last_names, hosts, num_emails)
    save_emails(emails, output_file)


if __name__ == "__main__":
    main()

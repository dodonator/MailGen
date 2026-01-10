import random
from requests import Session
from requests.exceptions import RequestException
from typing import Iterator, Iterable
from pathlib import Path
from argparse import ArgumentParser

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

# Default values
NUMBER_OF_MAILS = 100
OUTPUT_PATH = Path("emails.txt")


def load_from_web(urls: list[str]) -> Iterator[str]:
    url: str
    session: Session = Session()
    for url in urls:
        names: list[str]
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


def save_emails(emails: Iterable[str], output_file: str | Path):
    if isinstance(output_file, str):
        output_file = Path(output_file)
    with output_file.open("w", encoding="utf-8") as file:
        for email in emails:
            file.write(f"{email}\n")


def main():
    print(BANNER)  # Print the banner at the start

    parser: ArgumentParser = ArgumentParser(
        "mailGen", description="Generate random mail addresses"
    )
    parser.add_argument(
        "-n",
        "--number",
        type=int,
        help="Number of emails to create",
        default=NUMBER_OF_MAILS,
    )
    parser.add_argument(
        "-o", "--output", type=Path, help="Output file path", default=OUTPUT_PATH
    )

    # Command-line argument parsing
    args = parser.parse_args()
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
    emails = generate_emails(first_names, last_names, hosts, args.number)
    save_emails(emails, args.output)


if __name__ == "__main__":
    main()

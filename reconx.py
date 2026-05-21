import time
import whois
import socket
import random
import requests

from rich import print
from rich.panel import Panel
from rich.table import Table
from urllib.parse import urlparse
from rich.progress import Progress
from concurrent.futures import ThreadPoolExecutor, as_completed


# ============================================
# CONFIG
# ============================================

THREADS = 100
TIMEOUT = 5

INTERESTING_CODES = [200, 301, 302, 401, 403, 500, 404]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (X11; Linux x86_64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
]

session = requests.Session()


# ============================================
# BANNER
# ============================================

def banner():
    print("""

[red bold]

██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗██╗  ██╗
██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║╚██╗██╔╝
██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║ ╚███╔╝
██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║ ██╔██╗
██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║██╔╝ ██╗
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝
[/]
[cyan]
                  - RECON X -
       [ stealth recon & scanning engine ]
[/]

[green bold]* Recon Tool Framework[/]
[white bold]* Created By:[/] [red bold]nabil_jakoubi[/]
[magenta bold]* Instagram[/] : [white bold]@nabil_jakoubi[/]
""")


# ============================================
# LOGGING
# ============================================

def save_result(data):
    try:
        with open("results.txt", "a", encoding="utf-8") as f:
            f.write(data + "\n")
    except Exception as e:
        print(f"[red]Write error:[/] {e}")


def log_error(err):
    try:
        with open("errors.txt", "a", encoding="utf-8") as f:
            f.write(str(err) + "\n")
    except:
        pass


# ============================================
# RANDOM HEADERS
# ============================================

def random_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": random.choice(["text/html", "application/json", "*/*"]),
        "Accept-Language": random.choice(["en-US,en;q=0.9", "fr-FR", "ar-MA"]),
        "Connection": "close"
    }


# ============================================
# VALIDATION
# ============================================

def validate_url(url):
    parsed = urlparse(url)
    return bool(parsed.scheme and parsed.netloc)


# ============================================
# LOAD WORDLIST
# ============================================

def load_wordlist(file):
    try:
        with open(file, "r", encoding="utf-8", errors="ignore") as f:
            return [x.strip() for x in f if x.strip()]
    except:
        print("[red]Wordlist missing[/]")
        return []


# ============================================
# DOMAIN INFO
# ============================================


def info_gathering(domain):

    print("\n[bold cyan][+] Extract Information From Domain[/]\n")

    if domain.startswith("http://") or domain.startswith("https://"):
        print("\n[red bold][!] Invalid Domain Format[/]")
        print("[yellow bold][*] Example:[/] example.com\n")
        return

    try:
        ip = socket.gethostbyname(domain)

        try:
            info = whois.whois(domain)
        except Exception:
            info = None

        # =========================
        # SAFE VALUES
        # =========================

        creation = "N/A"
        expiration = "N/A"
        registrar = "N/A"
        emails = "N/A"
        nameservers = "N/A"

        if info:

            creation = (
                info.creation_date[0]
                if isinstance(info.creation_date, list)
                else info.creation_date
            )

            expiration = (
                info.expiration_date[0]
                if isinstance(info.expiration_date, list)
                else info.expiration_date
            )

            registrar = info.registrar or "N/A"
            emails = info.emails or "N/A"
            nameservers = info.name_servers or "N/A"

        # =========================
        # OUTPUT STYLE
        # =========================

        print(f"[green bold]📅 Date of establishment:[/] [magenta bold]{creation}[/]")
        time.sleep(1)

        print(f"[green bold]⏳ Expiration date:[/] [magenta bold]{expiration}[/]")
        time.sleep(1)

        print(f"[green bold]🏢 Registrar:[/] [magenta bold]{registrar}[/]")
        time.sleep(1)

        print(f"[green bold]📧 Emails:[/] [magenta bold]{emails}[/]")
        time.sleep(1)

        print(f"[green bold]🛰️ Server Name:[/] [magenta bold]{nameservers}[/]")
        time.sleep(1)

        print("[+]----------- [white on red bold]GET IP && Reverse DNS[/] -----------[+]")
        time.sleep(1)

        print(f"[green bold]The IP:[/] [magenta bold]{ip}[/]")
        print("\n[chartreuse2 bold][^_^] Results saved -> (results.txt)[/]")
        # =========================
        # REVERSE DNS
        # =========================

        try:
            reverse = socket.gethostbyaddr(ip)[0]
            print(f"[green bold]Reverse DNS:[/] [magenta bold]{reverse}[/]")
        except:
            print(f"[red]Reverse DNS: Not Found[/]")

    except socket.gaierror:
        print("[red bold]Invalid domain[/]")

    except Exception as e:
        print(f"[red bold]Error:[/] {e}")


# ============================================
# PATH SCAN
# ============================================

def scan_path(path, base_url):
    url = base_url + path

    try:
        r = session.get(url, headers=random_headers(), timeout=TIMEOUT, allow_redirects=False)

        if r.status_code in INTERESTING_CODES:
            if r.status_code == 200:
                print(f"[green bold][+] OK[/] -> [blue]{url}[/]")
            
            if r.status_code == 301:
                print(f"[yellow bold][*] Moved Permanently[/] -> [blue]{url}[/]")
            
            if r.status_code == 302:
                print(f"[cyan bold][+] Found[/] -> [blue]{url}[/]")
            
            if r.status_code == 401:
                print(f"[red bold][!] Unauthorized[/] -> [blue]{url}[/]")

            if r.status_code == 403:
                print(f"[red bold][-] Forbidden[/] -> [blue]{url}[/]")
            
            if r.status_code == 500:
                print(f"[magenta bold][!] Internal Server[/] -> [blue]{url}[/]")

            if r.status_code == 404:
                print(f"[red bold][-] Not Found[/] -> [blue]{url}[/]")
                
            
            save_result(f"{r.status_code} | {url}")

    except Exception as e:
        log_error(e)


def start_path_scan(base_url):

    print("\n                      [white on red bold][+]  Path Scaning  [+][/]\n")

    if not base_url.endswith("/"):
        base_url += "/"

    paths = load_wordlist("common.txt")

    with Progress() as progress:
        task = progress.add_task("\n[cyan bold]Scanning...[/]", total=len(paths))

        with ThreadPoolExecutor(max_workers=THREADS) as ex:
            futures = [ex.submit(scan_path, p, base_url) for p in paths]

            for _ in as_completed(futures):
                progress.update(task, advance=1)

    print("\n[green bold][+] Successfull Scan.[/]")
    print("\n[chartreuse2 bold][^_^] Results saved -> (results.txt)[/]")


# ============================================
# SUBDOMAIN SCAN
# ============================================

FOUND_SUBS = False


def check_sub(sub, domain):

    global FOUND_SUBS

    full = f"{sub}.{domain}"

    try:
        socket.gethostbyname(full)

        for proto in ["https", "http"]:

            try:
                r = session.get(
                    f"{proto}://{full}",
                    timeout=3,
                    allow_redirects=False
                )

                if r.status_code in INTERESTING_CODES:

                    FOUND_SUBS = True

                    if r.status_code == 200:
                        print(f"[green bold][+] OK[/] -> [blue]{full}[/]")

                    elif r.status_code == 301:
                        print(f"[yellow bold][*] Moved Permanently[/] -> [blue]{full}[/]")

                    elif r.status_code == 302:
                        print(f"[cyan bold][+] Found[/] -> [blue]{full}[/]")

                    elif r.status_code == 401:
                        print(f"[magenta bold][!] Unauthorized[/] -> [blue]{full}[/]")

                    elif r.status_code == 403:
                        print(f"[red bold][-] Forbidden[/] -> [blue]{full}[/]")

                    elif r.status_code == 404:
                        print(f"[red bold][-] Not Found[/] -> [blue]{full}[/]")

                    elif r.status_code == 500:
                        print(f"[bright_red bold][!] Internal Server Error[/] -> [blue]{full}[/]")

                    save_result(f"{r.status_code} | {proto}://{full}")
                    return

            except:
                pass

    except:
        return


def start_subdomain_scan(domain):

    global FOUND_SUBS
    FOUND_SUBS = False

    print("\n                      [white on red bold][+]  Subdomain Scaning  [+][/]\n")

    if domain.startswith("http://") or domain.startswith("https://"):
        print("\n[red bold][!] Invalid Domain Format[/]")
        print("[yellow bold][*] Example:[/] example.com\n")
        return

    subs = load_wordlist("subdomains.txt")

    with Progress() as progress:
        task = progress.add_task("[cyan bold]Scanning...[/]", total=len(subs))

        with ThreadPoolExecutor(max_workers=THREADS) as ex:
            futures = [ex.submit(check_sub, s, domain) for s in subs]

            for _ in as_completed(futures):
                progress.update(task, advance=1)

    if FOUND_SUBS:
        print("\n[green bold][+] Subdomain Scanning Successful.[/]")
        print("\n[chartreuse2 bold][^_^] Results saved -> (results.txt)[/]")
    else:
        print("\n[red bold][!] No Subdomains Found.[/]")
# ============================================
# MENU
# ============================================

def menu():

    print("""

[bold cyan]
========== MENU ==========
[/]

[green]1[/] Path Scan
[green]2[/] Subdomain Scan
[green]3[/] Domain Info
[green]4[/] Run All
[red bold]5 Exit[/]

[bold cyan]
==========================
[/]
""")

    return input("[?] Choose : ").strip()


# ============================================
# MAIN (MENU FIRST THEN INPUT)
# ============================================

def main():

    banner()

    while True:

        choice = menu()

        if choice == "5":
            print("\n[red bold]Exiting...[/]\n\n[cyan bold]Happy Hacking  ✌️[/]")
            time.sleep(1)
            break

        elif choice == "1":
            url = input("Enter URL : ").strip()
            if validate_url(url):
                start_path_scan(url)
            else:
                print("[red bold][!] Invalid URL[/]")
                print("[yellow bold]The URL Must be start with https:// or http://[/]")

        elif choice == "2":
            domain = input("Enter Domain like (example.com) : ").strip()
            start_subdomain_scan(domain)

        elif choice == "3":
            domain = input("Enter Domain : ").strip()
            info_gathering(domain)

        elif choice == "4":
            url = input("Enter URL : ").strip()

            if not validate_url(url):
                print("[red][!] Invalid URL[/]")
                continue

            domain = urlparse(url).netloc

            info_gathering(domain)
            start_path_scan(url)
            start_subdomain_scan(domain)

        else:
            print("[yellow bold][!] Invalid option[/]")


if __name__ == "__main__":
    try:
        main()
        

    except KeyboardInterrupt:
        print("\n[light_salmon3 bold][!] Stopping...[/]")
        time.sleep(1)
        print("\n[cyan bold]Happy Hacking ✌️[/]")
        exit()

    except Exception as e:
        print(f"[red bold][!] Error:[/] {e}")

